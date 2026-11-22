# Week 4 — UML Model Set (SP-014)

**Deliverables:** use case, class, sequence (main flow) and activity diagrams. **Marks: 8**

All diagrams are in Mermaid, so they render directly on GitHub and in VS Code.

## 1. Use case diagram

```mermaid
graph TB
    subgraph AFIT Lost and Found Portal
        UC1([Report lost item])
        UC2([Report found item])
        UC3([Search / filter items])
        UC4([Claim found item])
        UC5([Respond 'I found this item'])
        UC6([Chat privately])
        UC7([Confirm return])
        UC8([Reject claim])
        UC9([Resolve dispute])
        UC10([File dispute])
        UC11([Edit / close / mark-found own report])
        UC12([Sign up / sign in])
        UC13([View finder responses])
    end
    Student([Student])
    Finder([Finder])
    Reporter([Reporter])
    ThirdParty([Third party])

    Student --> UC1 & UC3 & UC4 & UC12
    Finder --> UC2 & UC3 & UC5 & UC12
    Reporter --> UC3 & UC6 & UC7 & UC8 & UC9 & UC11 & UC13 & UC12
    ThirdParty --> UC3 & UC10
    UC4 -.->|includes| UC12
    UC5 -.->|includes| UC12
    UC6 -.->|includes| UC12
    UC11 -.->|includes| UC12
```

One thing worth pointing out to anyone reading this: the *Reporter* actor is not a separate
kind of user — it's any student once they've filed a report. Modelling it as its own actor
made the diagram much clearer than trying to draw every permission on the Student actor.

## 2. Class diagram (domain + boundary entities)

```mermaid
classDiagram
    class Item {
        +int id
        +str item_type
        +str category
        +str title
        +str description
        +str location
        +str date
        +str contact_name
        +str contact_email
        +str contact_phone
        +str reporter_id
        +str security_personnel
        +str preferred_contact
        +str custody
        +str status
        +str image_url
        +str created_at
        +markFound()
        +close()
    }
    class ClaimDetails {
        +str claimant_name
        +str claimant_id
        +str contact_phone
        +str claimant_email
        +str proof_description
        +str proof_image_url
    }
    class FoundReport {
        +str finder_name
        +str finder_email
        +str finder_phone
        +str finder_id
        +str location_found
        +str message
        +str time
    }
    class Dispute {
        +str name
        +str email
        +str message
        +str time
        +str status
        +str resolved_at
    }
    class Conversation {
        +str key
        +List messages
        +addMessage()
    }
    class Message {
        +str sender_name
        +str sender_email
        +str sender_role
        +str text
        +str time
    }
    class User {
        +int id
        +str email
        +str name
        +str salt
        +str password_hash
        +verifyPassword()
    }
    class PortalAPI {
        +getItems(viewer)
        +createItem()
        +claimItem()
        +foundReport()
        +resolveDispute()
        +markFound()
        +closeReport()
        +getMessages()
        +postMessage()
    }
    PortalAPI "1" o-- "0..*" Item : manages
    Item "1" *-- "0..1" ClaimDetails
    Item "1" *-- "0..*" FoundReport
    Item "1" *-- "0..*" Dispute
    Conversation "1" *-- "0..*" Message
    PortalAPI "1" o-- "0..*" Conversation
    PortalAPI "1" o-- "0..*" User
```

The status lifecycle on `Item` is the heart of the model:
`Active → Claim Requested → (Claimed/Returned | Active)`. A lost item can also be resolved
directly by its reporter: `Active → Claimed/Returned` (marked found) or `Active → Closed`.

## 3. Sequence diagram — the main flow (claiming and returning a found item)

I picked this as "the" main flow because it's the one that exercises the most of the system:
two users, a state transition, validation, chat and a permission check all in one path.

```mermaid
sequenceDiagram
    actor Claimant
    actor Reporter
    participant UI as PWA (app.js)
    participant API as FastAPI (main.py)
    participant DB as db.json

    Reporter->>UI: submit found-item report
    UI->>API: POST /api/items (form + photo)
    API->>API: validate name/email/phone/matric
    API->>DB: save_state()
    API-->>UI: item created (status Active)

    Claimant->>UI: open claim form, answer proof questions
    UI->>API: POST /api/items/{id}/claim
    API->>API: checks: Active? not self-claim? not rejected before? valid details?
    API->>DB: save claim_details, status = Claim Requested
    API-->>UI: claim submitted

    Claimant->>API: POST /api/items/{id}/messages (private chat)
    API->>DB: append to thread "id:claimant_email"
    Reporter->>API: GET /api/chat/unread
    API-->>Reporter: unread dot for thread

    Reporter->>API: POST /api/items/{id}/confirm-return
    API->>DB: status = Claimed/Returned, returned_at set
    API-->>Reporter: "Return confirmed"
    Note over Claimant,Reporter: Reject path: POST .../reject-claim → status Active, claimant banned for this item
```

## 4. Sequence diagram — the finder response flow (lost items)

The mirror flow for lost reports, where the roles are reversed — now the *finder* comes to
the owner, and the owner holds all the decision power:

```mermaid
sequenceDiagram
    actor Finder
    actor Owner
    participant API as FastAPI (main.py)

    Finder->>API: POST /api/items/{id}/found-report
    API->>API: lost item? Active? not self? not duplicate? valid details?
    API-->>Finder: response recorded
    Owner->>API: GET /api/items/{id}/finders (reporter-only)
    API-->>Owner: list of finders with contact details
    Owner->>API: POST mark-found (finder_email credited)
    API-->>Owner: status = Claimed/Returned, "Returned by <finder>"
```

## 5. Activity diagram — report submission with validation and the duplicate warning

```mermaid
flowchart TD
    A[Open report form] --> B{Lost or found?}
    B -->|lost| C[Show lost fields - no handover officer required]
    B -->|found| D[Show found fields - handover officer required]
    C --> E[Fill title/description/category/location/date]
    D --> E
    E --> F[Type title]
    F --> G{Similar reports found?}
    G -->|yes| H[Show 'possible matches' warning panel]
    G -->|no| I[Continue]
    H --> I
    I --> J[Submit]
    J --> K{Server validation passes?}
    K -->|no| L[Show field error, stay on form]
    L --> E
    K -->|yes| M{Lost report and 3 active already?}
    M -->|yes| N[Reject: report limit reached]
    M -->|no| O[Save item, status Active]
    O --> P[Browse grid refreshes]
```

Note the duplicate warning is deliberately *non-blocking* — it informs, it doesn't prevent.
Two people genuinely can lose the same model of phone in the same week.

## 6. Activity diagram — claim resolution with disputes

```mermaid
flowchart TD
    A[Claim submitted - status Claim Requested] --> B{Reporter reviews}
    B --> C{Ownership convincing?}
    C -->|yes| D[Confirm return - status Claimed/Returned]
    C -->|no| E[Reject claim - claimant banned, status Active]
    B --> F{Third party disputes claim?}
    F -->|yes| G[Dispute recorded - amber badge]
    G --> H{Reporter decision}
    H -->|uphold| E
    H -->|dismiss| I[Claim stands - dispute marked dismissed]
    D --> Z[Resolved]
    E --> Z
    I --> Z
```

## 7. What drawing these taught me

Two things I only noticed once I had to draw them. First, the claim flow and the finder
response flow are near-mirrors of each other — seeing that on paper is why I built them as
separate-but-symmetric features rather than forcing one form to do both jobs. Second, every
diagram kept funneling through the reporter as the decision-maker, which confirmed the
design instinct that the reporter (owner or holder) should always be the one who closes a
report. Neither of those was obvious to me in week 2.
