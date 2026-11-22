import pytest
from fastapi.testclient import TestClient
from main import app, items_db

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "AFIT Lost" in response.text

def test_get_items():
    response = client.get("/api/items")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 10  # All mock items

def test_signup_and_login_workflow():
    # Sign up creates an account in the stored registry
    res = client.post("/api/signup", json={"name": "Demo User", "email": "demo@afit.edu.ng", "password": "secret123"})
    assert res.status_code == 200
    assert res.json()["email"] == "demo@afit.edu.ng"
    # Login with correct password returns the profile
    res2 = client.post("/api/login", json={"email": "demo@afit.edu.ng", "password": "secret123"})
    assert res2.status_code == 200
    assert res2.json()["name"] == "Demo User"
    # Duplicate signup rejected
    res3 = client.post("/api/signup", json={"name": "Demo User", "email": "demo@afit.edu.ng", "password": "secret123"})
    assert res3.status_code == 400
    # Wrong password rejected
    res4 = client.post("/api/login", json={"email": "demo@afit.edu.ng", "password": "wrongpass"})
    assert res4.status_code == 401
    # Unknown email points to sign up
    res5 = client.post("/api/login", json={"email": "ghost@afit.edu.ng", "password": "whatever"})
    assert res5.status_code == 404
    # Short password rejected at signup
    res6 = client.post("/api/signup", json={"name": "X", "email": "x@afit.edu.ng", "password": "123"})
    assert res6.status_code == 400
    # Passwords are never stored in plain text
    import main
    stored = next(u for u in main.users_db if u["email"] == "demo@afit.edu.ng")
    assert "password" not in stored and stored["password_hash"] != "secret123"

def test_claim_then_confirm_return_workflow():
    item_id = items_db[0]["id"]
    claim_data = {
        "claimant_name": "Cadet Test Officer",
        "claimant_id": "AFIT/2024/0001",
        "contact_phone": "08011223344",
        "claimant_email": "claimant@afit.edu.ng",
        "proof_description": "Exact serial number match and department seal",
    }
    res = client.post(f"/api/items/{item_id}/claim", data=claim_data)
    assert res.status_code == 200
    data = res.json()
    assert data["item"]["status"] == "Claim Requested"
    # claim details are not echoed publicly; the claimant can read their own via the claim endpoint
    mine = client.get(f"/api/items/{item_id}/claim", params={"claimant_email": "claimant@afit.edu.ng"}).json()
    assert mine["claimant_email"] == "claimant@afit.edu.ng"

    # Item is NOT marked returned until handover is confirmed
    statuses = {i["id"]: i["status"] for i in client.get("/api/items").json()}
    assert statuses[item_id] == "Claim Requested"

    # Confirm the physical return - reporter only
    res_noauth = client.post(f"/api/items/{item_id}/confirm-return", json={"reporter_email": "stranger@afit.edu.ng"})
    assert res_noauth.status_code == 403
    res3 = client.post(f"/api/items/{item_id}/confirm-return", json={"reporter_email": items_db[0]["contact_email"]})
    assert res3.status_code == 200
    assert res3.json()["item"]["status"] == "Claimed/Returned"

def test_claim_blocked_once_already_requested():
    item_id = items_db[1]["id"]
    claim = {
        "claimant_name": "First Claimant",
        "claimant_id": "AFIT/2024/0002",
        "contact_phone": "08000000001",
        "claimant_email": "first@afit.edu.ng",
        "proof_description": "details",
    }
    assert client.post(f"/api/items/{item_id}/claim", data=claim).status_code == 200
    res = client.post(f"/api/items/{item_id}/claim", data=claim)
    assert res.status_code == 400

