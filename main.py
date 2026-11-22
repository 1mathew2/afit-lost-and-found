from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import shutil
import json
import hashlib
import re
import secrets
import uuid
import os

app = FastAPI(title="AFIT Lost & Found Portal (Project SP-014)", version="3.0.0")

# Ensure upload directory exists
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
UPLOAD_DIR = os.path.join(STATIC_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

items_db = [
    {
        "seeded": True,
        "id": 1,
        "item_type": "lost",
        "category": "Bags & Luggage",
        "title": "Black School Bag (Nike)",
        "description": "Contains engineering textbooks, calculator, and a lab coat. Lost around the campus mosque after Jumat prayer.",
        "location": "Mosque Area",
        "date": "2026-11-20",
        "contact_name": "Mathew Umama",
        "contact_email": "1mathewumama@gmail.com",
        "contact_phone": "08031234567",
        "reporter_id": "U23CS1067",
        "security_personnel": "Mathew Umama",
        "status": "Active",
        "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=600&q=80",
        "created_at": "2026-11-20 14:30"
    },
    {
        "seeded": True,
        "id": 2,
        "item_type": "found",
        "category": "IDs & Cards",
        "title": "AFIT Student ID Card",
        "description": "ID Number: U23EE1084. Found on a concrete table near the food vendors at Bush Canteen.",
        "location": "Bush Canteen",
        "date": "2026-11-21",
        "contact_name": "Mathew Umama",
        "contact_email": "1mathewumama@gmail.com",
        "contact_phone": "08059876543",
        "reporter_id": "U23CS1067",
        "security_personnel": "Mathew Umama",
        "status": "Active",
        "image_url": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=600&q=80",
        "created_at": "2026-11-21 09:15"
    },
    {
        "seeded": True,
        "id": 3,
        "item_type": "found",
        "category": "IDs & Cards",
        "title": "Access Bank ATM Card",
        "description": "Found inside the card slot reader after transaction failed. Handed over to ICT security.",
        "location": "Front of ICT Center",
        "date": "2026-11-21",
        "contact_name": "Mathew Umama",
        "contact_email": "1mathewumama@gmail.com",
        "contact_phone": "08091122334",
        "reporter_id": "U23CS1067",
        "security_personnel": "Mathew Umama",
        "status": "Active",
        "image_url": "https://images.unsplash.com/photo-1563013544-824ae1b704d3?auto=format&fit=crop&w=600&q=80",
        "created_at": "2026-11-21 11:00"
    },
    {
        "seeded": True,
        "id": 4,
        "item_type": "lost",
        "category": "Electronics",
        "title": "Newage 20,000mAh Powerbank",
        "description": "Black powerbank with dual USB output. Left on a front bench in Alfa Hall during morning lectures.",
        "location": "Alfa Hall",
        "date": "2026-11-21",
        "contact_name": "Mathew Umama",
        "contact_email": "1mathewumama@gmail.com",
        "contact_phone": "08123344556",
        "reporter_id": "U23CS1067",
        "security_personnel": "Mathew Umama",
        "status": "Active",
        "image_url": "https://images.unsplash.com/photo-1609592424158-45c360875997?auto=format&fit=crop&w=600&q=80",
        "created_at": "2026-11-21 12:30"
    },
    {
        "seeded": True,
        "id": 5,
        "item_type": "found",
        "category": "Keys & Wallets",
        "title": "Leather Wallet with Cash & Cards",
        "description": "Brown leather wallet containing student ID, driver license, and ID cards. Found underneath a desk in Amao Hall.",
        "location": "Amao Hall",
        "date": "2026-11-20",
        "contact_name": "Mathew Umama",
        "contact_email": "1mathewumama@gmail.com",
        "contact_phone": "08034455667",
        "reporter_id": "U23CS1067",
        "security_personnel": "Mathew Umama",
        "status": "Active",
        "image_url": "https://images.unsplash.com/photo-1627123424574-724758594e93?auto=format&fit=crop&w=600&q=80",
        "created_at": "2026-11-20 16:45"
    },
    {
        "seeded": True,
        "id": 6,
        "item_type": "lost",
        "category": "Electronics",
        "title": "Oraimo Wireless Earbuds (Pods 3)",
        "description": "White charging case with one earbud missing or both inside. Lost around Amao Hall corridor during evening study.",
        "location": "Amao Hall",
        "date": "2026-11-21",
        "contact_name": "Mathew Umama",
        "contact_email": "1mathewumama@gmail.com",
        "contact_phone": "08189988776",
        "reporter_id": "U23CS1067",
        "security_personnel": "Mathew Umama",
        "status": "Active",
        "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=600&q=80",
        "created_at": "2026-11-21 18:20"
    },
    {
        "seeded": True,
        "id": 7,
        "item_type": "found",
        "category": "Electronics",
        "title": "Fast Type-C Phone Charger",
        "description": "White 65W charger block and braided cable left plugged into the wall socket in 200lvl Lecture Room.",
        "location": "200lvl LR",
        "date": "2026-11-21",
        "contact_name": "Mathew Umama",
        "contact_email": "1mathewumama@gmail.com",
        "contact_phone": "08021112233",
        "reporter_id": "U23CS1067",
        "security_personnel": "Mathew Umama",
        "status": "Active",
        "image_url": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=600&q=80",
        "created_at": "2026-11-21 13:10"
    },
    {
        "seeded": True,
        "id": 8,
        "item_type": "lost",
        "category": "Books & Notes",
        "title": "Hardcover Engineering Mathematics Textbook",
        "description": "Sticker on cover says 'Kaye & Wilson'. Contains handwritten notes inside. Lost in LR 201.",
        "location": "LR 201",
        "date": "2026-11-19",
        "contact_name": "Mathew Umama",
        "contact_email": "1mathewumama@gmail.com",
        "contact_phone": "08134455667",
        "reporter_id": "U23CS1067",
        "security_personnel": "Mathew Umama",
        "status": "Active",
        "image_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?auto=format&fit=crop&w=600&q=80",
        "created_at": "2026-11-19 10:00"
    },
    {
        "seeded": True,
        "id": 9,
        "item_type": "lost",
        "category": "Electronics",
        "title": "HP Pavilion Gaming Laptop",
        "description": "Black laptop with green backlit keyboard in a gray sleeve. Left on a study carrel on the 1st floor of the main library.",
        "location": "Library",
        "date": "2026-11-20",
        "contact_name": "Mathew Umama",
        "contact_email": "1mathewumama@gmail.com",
        "contact_phone": "08039998877",
        "reporter_id": "U23CS1067",
        "security_personnel": "Mathew Umama",
        "status": "Active",
        "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=600&q=80",
        "created_at": "2026-11-20 17:00"
    },
    {
        "seeded": True,
        "id": 10,
        "item_type": "found",
        "category": "Clothing & Wearables",
        "title": "Black Formal Cover Shoes",
        "description": "Size 43 leather cover shoes found neatly placed behind Alfa Hall near the exit door.",
        "location": "Back of Alfa Hall",
        "date": "2026-11-21",
        "contact_name": "Mathew Umama",
        "contact_email": "1mathewumama@gmail.com",
        "contact_phone": "08055667788",
        "reporter_id": "U23CS1067",
        "security_personnel": "Mathew Umama",
        "status": "Active",
        "image_url": "https://images.unsplash.com/photo-1533867617858-e7d97e0afd8b?auto=format&fit=crop&w=600&q=80",
        "created_at": "2026-11-21 08:30"
    },
    {
        "seeded": True,
        "id": 11,
        "item_type": "lost",
        "category": "Electronics",
        "title": "Itel S23 Ultra Smartphone",
        "description": "Glacial blue color with cracked tempered glass protector. Lost around Yisa Doko Hall during the student assembly.",
        "location": "Yisa Doko Hall",
        "date": "2026-11-20",
        "contact_name": "Mathew Umama",
        "contact_email": "1mathewumama@gmail.com",
        "contact_phone": "08145566778",
        "reporter_id": "U23CS1067",
        "security_personnel": "Mathew Umama",
        "status": "Active",
        "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=600&q=80",
        "created_at": "2026-11-20 13:45"
    }
]

item_counter = 12

# Anti-spam limit, chat store and lightweight persistence
MAX_ACTIVE_LOST_PER_REPORTER = 3
conversations = {}  # item_id -> list of messages
users_db = []       # signed-in users
DB_PATH = os.path.join(BASE_DIR, "db.json")

def save_state():
    """Persist items, users and conversations so data survives server restarts."""
    try:
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump({"items": items_db, "item_counter": item_counter,
                       "users": users_db, "conversations": {str(k): v for k, v in conversations.items()}}, f)
    except Exception:
        pass

def load_state():
    """Restore previously saved state, if any."""
    global items_db, item_counter, users_db, conversations
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data.get("items"), list) and data["items"]:
            items_db = data["items"]
            item_counter = data.get("item_counter", max(i["id"] for i in items_db) + 1)
            users_db = data.get("users", [])
            raw_conv = data.get("conversations", {})
            conv = {}
            for k, v in raw_conv.items():
                if ":" in k:  # new format "itemId:peerEmail"
                    conv[k] = v
                else:  # migrate old per-item threads to the reporter<->claimant thread
                    try:
                        iid = int(k)
                    except ValueError:
                        continue
                    item = next((x for x in items_db if x["id"] == iid), None)
                    if item:
                        ce = (item.get("claim_details") or {}).get("claimant_email", "")
                        if ce:
                            conv[f"{iid}:{ce}"] = v
            conversations = conv
    except Exception:
        pass

