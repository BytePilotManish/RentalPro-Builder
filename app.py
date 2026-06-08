import os
import json
import uuid
import docx
import pythoncom
import win32com.client
from datetime import datetime
from fastapi import FastAPI, HTTPException, Body, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Import Database & Auth modules
from database import Base, engine, User, Agreement, get_db, SessionLocal
from auth import hash_password, verify_password, create_access_token, decode_access_token
from runtime_paths import resource_dir, data_dir
import updater

DEFAULT_CONDITIONS = [
    "This RENTAL AGREEMENT is for a period of {{LEASE_PERIOD}} from the date of execution of this agreement i.e., on {{LEASE_END_DATE}}.",
    "The OWNER has agreed to let out the said premises for a monthly rent of Rs.{{RENT_AMOUNT}} (Rupees {{RENT_AMOUNT_WORDS}} only)",
    "The TENANT has agreed to pay the rental amount on {{RENT_PAYMENT_DAY}} of every month.",
    "The TENANT has agreed to pay {{ESCALATION_RATE}} increase in the rent every {{LEASE_PERIOD_NUM}} months, over the previous monthly rent.",
    "The TENANT has paid Security deposited to the OWNER an amount of Rs {{DEPOSIT_AMOUNT}}/- (Rupees {{DEPOSIT_AMOUNT_WORDS}} only) by way of {{DEPOSIT_MODE}} as an advance deposit amount. The OWNER has agreed to refund the said amount without interest to the TENANT while vacating the rented premises. The TENANT has agreed for the same. The OWNER hereby acknowledges the receipt of the said amount from the tenant.",
    "The TENANT should use the rented premises for his Business Purpose Only, and not for any illegal trade or business and unlawful purpose like to endanger the building.",
    "The TENANT should pay the Electricity and water charges utilized for his own use as per the actual meter reading for the rented premises during the period of tenancy.",
    "The tenancy period may be renewed for further period of {{LEASE_PERIOD_NUM}} months by mutual agreement between the OWNER and TENANT on the terms and conditions to be specified at that time.",
    "The OWNER and TENANT have agreed that {{NOTICE_PERIOD}} prior notice on either side is required for the termination of the tenancy period."
]

app = FastAPI(title="Rental Agreement Generator Hub")

# Directory setup
# Read-only resources (shipped with the app / bundled into the .exe)
RESOURCE_DIR = resource_dir()
TEMPLATE_PATH = os.path.join(RESOURCE_DIR, "TEMPLATE.docx")
STATIC_DIR = os.path.join(RESOURCE_DIR, "frontend", "dist")