def test_chat_is_private_to_reporter_and_claimant():
    item_id = items_db[2]["id"]
    # Claim it first so a claimant exists
    claim = {
        "claimant_name": "Private Claimant",
        "claimant_id": "AFIT/2024/0003",
        "contact_phone": "08000000003",
        "claimant_email": "claimant3@afit.edu.ng",
        "proof_description": "details",
    }
    item = client.post(f"/api/items/{item_id}/claim", data=claim).json()["item"]
    reporter_email = item["contact_email"]

    # Claimant can post and read
    res = client.post(f"/api/items/{item_id}/messages", json={
        "sender_name": "Private Claimant", "sender_email": "claimant3@afit.edu.ng",
        "sender_role": "claimant", "text": "Is my ID card with you?",
        "peer_email": reporter_email})
    assert res.status_code == 200
    res2 = client.get(f"/api/items/{item_id}/messages", params={"user_email": "claimant3@afit.edu.ng", "peer": reporter_email})
    assert res2.status_code == 200
    assert any(m["text"] == "Is my ID card with you?" for m in res2.json())

    # Reporter reads the same thread
    res3 = client.get(f"/api/items/{item_id}/messages", params={"user_email": reporter_email, "peer": "claimant3@afit.edu.ng"})
    assert res3.status_code == 200

    # A stranger cannot read or post
    assert client.get(f"/api/items/{item_id}/messages", params={"user_email": "stranger@afit.edu.ng"}).status_code == 403
    res4 = client.post(f"/api/items/{item_id}/messages", json={
        "sender_name": "Stranger", "sender_email": "stranger@afit.edu.ng",
        "sender_role": "claimant", "text": "hello?"})
    assert res4.status_code == 403

    # Empty messages rejected
    res5 = client.post(f"/api/items/{item_id}/messages", json={
        "sender_name": "Private Claimant", "sender_email": "claimant3@afit.edu.ng",
        "sender_role": "claimant", "text": "   "})
    assert res5.status_code == 400

def test_reporter_cannot_claim_own_item():
    # Item 4 is reported by amina.b@afit.edu.ng
    item = next(i for i in items_db if i["item_type"] == "found" and i["status"] == "Active")
    claim = {
        "claimant_name": "Self Claimer",
        "claimant_id": "AFIT/2024/9999",
        "contact_phone": "08000000009",
        "claimant_email": item["contact_email"],
        "proof_description": "trying to claim my own report",
    }
    res = client.post(f"/api/items/{item['id']}/claim", data=claim)
    assert res.status_code == 400
    assert "cannot claim" in res.json()["detail"]
    # Status unchanged
    statuses = {i["id"]: i["status"] for i in client.get("/api/items").json()}
    assert statuses[item["id"]] == "Active"

def test_reject_claim_returns_item_to_active():
    item_id = items_db[3]["id"]  # a lost item, Active
    claim = {
        "claimant_name": "Wrong Claimant",
        "claimant_id": "AFIT/2024/0004",
        "contact_phone": "08000000004",
        "claimant_email": "wrong@afit.edu.ng",
        "proof_description": "vague details",
    }
    assert client.post(f"/api/items/{item_id}/claim", data=claim).status_code == 200
    # A stranger cannot reject
    res = client.post(f"/api/items/{item_id}/reject-claim", json={"reporter_email": "stranger@afit.edu.ng"})
    assert res.status_code == 403
    # The reporter rejects: item falls back to Active
    res2 = client.post(f"/api/items/{item_id}/reject-claim", json={"reporter_email": items_db[3]["contact_email"]})
    assert res2.status_code == 200
    assert res2.json()["item"]["status"] == "Active"
    # Item can be claimed again after rejection - but NOT by the rejected claimant
    res_same = client.post(f"/api/items/{item_id}/claim", data=claim)
    assert res_same.status_code == 403
    claim2 = dict(claim, claimant_email="rightful@afit.edu.ng", claimant_name="Rightful Owner")
    assert client.post(f"/api/items/{item_id}/claim", data=claim2).status_code == 200

    # cleanup: confirm return so seed data is not left hanging
    client.post(f"/api/items/{item_id}/confirm-return", json={"reporter_email": items_db[1]["contact_email"]})

def test_only_reporter_can_delete():
    payload = {
        "title": "Delete Permission Probe", "description": "x", "category": "Other",
        "location": "Library", "date": "2026-11-22", "item_type": "found",
        "contact_name": "Owner", "contact_email": "owner2@afit.edu.ng", "contact_phone": "08077777777",
        "reporter_id": "AFIT/TEST/OW12", "security_personnel": "Campus Security Desk",
    }
    item_id = client.post("/api/items", data=payload).json()["id"]
    # A stranger cannot delete someone else's report
    res = client.delete(f"/api/items/{item_id}", params={"reporter_email": "stranger@afit.edu.ng"})
    assert res.status_code == 403
    # The reporter can
    res2 = client.delete(f"/api/items/{item_id}", params={"reporter_email": "owner2@afit.edu.ng"})
    assert res2.status_code == 200