load_state()

class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str

def hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()

# ---- Input validation (data quality gate) ----
PHONE_RE = re.compile(r"^(\+234|0)[789]\d{9}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
NAME_RE = re.compile(r"^[A-Za-z][A-Za-z .'\-]{2,49}$")
MATRIC_RE = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z0-9/\-]{5,20}$")

def validate_contact_details(name: str, email: str, phone: str, matric: str):
    """Reject nonsense names, emails, phone numbers and matric/ID numbers."""
    if not NAME_RE.match(name.strip()):
        raise HTTPException(status_code=400, detail="Enter a valid full name (letters only, e.g. Mathew John).")
    if not EMAIL_RE.match(email.strip()):
        raise HTTPException(status_code=400, detail="Enter a valid email address (e.g. name@afit.edu.ng).")
    if not PHONE_RE.match(re.sub(r"[\s\-]", "", phone)):
        raise HTTPException(status_code=400, detail="Enter a valid phone number (e.g. 08031234567 or +2348031234567).")
    if not MATRIC_RE.match(matric.strip()):
        raise HTTPException(status_code=400, detail="Enter a valid matric/staff ID with letters and numbers (e.g. U23CS1067 or AFIT/2024/8812).")

class MessageCreate(BaseModel):
    sender_name: str
    sender_email: str = ""
    sender_role: str = "claimant"  # claimant | reporter | finder | security
    text: str
    peer_email: str = ""  # the other person in this 1-to-1 thread