# Writable runtime data (generated documents) — kept out of the read-only bundle
OUTPUT_DIR = os.path.join(data_dir(), "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

# Security config
security = HTTPBearer()

# Auto Database creation & seeding
@app.on_event("startup")
def startup_db_seed():
    # Attempt to add master_conditions column dynamically (SQLite safe migration)
    try:
        with engine.begin() as conn:
            import sqlalchemy
            # Check if column already exists by inspecting user table
            conn.execute(sqlalchemy.text("ALTER TABLE users ADD COLUMN master_conditions TEXT"))
        print("[MIGRATION] Added master_conditions column to users table successfully.")
    except Exception as e:
        # Column likely already exists
        pass

    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            print("=== DATABASE SEEDING STARTED ===")
            # Seed users
            admin_user = User(
                email="admin@rentalpro.com",
                hashed_password=hash_password("admin123"),
                full_name="Admin User",
                master_conditions=json.dumps(DEFAULT_CONDITIONS)
            )
            tenant_user = User(
                email="tenant@rentalpro.com",
                hashed_password=hash_password("tenant123"),
                full_name="Tenant User",
                master_conditions=json.dumps(DEFAULT_CONDITIONS)
            )
            db.add(admin_user)
            db.add(tenant_user)
            db.commit()
            db.refresh(admin_user)
            
            # Default values for first agreement
            agreement_1_data = {
                "AGREEMENT_DATE": "01ST Day of this April 2026",
                "AGREEMENT_PLACE": "Bangalore",
                "OWNER_NAME": "Mr. MANOJ M & SANCHITHA C J",
                "OWNER_PARENT": "S/O T Mahesh",
                "OWNER_AGE": "45",
                "OWNER_ADDRESS": "No,99,100 C Near Sri Kalikamba Temple, ChowdeshwariNagar, , Laggere, Bengaluru- 560 058",
                "TENANT_NAME": "Mr. RAJUGOWDA",
                "TENANT_PARENT": "S/O Subbegowda",
                "TENANT_AGE": "47",
                "TENANT_ADDRESS": "No. 18, 3rd Cross, Rajeev Gandhi Nagar, Laggere, Bengaluru-560 058",
                "PREMISES_ADDRESS": "No.99 & 100C, Near Sri Kalikamba Temple Chowdeshwari Nagar, Laggere, Bengaluru- 560 058",
                "PREMISES_DESCRIPTION": "One RCC Roofed Shops, with rolling Shutter and electricity, Toilet and water facility",
                "BUSINESS_NAME": "J S TRADERS",
                "LEASE_PERIOD": "eleven months",
                "LEASE_PERIOD_NUM": "11",
                "LEASE_END_DATE": "25/02/2027",
                "RENT_AMOUNT": "10,500.00",
                "RENT_AMOUNT_WORDS": "Ten Thousand Five Hundred",
                "RENT_PAYMENT_DAY": "15th",
                "ESCALATION_RATE": "5%",
                "DEPOSIT_AMOUNT": "50,000",
                "DEPOSIT_AMOUNT_WORDS": "Fifty Thousand",
                "DEPOSIT_MODE": "cash",
                "NOTICE_PERIOD": "three months",
                "OWNER_SIG_NAMES": "MANOJ M AND SANCHITHA C J",
                "TENANT_SIG_NAMES": "RAJUGOWDA"
            }
            
            # Values for second agreement
            agreement_2_data = agreement_1_data.copy()
            agreement_2_data["OWNER_NAME"] = "Mrs. LATHA SHARMA"
            agreement_2_data["TENANT_NAME"] = "Mr. AMIT KUMAR"
            agreement_2_data["BUSINESS_NAME"] = "SHARMA GROCERIES"
            agreement_2_data["RENT_AMOUNT"] = "15,000.00"
            agreement_2_data["RENT_AMOUNT_WORDS"] = "Fifteen Thousand"
            agreement_2_data["DEPOSIT_AMOUNT"] = "80,000"
            agreement_2_data["DEPOSIT_AMOUNT_WORDS"] = "Eighty Thousand"
            
            # Add to DB
            ag1 = Agreement(
                user_id=admin_user.id,
                title="Laggere Commercial Shop - J S Traders",
                agreement_data=json.dumps(agreement_1_data)
            )
            ag2 = Agreement(
                user_id=admin_user.id,
                title="Commercial Premises Agreement - Sharma Groceries",
                agreement_data=json.dumps(agreement_2_data)
            )
            db.add(ag1)
            db.add(ag2)
            db.commit()
            print("=== DATABASE SEEDING COMPLETED ===")

        # Regenerate missing/null path physical files for all agreements in the DB
        all_agreements = db.query(Agreement).all()
        for ag in all_agreements:
            if not ag.docx_path or not ag.pdf_path or not os.path.exists(ag.docx_path) or not os.path.exists(ag.pdf_path):
                print(f"Regenerating missing physical files for Agreement ID {ag.id} ({ag.title})...")
                try:
                    data_dict = json.loads(ag.agreement_data)
                    unique_id = str(uuid.uuid4())[:8]
                    safe_title = "".join([c if c.isalnum() else "_" for c in ag.title])
                    docx_filename = f"agreement_{ag.user_id}_{safe_title}_{unique_id}.docx"
                    pdf_filename = f"agreement_{ag.user_id}_{safe_title}_{unique_id}.pdf"
                    
                    docx_path = os.path.join(OUTPUT_DIR, docx_filename)
                    pdf_path = os.path.join(OUTPUT_DIR, pdf_filename)
                    
                    doc = docx.Document(TEMPLATE_PATH)
                    style = doc.styles['Normal']
                    style.font.size = docx.shared.Pt(12)
                    style.font.name = 'Times New Roman'
                    
                    replace_placeholders(doc, data_dict)
                    doc.save(docx_path)
                    
                    success = docx_to_pdf(docx_path, pdf_path)
                    if success:
                        ag.docx_path = docx_path
                        ag.pdf_path = pdf_path
                        db.commit()
                        print(f"Successfully generated files for Agreement ID {ag.id}.")
                    else:
                        print(f"[WARNING] PDF conversion failed during startup regeneration for Agreement ID {ag.id}.")
                except Exception as ex:
                    print(f"[ERROR] Failed to regenerate files for Agreement ID {ag.id}: {ex}")
    except Exception as e:
        print(f"Seeding error: {e}")
    finally:
        db.close()

# Dependency: Get Current User via Bearer Token
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Session expired or invalid. Please log in again.")
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")
    return user

# Helper: Get Current User via Query String (for file downloads)
def get_current_user_query(token: str, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Session expired or invalid.")
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")
    return user

# Auth Request Schemas
class UserRegister(BaseModel):
    email: str
    password: str
    full_name: str

class UserLogin(BaseModel):
    email: str
    password: str

class AgreementData(BaseModel):
    AGREEMENT_DATE: str | None = ""
    AGREEMENT_PLACE: str | None = ""
    OWNER_NAME: str | None = ""
    OWNER_PARENT: str | None = ""
    OWNER_AGE: str | None = ""
    OWNER_ADDRESS: str | None = ""
    TENANT_NAME: str | None = ""
    TENANT_PARENT: str | None = ""
    TENANT_AGE: str | None = ""
    TENANT_ADDRESS: str | None = ""
    PREMISES_ADDRESS: str | None = ""
    PREMISES_DESCRIPTION: str | None = ""
    BUSINESS_NAME: str | None = ""
    LEASE_PERIOD: str | None = ""
    LEASE_PERIOD_NUM: str | None = ""
    LEASE_END_DATE: str | None = ""
    RENT_AMOUNT: str | None = ""
    RENT_AMOUNT_WORDS: str | None = ""
    RENT_PAYMENT_DAY: str | None = ""
    ESCALATION_RATE: str | None = ""
    DEPOSIT_AMOUNT: str | None = ""
    DEPOSIT_AMOUNT_WORDS: str | None = ""
    DEPOSIT_MODE: str | None = ""
    NOTICE_PERIOD: str | None = ""
    OWNER_SIG_NAMES: str | None = ""
    TENANT_SIG_NAMES: str | None = ""
    AGREEMENT_CONDITIONS: list[str] | None = []
    # Admin-only: service charge billed to the customer for preparing this document.
    # Not rendered in the document (no matching placeholder); used for earnings tracking.
    SERVICE_FEE: str | None = ""

class SaveAgreementPayload(BaseModel):
    id: int | None = None
    title: str
    data: AgreementData

# Helper to perform find-and-replace
def replace_placeholders(doc, data: dict):
    clauses = data.get("AGREEMENT_CONDITIONS", [])
    if isinstance(clauses, str):
        clauses = [c.strip() for c in clauses.split("\n") if c.strip()]

    # Pass 1: Replace {{AGREEMENT_CONDITIONS}} placeholder by inserting paragraphs
    for p in list(doc.paragraphs):
        if "{{AGREEMENT_CONDITIONS}}" in p.text:
            for idx, clause in enumerate(clauses):
                prefix = f"{idx + 1}. " if not clause.startswith(f"{idx + 1}.") else ""
                clause_text = f"{prefix}{clause}"
                
                new_p = p.insert_paragraph_before(clause_text)
                new_p.style = doc.styles['Normal']

                # Add breathing room between numbered clauses so they aren't congested
                pf = new_p.paragraph_format
                pf.line_spacing = 1.5
                pf.space_before = docx.shared.Pt(6)
                pf.space_after = docx.shared.Pt(6)

                # Ensure new_p contains at least one run and apply font styles
                if not new_p.runs:
                    new_p.add_run()
                for run in new_p.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = docx.shared.Pt(12)
            
            # Remove the placeholder paragraph
            p._element.getparent().remove(p._element)
            break

    # Pass 2: Replace standard placeholders in all paragraphs (including newly inserted conditions!)
    for p in doc.paragraphs:
        text_before = p.text
        for key, val in data.items():
            if key == "AGREEMENT_CONDITIONS":
                continue
            placeholder = f"{{{{{key}}}}}"
            if placeholder in text_before:
                for run in p.runs:
                    if placeholder in run.text:
                        run.text = run.text.replace(placeholder, str(val))
                        run.font.size = docx.shared.Pt(12)
                        run.font.name = 'Times New Roman'
                if placeholder in p.text:
                    p.text = p.text.replace(placeholder, str(val))
                    for run in p.runs:
                        run.font.size = docx.shared.Pt(12)
                        run.font.name = 'Times New Roman'
                    
    # Replace in tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in list(cell.paragraphs):
                    text_before = p.text
                    for key, val in data.items():
                        if key == "AGREEMENT_CONDITIONS":
                            continue
                        placeholder = f"{{{{{key}}}}}"
                        if placeholder in text_before:
                            for run in p.runs:
                                if placeholder in run.text:
                                    run.text = run.text.replace(placeholder, str(val))
                                    if run.font.size is None:
                                        run.font.size = docx.shared.Pt(12)
                                    if run.font.name is None:
                                        run.font.name = 'Times New Roman'
                            if placeholder in p.text:
                                p.text = p.text.replace(placeholder, str(val))
                                for run in p.runs:
                                    run.font.size = docx.shared.Pt(12)
                                    run.font.name = 'Times New Roman'

# Helper to convert docx to pdf
def docx_to_pdf(docx_path, pdf_path):
    word = None
    try:
        pythoncom.CoInitialize()
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        word.DisplayAlerts = False
        
        abs_docx = os.path.abspath(docx_path)
        abs_pdf = os.path.abspath(pdf_path)
        
        doc = word.Documents.Open(abs_docx, ReadOnly=True)
        doc.SaveAs2(abs_pdf, FileFormat=17) # wdFormatPDF = 17
        doc.Close(SaveChanges=0) # wdDoNotSaveChanges = 0
        return True
    except Exception as e:
        print(f"COM conversion error: {e}")
        return False
    finally:
        if word:
            try:
                word.Quit(SaveChanges=0)
            except Exception:
                pass
        pythoncom.CoUninitialize()

# Default field metadata and initial values
FIELDS_METADATA = {
    "AGREEMENT": {
        "title": "Agreement Info",
        "fields": {
            "AGREEMENT_DATE": {"label": "Agreement Date", "type": "text", "default": "01ST Day of this April 2026", "placeholder": "e.g., 01ST Day of this April 2026"},
            "AGREEMENT_PLACE": {"label": "Execution Place", "type": "text", "default": "Bangalore", "placeholder": "e.g., Bangalore"}
        }
    },
    "OWNER": {
        "title": "Landlord / Owner Details",
        "fields": {
            "OWNER_NAME": {"label": "Owner Full Name(s)", "type": "text", "default": "Mr. MANOJ M & SANCHITHA C J", "placeholder": "e.g., Mr. MANOJ M & SANCHITHA C J"},
            "OWNER_PARENT": {"label": "Owner S/O, D/O, W/O Name", "type": "text", "default": "S/O T Mahesh", "placeholder": "e.g., S/O T Mahesh"},
            "OWNER_AGE": {"label": "Owner Age", "type": "number", "default": "45", "placeholder": "e.g., 45"},
            "OWNER_ADDRESS": {"label": "Owner Residential Address", "type": "textarea", "default": "No,99,100 C Near Sri Kalikamba Temple, ChowdeshwariNagar, , Laggere, Bengaluru- 560 058", "placeholder": "Enter full address..."}
        }
    },
    "TENANT": {
        "title": "Tenant Details",
        "fields": {
            "TENANT_NAME": {"label": "Tenant Name", "type": "text", "default": "Mr. RAJUGOWDA", "placeholder": "e.g., Mr. RAJUGOWDA"},
            "TENANT_PARENT": {"label": "Tenant S/O, D/O, W/O Name", "type": "text", "default": "S/O Subbegowda", "placeholder": "e.g., S/O Subbegowda"},
            "TENANT_AGE": {"label": "Tenant Age", "type": "number", "default": "47", "placeholder": "e.g., 47"},
            "TENANT_ADDRESS": {"label": "Tenant Residential Address", "type": "textarea", "default": "No. 18, 3rd Cross, Rajeev Gandhi Nagar, Laggere, Bengaluru-560 058", "placeholder": "Enter full address..."}
        }
    },
    "PREMISES": {
        "title": "Premises / Shop Details",
        "fields": {
            "BUSINESS_NAME": {"label": "Tenant Business Name", "type": "text", "default": "J S TRADERS", "placeholder": "e.g., J S TRADERS"},
            "PREMISES_ADDRESS": {"label": "Premises / Shop Address", "type": "textarea", "default": "No.99 & 100C, Near Sri Kalikamba Temple Chowdeshwari Nagar, Laggere, Bengaluru- 560 058", "placeholder": "Enter shop address..."},
            "PREMISES_DESCRIPTION": {"label": "Premises Description & Amenities", "type": "textarea", "default": "One RCC Roofed Shops, with rolling Shutter and electricity, Toilet and water facility", "placeholder": "List details..."}
        }
    },
    "FINANCIALS": {
        "title": "Rent & Lease Terms",
        "fields": {
            "LEASE_PERIOD": {"label": "Lease Period (Text)", "type": "text", "default": "eleven months", "placeholder": "e.g., eleven months"},
            "LEASE_PERIOD_NUM": {"label": "Lease Period (Months Number)", "type": "number", "default": "11", "placeholder": "e.g., 11"},
            "LEASE_END_DATE": {"label": "Lease End Date", "type": "text", "default": "25/02/2027", "placeholder": "e.g., 25/02/2027"},
            "RENT_AMOUNT": {"label": "Monthly Rent Amount (Rs.)", "type": "text", "default": "10,500.00", "placeholder": "e.g., 10,500.00"},
            "RENT_AMOUNT_WORDS": {"label": "Rent in Words", "type": "text", "default": "Ten Thousand Five Hundred", "placeholder": "e.g., Ten Thousand Five Hundred"},
            "RENT_PAYMENT_DAY": {"label": "Rent Due Day of Month", "type": "text", "default": "15th", "placeholder": "e.g., 15th"},
            "ESCALATION_RATE": {"label": "Escalation Percentage (%)", "type": "text", "default": "5%", "placeholder": "e.g., 5%"},
            "DEPOSIT_AMOUNT": {"label": "Security Deposit Amount (Rs.)", "type": "text", "default": "50,000", "placeholder": "e.g., 50,000"},
            "DEPOSIT_AMOUNT_WORDS": {"label": "Deposit in Words", "type": "text", "default": "Fifty Thousand", "placeholder": "e.g., Fifty Thousand"},
            "DEPOSIT_MODE": {"label": "Deposit Payment Mode", "type": "text", "default": "cash", "placeholder": "e.g., cash, bank transfer, UPI"},
            "NOTICE_PERIOD": {"label": "Notice Period (Text)", "type": "text", "default": "three months", "placeholder": "e.g., three months"}
        }
    },
    "SIGNATURES": {
        "title": "Signatures",
        "fields": {
            "OWNER_SIG_NAMES": {"label": "Owner Names (Signatures)", "type": "text", "default": "MANOJ M AND SANCHITHA C J", "placeholder": "e.g., MANOJ M AND SANCHITHA C J"},
            "TENANT_SIG_NAMES": {"label": "Tenant Name (Signature)", "type": "text", "default": "RAJUGOWDA", "placeholder": "e.g., RAJUGOWDA"}
        }
    }
}

# --- AUTH ENDPOINTS ---

@app.post("/api/auth/register")
def register(payload: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists.")
    
    new_user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
        master_conditions=json.dumps(DEFAULT_CONDITIONS)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    token = create_access_token({"sub": new_user.email})
    return {
        "token": token,
        "user": {
            "email": new_user.email,
            "full_name": new_user.full_name
        }
    }

@app.post("/api/auth/login")
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
        
    token = create_access_token({"sub": user.email})
    return {
        "token": token,
        "user": {
            "email": user.email,
            "full_name": user.full_name
        }
    }

@app.get("/api/auth/me")
def get_me(user: User = Depends(get_current_user)):
    try:
        conds = json.loads(user.master_conditions) if user.master_conditions else DEFAULT_CONDITIONS
    except Exception:
        conds = DEFAULT_CONDITIONS
    return {
        "email": user.email,
        "full_name": user.full_name,
        "master_conditions": conds
    }

class UpdateConditionsPayload(BaseModel):
    conditions: list[str]

@app.put("/api/auth/conditions")
def update_conditions(payload: UpdateConditionsPayload, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user.master_conditions = json.dumps(payload.conditions)
    db.commit()
    return {"detail": "Conditions updated successfully.", "conditions": payload.conditions}

# --- SOFTWARE UPDATE ENDPOINTS ---

@app.get("/api/update/check")
def update_check(user: User = Depends(get_current_user)):
    return updater.get_status()

@app.post("/api/update/apply")
def update_apply(user: User = Depends(get_current_user)):
    ok, err = updater.start_update_in_background()
    if not ok:
        raise HTTPException(status_code=400, detail=err or "No update available.")
    return {"status": "updating"}

# --- AGREEMENT HISTORY ENDPOINTS ---

@app.get("/api/fields")
def get_fields():
    return FIELDS_METADATA

@app.get("/api/agreements")
def list_agreements(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    agreements = db.query(Agreement).filter(Agreement.user_id == user.id).order_by(Agreement.updated_at.desc()).all()
    result = []
    for ag in agreements:
        try:
            parsed_data = json.loads(ag.agreement_data)
        except Exception:
            parsed_data = {}
        result.append({
            "id": ag.id,
            "title": ag.title,
            "data": parsed_data,
            "created_at": ag.created_at.isoformat(),
            "updated_at": ag.updated_at.isoformat(),
            "pdf_url": f"/api/download/pdf/{ag.id}",
            "docx_url": f"/api/download/docx/{ag.id}"
        })
    return result

@app.get("/api/agreements/{agreement_id}")
def get_agreement(agreement_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    agreement = db.query(Agreement).filter(Agreement.id == agreement_id, Agreement.user_id == user.id).first()
    if not agreement:
        raise HTTPException(status_code=404, detail="Agreement not found.")
    try:
        parsed_data = json.loads(agreement.agreement_data)
    except Exception:
        parsed_data = {}
    return {
        "id": agreement.id,
        "title": agreement.title,
        "data": parsed_data,
        "pdf_url": f"/api/download/pdf/{agreement.id}",
        "docx_url": f"/api/download/docx/{agreement.id}"
    }

@app.post("/api/agreements")
def save_and_generate_agreement(
    payload: SaveAgreementPayload = Body(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not os.path.exists(TEMPLATE_PATH):
        raise HTTPException(status_code=404, detail="TEMPLATE.docx not found.")

    try:
        # Load Template
        doc = docx.Document(TEMPLATE_PATH)
        
        # Configure Normal style
        style = doc.styles['Normal']
        style.font.size = docx.shared.Pt(12)
        style.font.name = 'Times New Roman'
        
        # Replace placeholders
        replace_placeholders(doc, payload.data.model_dump())
        
        # Generate unique filenames per agreement
        unique_id = str(uuid.uuid4())[:8]
        safe_title = "".join([c if c.isalnum() else "_" for c in payload.title])
        docx_filename = f"agreement_{user.id}_{safe_title}_{unique_id}.docx"
        pdf_filename = f"agreement_{user.id}_{safe_title}_{unique_id}.pdf"
        
        docx_path = os.path.join(OUTPUT_DIR, docx_filename)
        pdf_path = os.path.join(OUTPUT_DIR, pdf_filename)
        
        # Save generated DOCX
        doc.save(docx_path)
        
        # Convert to PDF
        success = docx_to_pdf(docx_path, pdf_path)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to convert document to PDF.")
            
        # Write/Update record in database
        agreement = None
        if payload.id:
            # Check ownership on update
            agreement = db.query(Agreement).filter(Agreement.id == payload.id, Agreement.user_id == user.id).first()
            
        if agreement:
            # Delete old physical files if updated
            if agreement.docx_path and os.path.exists(agreement.docx_path) and agreement.docx_path != docx_path:
                try: os.remove(agreement.docx_path)
                except Exception: pass
            if agreement.pdf_path and os.path.exists(agreement.pdf_path) and agreement.pdf_path != pdf_path:
                try: os.remove(agreement.pdf_path)
                except Exception: pass
                
            agreement.title = payload.title
            agreement.agreement_data = json.dumps(payload.data.model_dump())
            agreement.docx_path = docx_path
            agreement.pdf_path = pdf_path
            agreement.updated_at = datetime.utcnow()
        else:
            agreement = Agreement(
                user_id=user.id,
                title=payload.title,
                agreement_data=json.dumps(payload.data.model_dump()),
                docx_path=docx_path,
                pdf_path=pdf_path
            )
            db.add(agreement)
            
        db.commit()
        db.refresh(agreement)
        
        return {
            "id": agreement.id,
            "title": agreement.title,
            "pdfUrl": f"/api/download/pdf/{agreement.id}",
            "docxUrl": f"/api/download/docx/{agreement.id}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.delete("/api/agreements/{agreement_id}")
def delete_agreement(agreement_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    agreement = db.query(Agreement).filter(Agreement.id == agreement_id, Agreement.user_id == user.id).first()
    if not agreement:
        raise HTTPException(status_code=404, detail="Agreement not found or unauthorized.")
    
    # Delete physical files
    if agreement.docx_path and os.path.exists(agreement.docx_path):
        try: os.remove(agreement.docx_path)
        except Exception: pass
    if agreement.pdf_path and os.path.exists(agreement.pdf_path):
        try: os.remove(agreement.pdf_path)
        except Exception: pass
            
    db.delete(agreement)
    db.commit()
    return {"detail": "Agreement deleted successfully."}

# --- SECURED DOWNLOAD ENDPOINTS ---

@app.get("/api/download/pdf/{agreement_id}")
def download_pdf(agreement_id: int, token: str, db: Session = Depends(get_db)):
    user = get_current_user_query(token, db)
    agreement = db.query(Agreement).filter(Agreement.id == agreement_id, Agreement.user_id == user.id).first()
    if not agreement:
        raise HTTPException(status_code=404, detail="Agreement not found.")
    
    pdf_path = agreement.pdf_path
    if pdf_path and os.path.exists(pdf_path):
        filename = f"{agreement.title.replace(' ', '_')}.pdf"
        return FileResponse(
            pdf_path, 
            media_type="application/pdf", 
            filename=filename,
            content_disposition_type="inline"
        )
    raise HTTPException(status_code=404, detail="PDF file not found on server.")

@app.get("/api/download/docx/{agreement_id}")
def download_docx(agreement_id: int, token: str, db: Session = Depends(get_db)):
    user = get_current_user_query(token, db)
    agreement = db.query(Agreement).filter(Agreement.id == agreement_id, Agreement.user_id == user.id).first()
    if not agreement:
        raise HTTPException(status_code=404, detail="Agreement not found.")
    
    docx_path = agreement.docx_path
    if docx_path and os.path.exists(docx_path):
        return FileResponse(docx_path, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", filename=f"{agreement.title.replace(' ', '_')}.docx")
    raise HTTPException(status_code=404, detail="DOCX file not found on server.")

# Serve Static files at root
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