def test_claimant_can_edit_submitted_claim():
    item_id = items_db[4]["id"]
    claim = {
        "claimant_name": "Editable Claimant", "claimant_id": "AFIT/2024/0005",
        "contact_phone": "08000000005", "claimant_email": "editable@afit.edu.ng",
        "proof_description": "initial proof",
    }
    assert client.post(f"/api/items/{item_id}/claim", data=claim).status_code == 200
    # The claimant edits their claim while it awaits handover
    upd = dict(claim, proof_description="updated proof with serial number")
    res = client.put(f"/api/items/{item_id}/claim", json=upd)
    assert res.status_code == 200
    details = client.get(f"/api/items/{item_id}/claim", params={"claimant_email": "editable@afit.edu.ng"}).json()
    assert details["proof_description"] == "updated proof with serial number"
    # A stranger cannot edit someone else's claim
    res2 = client.put(f"/api/items/{item_id}/claim", json=dict(upd, claimant_email="stranger@afit.edu.ng"))
    assert res2.status_code == 403
    # cleanup
    client.post(f"/api/items/{item_id}/reject-claim", json={"reporter_email": items_db[4]["contact_email"]})

def test_dispute_flow():
    item_id = items_db[6]["id"]
    claim = {
        "claimant_name": "Suspicious Claimant", "claimant_id": "AFIT/2024/0007",
        "contact_phone": "08000000007", "claimant_email": "sus@afit.edu.ng",
        "proof_description": "vague",
    }
    assert client.post(f"/api/items/{item_id}/claim", data=claim).status_code == 200
    # A third party reports the claim as wrong
    res = client.post(f"/api/items/{item_id}/dispute", json={
        "name": "Real Owner", "email": "realowner@afit.edu.ng",
        "message": "That item is mine - serial number ABC123"})
    assert res.status_code == 200
    items = client.get("/api/items", params={"viewer_email": items_db[6]["contact_email"]}).json()
    item = next(i for i in items if i["id"] == item_id)
    assert len(item["disputes"]) == 1
    assert item["disputes"][0]["email"] == "realowner@afit.edu.ng"
    # anonymous viewers see the dispute without the disputer's email
    anon = next(i for i in client.get("/api/items").json() if i["id"] == item_id)
    assert "email" not in anon["disputes"][0]
    # Empty message rejected
    res2 = client.post(f"/api/items/{item_id}/dispute", json={"name": "X", "email": "x@afit.edu.ng", "message": "  "})
    assert res2.status_code == 400
    # Reporter reviews and rejects the wrong claim -> item back to Active
    res3 = client.post(f"/api/items/{item_id}/reject-claim", json={"reporter_email": items_db[7]["contact_email"]})
    assert res3.status_code == 200
    assert res3.json()["item"]["status"] == "Active"

def test_reporter_can_resolve_disputes():
    item_id = items_db[7]["id"]
    reporter_email = items_db[6]["contact_email"]
    claim = {
        "claimant_name": "Suspicious Claimant", "claimant_id": "AFIT/2024/0007",
        "contact_phone": "08000000007", "claimant_email": "sus@afit.edu.ng",
        "proof_description": "vague",
    }
    assert client.post(f"/api/items/{item_id}/claim", data=claim).status_code == 200
    res = client.post(f"/api/items/{item_id}/dispute", json={
        "name": "Real Owner", "email": "realowner@afit.edu.ng",
        "message": "That item is mine - serial number ABC123"})
    assert res.status_code == 200
    # A stranger cannot resolve
    res_s = client.post(f"/api/items/{item_id}/disputes/0/resolve", json={"reporter_email": "stranger@afit.edu.ng", "action": "uphold"})
    assert res_s.status_code == 403
    # The reporter upholds: claim rejected, item back to Active, dispute marked upheld
    res2 = client.post(f"/api/items/{item_id}/disputes/0/resolve", json={"reporter_email": reporter_email, "action": "uphold"})
    assert res2.status_code == 200
    assert res2.json()["item"]["status"] == "Active"
    item = next(i for i in client.get("/api/items").json() if i["id"] == item_id)
    assert item["disputes"][0]["status"] == "upheld"
    assert "claim_details" not in item
    # Resolving twice is blocked
    res3 = client.post(f"/api/items/{item_id}/disputes/0/resolve", json={"reporter_email": reporter_email, "action": "uphold"})
    assert res3.status_code == 400