class ItemCreate(BaseModel):
    title: str
    description: str
    category: str
    location: str
    date: str
    item_type: str
    contact_name: str
    contact_email: str
    contact_phone: str
    reporter_id: str
    security_personnel: str = ""
    image_url: Optional[str] = "https://images.unsplash.com/photo-1584438784894-089d6a62b8fa?auto=format&fit=crop&w=600&q=80"
    status: str = "Active"

@app.get("/api/items")
def get_items(item_type: Optional[str] = None, search: Optional[str] = None, status: Optional[str] = None, category: Optional[str] = None, location: Optional[str] = None, viewer_email: str = ""):
    results = items_db
    if item_type:
        results = [i for i in results if i["item_type"] == item_type]
    if status:
        results = [i for i in results if i["status"] == status]
    if category:
        results = [i for i in results if i["category"].lower() == category.lower()]
    if location:
        results = [i for i in results if location.lower() in i["location"].lower()]
    if search:
        s = search.lower()
        results = [i for i in results if s in i["title"].lower() or s in i["description"].lower() or s in i["location"].lower() or s in i["category"].lower() or s in i["contact_name"].lower() or s in i["reporter_id"].lower() or s in i["security_personnel"].lower()]
    return [public_item(i, viewer_email) for i in results]

# ---- Privacy: strip private fields based on who is asking ----
ALLOWED_IMAGE_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_IMAGE_BYTES = 5 * 1024 * 1024

def save_image_upload(upload, prefix):
    """Validate and store an uploaded image with a server-generated name (no path traversal)."""
    ext = os.path.splitext(os.path.basename(upload.filename or ""))[1].lower()
    if ext not in ALLOWED_IMAGE_EXT:
        raise HTTPException(status_code=400, detail="Only image files (jpg, jpeg, png, gif, webp) are allowed.")
    upload.file.seek(0, os.SEEK_END)
    size = upload.file.tell()
    upload.file.seek(0)
    if size > MAX_IMAGE_BYTES:
        raise HTTPException(status_code=400, detail="Image too large (max 5 MB).")
    filename = f"{prefix}_{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload.file, buffer)
    return f"/static/uploads/{filename}"

