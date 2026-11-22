# AFIT Lost & Found Portal (Project SP-014)

**Institution:** Air Force Institute of Technology (AFIT)  
**Domain:** Security & Property Recovery  
**Level:** Intermediate Software Engineering Project  
**Tech Stack:** Python 3 / FastAPI + Modern Responsive UI (Tailwind CSS, Plus Jakarta Sans, File Upload Handling)

---

## 📖 Overview
The **AFIT Lost & Found Portal** is an institutional campus security and property recovery system designed for cadets, students, academic staff, and campus provost security personnel to report, log, verify, and recover lost or found items across all campus zones.

## 🚀 Key Features & Capabilities
1. **Full AFIT Campus Location Support**:
   - Mosque Area
   - Bush Canteen
   - Front of ICT Center
   - Alfa Hall & Back of Alfa Hall
   - Amao Hall
   - 200lvl Lecture Room
   - LR 201
   - Main Library
   - Yisa Doko Hall
   - Main Gate / Security Post

2. **Preloaded Real-World Campus Items**:
   - Black School Bag (Mosque Area)
   - Student ID Card `U23EE1084` (Bush Canteen)
   - ATM Card (Front of ICT Center)
   - Powerbank (Alfa Hall)
   - Leather Wallet (Amao Hall)
   - Earbuds / Pods (Amao Hall)
   - Fast Charger (200lvl LR)
   - Hardcover Textbook (LR 201)
   - Laptop (Main Library)
   - Cover Shoes (Back of Alfa Hall)
   - Itel S23 Ultra Smartphone (Yisa Doko Hall)

3. **High-Resolution Photography & File Uploads**:
   - Each card displays curated property imagery or user-uploaded photos via multipart file upload support.

4. **Institutional Security Verification**:
   - Designates specific campus security personnel or hall wardens to report to (e.g. *WO 1 Bala / Campus Provost*, *Lt. Commander Musa*, *Hall Wardens*).
   - Multi-step claim verification modal requiring:
     - Claimant Full Name
     - Student / Matriculation Number
     - Contact Phone
     - Proof of Ownership (unique identifiers, marks, or serial numbers).

5. **Security Protocols & Compliance Section**:
   - Integrated Institutional Guidelines for proof of ownership, designated security handovers, and unclaimed property policies.

---

## 🛠️ How to Run Locally

1. **Install dependencies:**
   ```powershell
   cd "C:\Users\HP PC\claude\campus_lost_and_found"
   pip install -r requirements.txt
   ```

2. **Start the FastAPI application:**
   ```powershell
   python -m uvicorn main:app --reload --port 8000
   ```

3. **Open in your browser:**  
   Navigate to [http://localhost:8000](http://localhost:8000)