def test_input_validation_rejects_nonsense():
    base = {
        "title": "Validation Probe", "description": "x", "category": "Other",
        "location": "Library", "date": "2026-11-22", "item_type": "lost",
        "contact_name": "Mathew John", "contact_email": "1mathewumama@gmail.com",
        "contact_phone": "08031234567", "reporter_id": "U23CS1067",
        "security_personnel": "Campus Security Desk",
    }
    # Bad phone
    res = client.post("/api/items", data=dict(base, contact_phone="abcdefghijk"))
    assert res.status_code == 400 and "phone" in res.json()["detail"].lower()
    # Bad matric (letters only, no digits)
    res = client.post("/api/items", data=dict(base, reporter_id="nonsenseid"))
    assert res.status_code == 400 and "matric" in res.json()["detail"].lower()
    # Bad email
    res = client.post("/api/items", data=dict(base, contact_email="not-an-email"))
    assert res.status_code == 400 and "email" in res.json()["detail"].lower()
    # Bad name (digits)
    res = client.post("/api/items", data=dict(base, contact_name="12345"))
    assert res.status_code == 400 and "name" in res.json()["detail"].lower()
    # Valid data passes
    ok = client.post("/api/items", data=base)
    assert ok.status_code == 200
    client.delete(f"/api/items/{ok.json()['id']}", params={"reporter_email": "1mathewumama@gmail.com"})

def test_rejected_claimant_cannot_reclaim():
    item_id = items_db[8]["id"]
    claim = {
        "claimant_name": "Repeat Claimant", "claimant_id": "AFIT/2024/0009",
        "contact_phone": "08000000009", "claimant_email": "repeat@afit.edu.ng",
        "proof_description": "first attempt",
    }
    assert client.post(f"/api/items/{item_id}/claim", data=claim).status_code == 200
    client.post(f"/api/items/{item_id}/reject-claim", json={"reporter_email": items_db[8]["contact_email"]})
    # The rejected claimant is locked out of this specific item
    res = client.post(f"/api/items/{item_id}/claim", data=claim)
    assert res.status_code == 403
    assert "rejected" in res.json()["detail"].lower()
    # Other people can still claim
    claim2 = dict(claim, claimant_email="other@afit.edu.ng", claimant_name="Other Person")
    assert client.post(f"/api/items/{item_id}/claim", data=claim2).status_code == 200
    client.post(f"/api/items/{item_id}/reject-claim", json={"reporter_email": items_db[8]["contact_email"]})

def test_chat_unread_counts():
    item_id = items_db[10]["id"]
    claim = {
        "claimant_name": "Unread Claimant", "claimant_id": "AFIT/2024/0011",
        "contact_phone": "08000000011", "claimant_email": "unread@afit.edu.ng",
        "proof_description": "details",
    }
    assert client.post(f"/api/items/{item_id}/claim", data=claim).status_code == 200
    client.post(f"/api/items/{item_id}/messages", json={
        "sender_name": "Unread Claimant", "sender_email": "unread@afit.edu.ng",
        "sender_role": "claimant", "text": "hello there",
        "peer_email": items_db[10]["contact_email"]})
    thread_key = f"{item_id}:unread@afit.edu.ng"
    counts = client.get("/api/chat/unread", params={"user_email": "unread@afit.edu.ng"}).json()
    assert counts.get(thread_key) == 1
    counts2 = client.get("/api/chat/unread", params={"user_email": items_db[10]["contact_email"]}).json()
    assert counts2.get(thread_key) == 1
    counts3 = client.get("/api/chat/unread", params={"user_email": "stranger@afit.edu.ng"}).json()
    assert thread_key not in counts3

def test_security_personnel_rules():
    base = {
        "title": "Sec Field Probe", "description": "x", "category": "Other",
        "location": "Library", "date": "2026-11-22", "contact_name": "Mathew John",
        "contact_email": "1mathewumama@gmail.com", "contact_phone": "08031234567",
        "reporter_id": "U23CS1067",
    }
    # Lost report: security officer field NOT required (owner is reporting their own loss)
    res = client.post("/api/items", data=dict(base, item_type="lost"))
    assert res.status_code == 200
    lost_id = res.json()["id"]
    client.delete(f"/api/items/{lost_id}", params={"reporter_email": "1mathewumama@gmail.com"})
    # Found report WITHOUT handover officer is rejected
    res = client.post("/api/items", data=dict(base, item_type="found"))
    assert res.status_code == 400 and "handed" in res.json()["detail"].lower()
    # Found report with officer passes
    res = client.post("/api/items", data=dict(base, item_type="found", security_personnel="Student"))
    assert res.status_code == 200
    client.delete(f"/api/items/{res.json()['id']}", params={"reporter_email": "1mathewumama@gmail.com"})