def public_item(item, viewer_email=""):
    """Copy of an item for public listings: contact details, claim proof and finder contacts
    are only included for the reporter, the active claimant, or a finder on that item."""
    viewer = (viewer_email or "").strip().lower()
    reporter = item["contact_email"].strip().lower()
    claimant = (item.get("claim_details") or {}).get("claimant_email", "").strip().lower()
    finder_emails = {fr["finder_email"].strip().lower() for fr in item.get("found_reports", [])}
    is_reporter = viewer == reporter
    is_claimant = bool(claimant) and viewer == claimant
    is_finder = viewer in finder_emails
    pub = {k: v for k, v in item.items()
           if k not in ("contact_email", "contact_phone", "claim_details", "found_reports",
                        "rejected_claimants", "seeded")}
    if is_reporter or is_claimant or is_finder:
        pub["contact_email"] = item["contact_email"]
        pub["contact_phone"] = item["contact_phone"]
    pub["viewer_is_reporter"] = is_reporter
    pub["viewer_is_claimant"] = is_claimant and item["status"] == "Claim Requested"
    pub["viewer_is_finder"] = is_finder
    pub["viewer_is_rejected"] = viewer in {e.strip().lower() for e in item.get("rejected_claimants", [])}
    pub["found_reports_count"] = len(item.get("found_reports", []))
    if is_reporter:
        pub["disputes"] = item.get("disputes", [])
        if item.get("claim_details"):
            pub["active_claimant_email"] = claimant
    else:
        # third parties see dispute reports without the disputer's email
        pub["disputes"] = [{k: v for k, v in d.items() if k != "email"} for d in item.get("disputes", [])]
    return pub

@app.get("/api/items/similar")
def similar_items(title: str = "", category: str = ""):
    """Fuzzy-match existing reports so duplicates surface before a new report is submitted."""
    STOP = {"a", "an", "the", "of", "and", "with", "for", "in", "on", "at", "my", "is", "it", "to", "was"}
    words = set(w for w in re.findall(r"[a-z0-9]+", title.lower()) if w not in STOP and len(w) > 2)
    if not words:
        return []
    scored = []
    for i in items_db:
        text = f"{i['title']} {i['description']} {i['category']} {i['location']}".lower()
        tokens = set(re.findall(r"[a-z0-9]+", text))
        overlap = sum(1 for w in words if w in tokens)
        score = overlap / len(words)
        if score >= 0.34:
            scored.append((score, i))
    scored.sort(key=lambda x: -x[0])
    return [{"id": i["id"], "title": i["title"], "item_type": i["item_type"], "status": i["status"],
             "location": i["location"], "date": i["date"], "image_url": i["image_url"], "score": round(s, 2)}
            for s, i in scored[:4]]