def test_finder_response_flow():
    item_id = items_db[8]["id"]  # lost item (HP Pavilion Gaming Laptop)
    # Self-response blocked
    res = client.post(f"/api/items/{item_id}/found-report", json={
        "finder_name": "Mathew John", "finder_id": "U23CS1067",
        "finder_phone": "08031234567", "finder_email": items_db[9]["contact_email"],
        "location_found": "Library", "message": ""})
    assert res.status_code == 400
    # Bad phone blocked
    res = client.post(f"/api/items/{item_id}/found-report", json={
        "finder_name": "Good Samaritan", "finder_id": "AFIT/2024/0123",
        "finder_phone": "notaphone", "finder_email": "finder@afit.edu.ng",
        "location_found": "Library", "message": ""})
    assert res.status_code == 400
    # Valid response
    res = client.post(f"/api/items/{item_id}/found-report", json={
        "finder_name": "Good Samaritan", "finder_id": "AFIT/2024/0123",
        "finder_phone": "08031234567", "finder_email": "finder@afit.edu.ng",
        "location_found": "Library ground floor", "message": "Safe with me"})
    assert res.status_code == 200
    # Duplicate response blocked
    res = client.post(f"/api/items/{item_id}/found-report", json={
        "finder_name": "Good Samaritan", "finder_id": "AFIT/2024/0123",
        "finder_phone": "08031234567", "finder_email": "finder@afit.edu.ng",
        "location_found": "Library", "message": ""})
    assert res.status_code == 400
    # The finder can now use the private chat; a stranger cannot
    assert client.get(f"/api/items/{item_id}/messages", params={"user_email": "finder@afit.edu.ng", "peer": items_db[8]["contact_email"]}).status_code == 200
    assert client.get(f"/api/items/{item_id}/messages", params={"user_email": "stranger@afit.edu.ng", "peer": items_db[8]["contact_email"]}).status_code == 403
    # A second finder gets their OWN thread - messages never leak across
    client.post(f"/api/items/{item_id}/found-report", json={
        "finder_name": "Second Finder", "finder_id": "AFIT/2024/0456",
        "finder_phone": "08031234568", "finder_email": "finder2@afit.edu.ng",
        "location_found": "Mosque Area", "message": ""})
    client.post(f"/api/items/{item_id}/messages", json={
        "sender_name": "Good Samaritan", "sender_email": "finder@afit.edu.ng",
        "sender_role": "finder", "text": "I have your laptop", "peer_email": items_db[8]["contact_email"]})
    thread1 = client.get(f"/api/items/{item_id}/messages", params={"user_email": items_db[8]["contact_email"], "peer": "finder@afit.edu.ng"}).json()
    thread2 = client.get(f"/api/items/{item_id}/messages", params={"user_email": items_db[8]["contact_email"], "peer": "finder2@afit.edu.ng"}).json()
    assert any(m["text"] == "I have your laptop" for m in thread1)
    assert all(m["text"] != "I have your laptop" for m in thread2)
    # Unread counts are keyed per thread
    counts = client.get("/api/chat/unread", params={"user_email": "finder@afit.edu.ng"}).json()
    assert counts.get(f"{item_id}:finder@afit.edu.ng") == 1

def test_similar_items_matching():
    res = client.get("/api/items/similar", params={"title": "Black Nike School Bag Lost"})
    assert res.status_code == 200
    matches = res.json()
    assert any(m["id"] == items_db[0]["id"] for m in matches)
    # Nonsense title matches nothing
    res = client.get("/api/items/similar", params={"title": "zzz qqq xxx"})
    assert res.json() == []

def test_mark_found_by_owner():
    item_id = items_db[5]["id"]  # lost item (Oraimo earbuds)
    # Stranger cannot mark it
    res = client.post(f"/api/items/{item_id}/mark-found", json={"reporter_email": "stranger@afit.edu.ng"})
    assert res.status_code == 403
    # Owner marks it found via a specific finder
    client.post(f"/api/items/{item_id}/found-report", json={
        "finder_name": "Returner Sam", "finder_id": "AFIT/2024/0555",
        "finder_phone": "08055555555", "finder_email": "returner@afit.edu.ng",
        "location_found": "Cafeteria", "message": ""})
    res = client.post(f"/api/items/{item_id}/mark-found",
                      json={"reporter_email": items_db[5]["contact_email"], "finder_email": "returner@afit.edu.ng"})
    assert res.status_code == 200
    item = next(i for i in client.get("/api/items").json() if i["id"] == item_id)
    assert item["status"] == "Claimed/Returned"
    assert "Returner Sam" in item["resolved_via"]
    # Cannot mark twice
    res = client.post(f"/api/items/{item_id}/mark-found", json={"reporter_email": items_db[5]["contact_email"]})
    assert res.status_code == 400

def test_close_report_by_owner():
    created = client.post("/api/items", data={
        "title": "Close Test Calculator", "description": "Casio fx-991", "category": "Other",
        "location": "Library", "date": "2026-11-22", "item_type": "lost",
        "contact_name": "Mathew John", "contact_email": "1mathewumama@gmail.com",
        "contact_phone": "08031234567", "reporter_id": "U23CS1067"})
    assert created.status_code == 200
    item_id = created.json()["id"]
    res = client.post(f"/api/items/{item_id}/close-report", json={"reporter_email": "stranger@afit.edu.ng"})
    assert res.status_code == 403
    res = client.post(f"/api/items/{item_id}/close-report", json={"reporter_email": "1mathewumama@gmail.com"})
    assert res.status_code == 200
    item = next(i for i in client.get("/api/items").json() if i["id"] == item_id)
    assert item["status"] == "Closed"
    res = client.post(f"/api/items/{item_id}/close-report", json={"reporter_email": "1mathewumama@gmail.com"})
    assert res.status_code == 400
    client.delete(f"/api/items/{item_id}", params={"reporter_email": "1mathewumama@gmail.com"})

def test_public_api_strips_private_fields():
    # Anonymous viewer: no contact details, no claim proof, no finder contacts
    items = client.get("/api/items").json()
    sample = next(i for i in items if i["id"] == items_db[0]["id"])
    assert "contact_email" not in sample and "contact_phone" not in sample
    assert "claim_details" not in sample and "found_reports" not in sample
    assert "rejected_claimants" not in sample and "seeded" not in sample
    # Reporter sees their own contact back
    items_r = client.get("/api/items", params={"viewer_email": items_db[0]["contact_email"]}).json()
    mine = next(i for i in items_r if i["id"] == items_db[0]["id"])
    assert mine["contact_email"] == items_db[0]["contact_email"]
    assert mine["viewer_is_reporter"] is True
    # A stranger is not the reporter even if they guess the viewer param
    assert mine["viewer_is_reporter"] is True  # correct email
    items_s = client.get("/api/items", params={"viewer_email": "stranger@afit.edu.ng"}).json()
    theirs = next(i for i in items_s if i["id"] == items_db[0]["id"])
    assert theirs["viewer_is_reporter"] is False and "contact_email" not in theirs

def test_finder_and_claimant_private_endpoints():
    # finder responses are reporter-only
    res = client.get(f"/api/items/{items_db[8]['id']}/finders", params={"reporter_email": "stranger@afit.edu.ng"})
    assert res.status_code == 403
    res = client.get(f"/api/items/{items_db[8]['id']}/finders", params={"reporter_email": items_db[8]["contact_email"]})
    assert res.status_code == 200 and isinstance(res.json(), list)
    # claim details are claimant-only
    res = client.get(f"/api/items/{items_db[2]['id']}/claim", params={"claimant_email": "stranger@afit.edu.ng"})
    assert res.status_code == 403

def test_upload_validation():
    base = {
        "title": "Upload Probe", "description": "x", "category": "Other", "location": "Library",
        "date": "2026-11-22", "item_type": "lost", "contact_name": "Mathew John",
        "contact_email": "1mathewumama@gmail.com", "contact_phone": "08031234567",
        "reporter_id": "U23CS1067",
    }
    # non-image extension rejected
    res = client.post("/api/items", data=base, files={"image": ("evil.html", b"<h1>x", "text/html")})
    assert res.status_code == 400 and "image" in res.json()["detail"].lower()
    # path-traversal filename is neutralized (uuid name), valid image accepted
    res = client.post("/api/items", data=base, files={"image": ("../../evil.png", b"PNG-fake-bytes", "image/png")})
    assert res.status_code == 200
    url = res.json()["image_url"]
    assert url.startswith("/static/uploads/") and "evil" not in url
    client.delete(f"/api/items/{res.json()['id']}", params={"reporter_email": "1mathewumama@gmail.com"})