@app.post("/api/items")
def create_item(
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    location: str = Form(...),
    date: str = Form(...),
    item_type: str = Form(...),
    contact_name: str = Form(...),
    contact_email: str = Form(...),
    contact_phone: str = Form(...),
    reporter_id: str = Form(...),
    security_personnel: str = Form(""),
    preferred_contact: str = Form("both"),
    custody: str = Form("security"),
    image: Optional[UploadFile] = File(None)
):
    global item_counter

    validate_contact_details(contact_name, contact_email, contact_phone, reporter_id)

    # Found items must say who holds them; lost reporters are the owner, so no handover officer is needed
    if item_type == "found" and not security_personnel.strip():
        raise HTTPException(status_code=400, detail="Found items must specify who the item was handed to or reported to.")

    # Anti-spam: limit active lost reports per reporter ID (portal submissions only)
    if item_type == "lost":
        active_lost = [x for x in items_db if x["item_type"] == "lost"
                       and not x.get("seeded")
                       and x["reporter_id"].strip().lower() == reporter_id.strip().lower()
                       and x["status"] == "Active"]
        if len(active_lost) >= MAX_ACTIVE_LOST_PER_REPORTER:
            raise HTTPException(status_code=429, detail=f"Report limit reached: you already have {MAX_ACTIVE_LOST_PER_REPORTER} active lost-item reports under ID {reporter_id}. An item must be returned or removed before another report is accepted.")

    image_url = "https://images.unsplash.com/photo-1584438784894-089d6a62b8fa?auto=format&fit=crop&w=600&q=80"

    if image and image.filename:
        image_url = save_image_upload(image, f"item{item_counter}")

    new_item = {
        "id": item_counter,
        "item_type": item_type,
        "category": category,
        "title": title,
        "description": description,
        "location": location,
        "date": date,
        "contact_name": contact_name,
        "contact_email": contact_email,
        "contact_phone": contact_phone,
        "reporter_id": reporter_id,
        "security_personnel": security_personnel,
        "preferred_contact": preferred_contact,
        "custody": custody if item_type == "found" else None,
        "status": "Active",
        "image_url": image_url,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    items_db.append(new_item)
    item_counter += 1
    save_state()
    return new_item

@app.post("/api/signup")
def signup(req: SignupRequest):
    """Register a new user in the stored user registry (persisted to disk)."""
    email = req.email.strip().lower()
    name = req.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Your full name is required.")
    if "@" not in email or "." not in email:
        raise HTTPException(status_code=400, detail="Please enter a valid email address.")
    if len(req.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters.")
    if any(u["email"] == email for u in users_db):
        raise HTTPException(status_code=400, detail="An account with this email already exists. Please sign in.")
    salt = secrets.token_hex(16)
    user = {
        "id": len(users_db) + 1,
        "email": email,
        "name": name,
        "salt": salt,
        "password_hash": hash_password(req.password, salt),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    users_db.append(user)
    save_state()
    return {"id": user["id"], "email": user["email"], "name": user["name"]}

@app.post("/api/login")
def login(req: LoginRequest):
    """Verify credentials against the stored user registry."""
    email = req.email.strip().lower()
    user = next((u for u in users_db if u["email"] == email), None)
    if user is None:
        raise HTTPException(status_code=404, detail="No account with this email. Please sign up first.")
    if user.get("password_hash") != hash_password(req.password, user.get("salt", "")):
        raise HTTPException(status_code=401, detail="Incorrect email or password.")
    return {"id": user["id"], "email": user["email"], "name": user["name"]}

@app.post("/api/items/{item_id}/claim")
def verify_and_claim(
    item_id: int,
    claimant_name: str = Form(...),
    claimant_id: str = Form(...),
    contact_phone: str = Form(...),
    claimant_email: str = Form(...),
    proof_description: str = Form(...),
    proof_image: Optional[UploadFile] = File(None)
):
    for i in items_db:
        if i["id"] == item_id:
            if i["status"] != "Active":
                raise HTTPException(status_code=400, detail="This item already has an active claim in progress.")
            if claimant_email.strip().lower() == i["contact_email"].strip().lower():
                raise HTTPException(status_code=400, detail="You cannot claim an item you reported yourself.")
            if claimant_email.strip().lower() in [e.strip().lower() for e in i.get("rejected_claimants", [])]:
                raise HTTPException(status_code=403, detail="Your previous claim for this item was rejected. You cannot claim it again.")
            validate_contact_details(claimant_name, claimant_email, contact_phone, claimant_id)
            proof_image_url = None
            if proof_image and proof_image.filename:
                proof_image_url = save_image_upload(proof_image, f"claim{item_id}")
            i["status"] = "Claim Requested"
            i["claim_details"] = {
                "claimant_name": claimant_name,
                "claimant_id": claimant_id,
                "contact_phone": contact_phone,
                "claimant_email": claimant_email.strip().lower(),
                "proof_description": proof_description,
                "proof_image_url": proof_image_url,
            }
            save_state()
            return {"message": "Claim request submitted. Contact the reporter by email or in-app chat to arrange the return. The item shows as Claimed/Returned only after the return is confirmed.", "item": i}
    raise HTTPException(status_code=404, detail="Item not found")

class ClaimUpdate(BaseModel):
    claimant_name: str
    claimant_id: str
    contact_phone: str
    claimant_email: str
    proof_description: str

@app.put("/api/items/{item_id}/claim")
def update_claim(item_id: int, upd: ClaimUpdate):
    """The claimant can edit their claim details while the item awaits handover."""
    for i in items_db:
        if i["id"] == item_id:
            if i["status"] != "Claim Requested":
                raise HTTPException(status_code=400, detail="There is no active claim to edit on this item.")
            details = i.get("claim_details") or {}
            if upd.claimant_email.strip().lower() != details.get("claimant_email", ""):
                raise HTTPException(status_code=403, detail="Only the claimant who submitted this claim can edit it.")
            validate_contact_details(upd.claimant_name, upd.claimant_email, upd.contact_phone, upd.claimant_id)
            details.update({
                "claimant_name": upd.claimant_name,
                "claimant_id": upd.claimant_id,
                "contact_phone": upd.contact_phone,
                "claimant_email": upd.claimant_email.strip().lower(),
                "proof_description": upd.proof_description,
            })
            i["claim_details"] = details
            save_state()
            return {"message": "Claim details updated.", "item": i}
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/api/items/{item_id}")
def delete_item(item_id: int, reporter_email: str = ""):
    global items_db
    for i in items_db:
        if i["id"] == item_id:
            if reporter_email.strip().lower() != i["contact_email"].strip().lower():
                raise HTTPException(status_code=403, detail="Only the person who reported this item can remove it.")
            items_db = [x for x in items_db if x["id"] != item_id]
            for k in [k for k in conversations if k == item_id or k.startswith(f"{item_id}:")]:
                conversations.pop(k, None)
            save_state()
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

class RejectClaimRequest(BaseModel):
    reporter_email: str

@app.put("/api/items/{item_id}")
def update_item(
    item_id: int,
    reporter_email: str = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    location: str = Form(...),
    date: str = Form(...),
    preferred_contact: str = Form("both"),
    security_personnel: str = Form(""),
    contact_name: str = Form(...),
    contact_phone: str = Form(...),
    reporter_id: str = Form(...),
    custody: str = Form(""),
    image: Optional[UploadFile] = File(None),
):
    """Reporter edits every detail of their own report while it is still Active.
    The contact email is the ownership identity and is intentionally not editable."""
    for i in items_db:
        if i["id"] == item_id:
            if reporter_email.strip().lower() != i["contact_email"].strip().lower():
                raise HTTPException(status_code=403, detail="Only the person who reported this item can edit it.")
            if i["status"] != "Active":
                raise HTTPException(status_code=400, detail="Only active reports can be edited.")
            title = title.strip()
            description = description.strip()
            if not (3 <= len(title) <= 120):
                raise HTTPException(status_code=400, detail="Title must be between 3 and 120 characters.")
            if not (10 <= len(description) <= 1000):
                raise HTTPException(status_code=400, detail="Description must be between 10 and 1000 characters.")
            if not category.strip() or not location.strip():
                raise HTTPException(status_code=400, detail="Category and location are required.")
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", date.strip()):
                raise HTTPException(status_code=400, detail="Enter a valid date (YYYY-MM-DD).")
            if preferred_contact not in ("email", "phone", "both"):
                raise HTTPException(status_code=400, detail="Invalid contact preference.")
            validate_contact_details(contact_name, i["contact_email"], contact_phone, reporter_id)
            if image and image.filename:
                i["image_url"] = save_image_upload(image, f"item{item_id}")
            i.update({
                "title": title,
                "description": description,
                "category": category.strip()[:80],
                "location": location.strip()[:80],
                "date": date.strip(),
                "preferred_contact": preferred_contact,
                "security_personnel": security_personnel.strip()[:80],
                "contact_name": contact_name.strip()[:80],
                "contact_phone": contact_phone.strip(),
                "reporter_id": reporter_id.strip().upper(),
            })
            if i["item_type"] == "found" and custody in ("security", "finder"):
                i["custody"] = custody
            save_state()
            return {"message": "Report updated.", "item": i}
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/api/items/{item_id}/confirm-return")
def confirm_return(item_id: int, req: RejectClaimRequest):
    for i in items_db:
        if i["id"] == item_id:
            if req.reporter_email.strip().lower() != i["contact_email"].strip().lower():
                raise HTTPException(status_code=403, detail="Only the reporter can confirm the return.")
            if i["status"] != "Claim Requested":
                raise HTTPException(status_code=400, detail="Return can only be confirmed for items with an active claim request.")
            i["status"] = "Claimed/Returned"
            i["returned_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_state()
            return {"message": "Return confirmed. The item has been handed back to its owner.", "item": i}
    raise HTTPException(status_code=404, detail="Item not found")

class DisputeRequest(BaseModel):
    name: str
    email: str
    message: str

@app.get("/api/items/{item_id}/finders")
def get_finders(item_id: int, reporter_email: str = ""):
    """Reporter-only: full finder responses with contact details."""
    item = next((i for i in items_db if i["id"] == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if reporter_email.strip().lower() != item["contact_email"].strip().lower():
        raise HTTPException(status_code=403, detail="Only the reporter can view finder responses.")
    return item.get("found_reports", [])

@app.get("/api/items/{item_id}/claim")
def get_claim(item_id: int, claimant_email: str = ""):
    """Claimant-only: their own claim details (for viewing/editing)."""
    item = next((i for i in items_db if i["id"] == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    details = item.get("claim_details") or {}
    if claimant_email.strip().lower() != details.get("claimant_email", ""):
        raise HTTPException(status_code=403, detail="Only the claimant who submitted this claim can view it.")
    return details

@app.post("/api/items/{item_id}/dispute")
def report_dispute(item_id: int, req: DisputeRequest):
    """A third party reports a claim they believe is wrong; the reporter is prompted to verify."""
    for i in items_db:
        if i["id"] == item_id:
            if i["status"] != "Claim Requested":
                raise HTTPException(status_code=400, detail="Disputes can only be raised on items with a claim in progress.")
            message = req.message.strip()
            if not message:
                raise HTTPException(status_code=400, detail="Please describe the issue with this claim.")
            disputes = i.setdefault("disputes", [])
            if len(disputes) >= 20:
                raise HTTPException(status_code=429, detail="Too many dispute reports on this item.")
            disputes.append({
                "name": req.name.strip()[:80],
                "email": req.email.strip().lower(),
                "message": message[:1000],
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })
            save_state()
            return {"message": "Report received. The reporter and the security desk will verify and contact you after review.", "disputes": len(disputes)}
    raise HTTPException(status_code=404, detail="Item not found")

class FoundReportRequest(BaseModel):
    finder_name: str
    finder_email: str
    finder_phone: str
    finder_id: str
    location_found: str
    message: str = ""

@app.post("/api/items/{item_id}/found-report")
def found_report(item_id: int, req: FoundReportRequest):
    """A finder responds to a LOST report: light-weight contact request, no ownership quiz."""
    item = next((i for i in items_db if i["id"] == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if item["item_type"] != "lost":
        raise HTTPException(status_code=400, detail="Finder responses apply to lost item reports. Found items use the claim flow.")
    if item["status"] != "Active":
        raise HTTPException(status_code=400, detail="This item is not open for finder responses right now.")
    if req.finder_email.strip().lower() == item["contact_email"].strip().lower():
        raise HTTPException(status_code=400, detail="You reported this item yourself.")
    validate_contact_details(req.finder_name, req.finder_email, req.finder_phone, req.finder_id)
    reports = item.setdefault("found_reports", [])
    if len(reports) >= 20:
        raise HTTPException(status_code=429, detail="Too many finder responses on this item.")
    if any(r["finder_email"].strip().lower() == req.finder_email.strip().lower() for r in reports):
        raise HTTPException(status_code=400, detail="You have already responded to this item. Use the chat instead.")
    reports.append({
        "finder_name": req.finder_name.strip()[:80],
        "finder_email": req.finder_email.strip().lower(),
        "finder_phone": req.finder_phone.strip(),
        "finder_id": req.finder_id.strip().upper(),
        "location_found": req.location_found.strip()[:120],
        "message": req.message.strip()[:500],
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    save_state()
    return {"message": "Response sent. The owner has been notified and can now chat with you directly.", "item": item}

class DisputeResolveRequest(BaseModel):
    reporter_email: str
    action: str  # "uphold" | "dismiss"

@app.post("/api/items/{item_id}/disputes/{dispute_index}/resolve")
def resolve_dispute(item_id: int, dispute_index: int, req: DisputeResolveRequest):
    """Reporter resolves a dispute: uphold it (reject the wrong claim) or dismiss it."""
    for i in items_db:
        if i["id"] == item_id:
            if req.reporter_email.strip().lower() != i["contact_email"].strip().lower():
                raise HTTPException(status_code=403, detail="Only the reporter can resolve disputes on this item.")
            disputes = i.get("disputes", [])
            if dispute_index < 0 or dispute_index >= len(disputes):
                raise HTTPException(status_code=404, detail="Dispute not found.")
            if disputes[dispute_index].get("status"):
                raise HTTPException(status_code=400, detail="This dispute has already been resolved.")
            if req.action == "uphold":
                if i["status"] != "Claim Requested":
                    raise HTTPException(status_code=400, detail="The claim has already been resolved.")
                claimant_email = (i.get("claim_details") or {}).get("claimant_email", "")
                if claimant_email:
                    i.setdefault("rejected_claimants", []).append(claimant_email)
                i.pop("claim_details", {})
                i["status"] = "Active"
                disputes[dispute_index]["status"] = "upheld"
                message = "Dispute upheld: the claim was rejected and the item is Active again for the rightful owner."
            elif req.action == "dismiss":
                disputes[dispute_index]["status"] = "dismissed"
                message = "Dispute dismissed. The current claim stands."
            else:
                raise HTTPException(status_code=400, detail="Invalid action. Use uphold or dismiss.")
            disputes[dispute_index]["resolved_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_state()
            return {"message": message, "item": i}
    raise HTTPException(status_code=404, detail="Item not found")

class MarkFoundRequest(BaseModel):
    reporter_email: str
    finder_email: str = ""  # optional: credit the finder whose response led to the return

@app.post("/api/items/{item_id}/mark-found")
def mark_found(item_id: int, req: MarkFoundRequest):
    """Owner of a lost item marks it as recovered/reunited, optionally via a specific finder."""
    for i in items_db:
        if i["id"] == item_id:
            if req.reporter_email.strip().lower() != i["contact_email"].strip().lower():
                raise HTTPException(status_code=403, detail="Only the reporter can mark their item as found.")
            if i["item_type"] != "lost":
                raise HTTPException(status_code=400, detail="Only lost item reports can be marked as found.")
            if i["status"] != "Active":
                raise HTTPException(status_code=400, detail="This item is already marked as returned.")
            i["status"] = "Claimed/Returned"
            i["resolved_via"] = "marked-found"
            if req.finder_email.strip():
                finder = next((f for f in i.get("found_reports", [])
                               if f["finder_email"].strip().lower() == req.finder_email.strip().lower()), None)
                if finder:
                    i["resolved_via"] = f"Returned by {finder['finder_name']}"
            save_state()
            return {"message": "Great news! Your item has been marked as found and returned.", "item": i}
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/api/items/{item_id}/close-report")
def close_report(item_id: int, req: RejectClaimRequest):
    """Reporter closes/withdraws their own report (e.g. found it themselves, no longer missing)."""
    for i in items_db:
        if i["id"] == item_id:
            if req.reporter_email.strip().lower() != i["contact_email"].strip().lower():
                raise HTTPException(status_code=403, detail="Only the reporter can close their report.")
            if i["status"] != "Active":
                raise HTTPException(status_code=400, detail="This report is already resolved.")
            i["status"] = "Closed"
            i["resolved_via"] = "closed-by-reporter"
            save_state()
            return {"message": "Report closed. It no longer appears as active on the portal.", "item": i}
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/api/items/{item_id}/reject-claim")
def reject_claim(item_id: int, req: RejectClaimRequest):
    """Reporter rejects a claim request: the item falls back to Active (unclaimed)."""
    for i in items_db:
        if i["id"] == item_id:
            if i["status"] != "Claim Requested":
                raise HTTPException(status_code=400, detail="Only items with an active claim request can be rejected.")
            if req.reporter_email.strip().lower() != i["contact_email"].strip().lower():
                raise HTTPException(status_code=403, detail="Only the reporter can reject a claim request.")
            rejected = i.pop("claim_details", {})
            claimant_email = (rejected or {}).get("claimant_email", "")
            if claimant_email:
                i.setdefault("rejected_claimants", []).append(claimant_email)
            i["status"] = "Active"
            i["last_rejected_claimant"] = rejected.get("claimant_name", "") if rejected else ""
            save_state()
            return {"message": "Claim rejected. The item is Active again and can be claimed by the rightful owner.", "item": i}
    raise HTTPException(status_code=404, detail="Item not found")

def conversation_participants(item):
    """Emails allowed in this item's chats: reporter, claimant, and finders who reported it."""
    emails = {item["contact_email"].strip().lower()}
    claimant_email = (item.get("claim_details") or {}).get("claimant_email", "")
    if claimant_email:
        emails.add(claimant_email.strip().lower())
    for fr in item.get("found_reports", []):
        emails.add(fr["finder_email"].strip().lower())
    return emails

def resolve_thread(item, user_email, peer_email):
    """Resolve the 1-to-1 thread 'itemId:partner' between the reporter and one claimant/finder.
    The partner (non-reporter party) identifies the thread, so multiple finders never share one."""
    user = (user_email or "").strip().lower()
    peer = (peer_email or "").strip().lower()
    reporter = item["contact_email"].strip().lower()
    claimant = (item.get("claim_details") or {}).get("claimant_email", "").strip().lower()
    finders = {fr["finder_email"].strip().lower() for fr in item.get("found_reports", [])}
    others = ({claimant} | finders) - {reporter}
    if peer in others:
        partner = peer
    elif user in others:
        partner = user
    else:
        return None
    if user not in (reporter, partner):
        return None
    return f"{item['id']}:{partner}"

@app.get("/api/items/{item_id}/messages")
def get_messages(item_id: int, user_email: str = "", peer: str = ""):
    item = next((i for i in items_db if i["id"] == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    key = resolve_thread(item, user_email, peer)
    if key is None:
        raise HTTPException(status_code=403, detail="This chat is private between the reporter and the person who responded.")
    return conversations.get(key, [])

@app.post("/api/items/{item_id}/messages")
def post_message(item_id: int, msg: MessageCreate):
    item = next((i for i in items_db if i["id"] == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    sender_email = (msg.sender_email or "").strip().lower()
    key = resolve_thread(item, sender_email, msg.peer_email)
    if key is None:
        raise HTTPException(status_code=403, detail="This chat is private between the reporter and the person who responded.")
    text = msg.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    if len(text) > 1000:
        raise HTTPException(status_code=400, detail="Message too long (max 1000 characters)")
    convo = conversations.setdefault(key, [])
    if len(convo) >= 200:
        raise HTTPException(status_code=429, detail="Message limit reached for this conversation.")
    convo.append({
        "sender_name": msg.sender_name.strip()[:80],
        "sender_email": sender_email,
        "sender_role": msg.sender_role,
        "text": text,
        "time": datetime.now().strftime("%H:%M")
    })
    save_state()
    return {"ok": True}

@app.get("/api/chat/unread")
def chat_unread(user_email: str = ""):
    """Message counts per conversation for the given user (participants only)."""
    email = user_email.strip().lower()
    if not email:
        return {}
    counts = {}
    for key, msgs in conversations.items():
        item_id_str, peer = key.split(":", 1)
        item = next((x for x in items_db if x["id"] == int(item_id_str)), None)
        if not item:
            continue
        if email in (item["contact_email"].strip().lower(), peer.strip().lower()):
            counts[key] = len(msgs)
    return counts

@app.get("/")
def read_root():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))