def test_reporter_can_edit_report():
    created = client.post("/api/items", data={
        "title": "Editable Probe Item", "description": "Original description here",
        "category": "Electronics", "location": "Library", "date": "2026-11-22",
        "item_type": "lost", "contact_name": "Mathew Umama",
        "contact_email": "1mathewumama@gmail.com", "contact_phone": "08031234567",
        "reporter_id": "U23CS1067"})
    assert created.status_code == 200
    item_id = created.json()["id"]
    edit = {
        "reporter_email": "1mathewumama@gmail.com", "title": "Editable Probe Item (Updated)",
        "description": "Updated description with more detail", "category": "Electronics",
        "location": "LR 201", "date": "2026-11-21", "preferred_contact": "phone",
        "security_personnel": "Mathew Umama", "contact_name": "Mathew Umama",
        "contact_phone": "08099999999", "reporter_id": "U23CS1067"}
    # Stranger cannot edit
    res = client.put(f"/api/items/{item_id}", data=dict(edit, reporter_email="stranger@afit.edu.ng", title="Hacked Title"))
    assert res.status_code == 403
    # Owner edits everything, including replacing the photo
    res = client.put(f"/api/items/{item_id}", data=edit,
                     files={"image": ("newphoto.png", b"PNG-fake-bytes", "image/png")})
    assert res.status_code == 200
    # read back as the reporter (public view strips contact details)
    item = next(i for i in client.get("/api/items", params={"viewer_email": "1mathewumama@gmail.com"}).json() if i["id"] == item_id)
    assert item["title"] == "Editable Probe Item (Updated)"
    assert item["location"] == "LR 201"
    assert item["contact_phone"] == "08099999999"
    assert item["image_url"].startswith("/static/uploads/item")
    # Invalid phone rejected by the validation gate
    res = client.put(f"/api/items/{item_id}", data=dict(edit, contact_phone="badphone"))
    assert res.status_code == 400
    # Invalid date rejected
    res = client.put(f"/api/items/{item_id}", data=dict(edit, date="not-a-date"))
    assert res.status_code == 400
    client.delete(f"/api/items/{item_id}", params={"reporter_email": "1mathewumama@gmail.com"})

def test_lost_report_rate_limit():
    base = {
        "title": "Rate Limit Probe",
        "description": "spam check",
        "category": "Other",
        "location": "Library",
        "date": "2026-11-22",
        "item_type": "lost",
        "contact_name": "Spammer",
        "contact_email": "spam@afit.edu.ng",
        "contact_phone": "08099999999",
        "reporter_id": "AFIT/TEST/SP12",
        "security_personnel": "Campus Security Desk",
    }
    created = []
    for n in range(3):
        payload = dict(base, title=f"Rate Limit Probe {n}")
        res = client.post("/api/items", data=payload)
        assert res.status_code == 200
        created.append(res.json()["id"])
    res = client.post("/api/items", data=base)
    assert res.status_code == 429
    for item_id in created:
        client.delete(f"/api/items/{item_id}", params={"reporter_email": "spam@afit.edu.ng"})

def test_custom_location_and_category_accepted():
    payload = {
        "title": "Custom Field Probe",
        "description": "custom dropdown values",
        "category": "Sports Gear",
        "location": "Cadet Mess Hall",
        "date": "2026-11-22",
        "item_type": "found",
        "contact_name": "Finder",
        "contact_email": "finder@afit.edu.ng",
        "contact_phone": "08088888888",
        "reporter_id": "AFIT/TEST/CU12",
        "security_personnel": "Campus Security Desk",
        "preferred_contact": "email",
        "custody": "finder",
    }
    res = client.post("/api/items", data=payload)
    assert res.status_code == 200
    item = res.json()
    assert item["location"] == "Cadet Mess Hall"
    assert item["category"] == "Sports Gear"
    assert item["custody"] == "finder"
    client.delete(f"/api/items/{item['id']}", params={"reporter_email": "finder@afit.edu.ng"})

def test_state_persists_to_disk():
    import os
    assert os.path.exists("db.json")

def test_pwa_assets_served():
    assert client.get("/static/manifest.webmanifest").status_code == 200
    assert client.get("/static/sw.js").status_code == 200
    assert client.get("/static/app.js").status_code == 200
    assert client.get("/static/icon-192.png").status_code == 200
