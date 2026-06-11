import os
import json
import uuid
import docx
import pythoncom
import win32com.client
from datetime import datetime
import random
import time
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from fastapi import FastAPI, HTTPException, Body, Depends, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session

def _load_dotenv():
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.isfile(env_file):
        return
    with open(env_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            key, val = key.strip(), val.strip().strip('"').strip("'")
            if key:
                os.environ[key] = val

_load_dotenv()

# Import Database & Auth modules
from database import Base, engine, User, Agreement, Notification, Template, Tenant, Owner, Property, get_db, SessionLocal
from auth import hash_password, verify_password, create_access_token, decode_access_token
from runtime_paths import resource_dir, data_dir
import updater
from kannada_helper import unicode_to_nudi


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

DEFAULT_KANNADA_CONDITIONS = [
    "ಸದರಿ ಮನೆಗೆ ಮುಂಗಡ (ಭದ್ರತಾ ಠೇವಣಿ) ಹಣವಾಗಿ ರೂ.{{DEPOSIT_AMOUNT}}/- ({{DEPOSIT_AMOUNT_WORDS}}) ರೂಪಾಯಿಗಳನ್ನು ನಿಮಗೆ ಈ ಕೆಳಕಂಡ ಸಾಕ್ಷಿದಾರರ ಸಮಕ್ಷಮ ನಗದು ರೂಪದಲ್ಲಿ ಪಾವತಿಮಾಡಿರುತ್ತೇನೆ.  ಸದರಿ ಮುಂಗಡ ಹಣಕ್ಕೆ ತಾವು ಯಾವುದೇ ರೀತಿಯ ಬಡ್ಡಿಯನ್ನು ಕೊಡಬೇಕಾಗಿಲ್ಲ ಮತ್ತು  ಸದರಿ ಹಣವನ್ನು  ಮನೆಯನ್ನು ಖಾಲೀ ಮಾಡಿ ನಿಮ್ಮ ಸ್ವಾಧೀನಕ್ಕೆ ಕೊಡುವಾಗ ಒಂದೇ ಕಂತಿನಲ್ಲಿ ಹಿಂದಿರುಗಿಸತಕ್ಕದ್ದು.",
    "ಸದರಿ ಮನೆಗೆ ಬಾಡಿಗೆಯಾಗಿ ರೂ.{{RENT_AMOUNT}}/- ({{RENT_AMOUNT_WORDS}}) ರೂಪಾಯಿಗಳನ್ನು ನಿಗಧಿ ಮಾಡಿದ್ದು,  ಸದರಿ ಬಾಡಿಗೆಯನ್ನು ಪ್ರತಿ ಮಾಹೇ {{RENT_PAYMENT_DAY}} ನೇ ದಿನಾಂಕದ ಒಳಗೆ ತಪ್ಪದೇ ಪಾವತಿಮಾಡುತ್ತೇನೆ.",
    "ಮೇಲ್ಕಂಡ ಸದರಿ ಮನೆಗೆ ದಿನಾಂಕ: {{LEASE_START_DATE}} ರಿಂದ {{LEASE_PERIOD_NUM}} ({{LEASE_PERIOD}}) ತಿಂಗಳು ಅವಧಿಯನ್ನು ಗೊತ್ತುಪಡಿಸಲಾಗಿರುತ್ತದೆ.",
    "ಸದರಿ ಮನೆಯಲ್ಲಿ ಉಪಯೋಗಿಸುವ ವಿಧ್ಯುತ್ ಬಿಲ್ಲನ್ನು ಪ್ರತಿ ತಿಂಗಳು ವಿಧ್ಯುತ್ ಇಲಾಖೆಗೆ ಕಟ್ಟುವುದಾಗಿ ಒಪ್ಪಿರುತ್ತೇನೆ.",
    "ಸದರಿ ಮನೆಯನ್ನು ವಾಯಿದೆಯನಂತರ ಬಾಡಿಗೆ ಮುಂದುವರೆದಲ್ಲಿ ಶೇಖಡ {{ESCALATION_RATE}} ಹೆಚ್ಚಿನ ಬಾಡಿಗೆ ಕೊಟ್ಟು ಹೊಸ ಕರಾರನ್ನು ಮಾಡಿಕೊಂಡು ಮುಂದುವರಿಯುವುದಾಗಿ ಒಪ್ಪಿರುತ್ತೇನೆ.",
    "ಸದರಿ ಮನೆಯನ್ನು ನನ್ನ ವಾಸಕ್ಕೆ ಮಾತ್ರ ಉಪಯೋಗಿಸುವುದಾಗಿ ಮತ್ತು ನಾನು  ಯಾವುದೇ ಕಾರಣಕ್ಕೂ ಯಾರಿಗೂ ಒಳಬಾಡಿಗೆಗೆ, ಶಿಕ್ಮಿ ಬಾಡಿಗೆಗೆ ಕೊಡುವುದಿಲ್ಲವೆಂದು ಹಾಗೂ ಕಾನೂನು ಬಾಹಿರ ಚಟುವಟಿಕೆಗಳಿಗೆ ಗುರಿಪಡಿಸುದಿಲ್ಲವೆಂದು ಒಪ್ಪಿರುತ್ತೇನೆ.",
    "ಸದರಿ  ಮನೆಯನ್ನು ಖಾಲೀ  ಮಾಡುವ ಅಥವಾ  ಖಾಲೀ  ಮಾಡಿಸುವ ಸಂದರ್ಭ ಬಂದಲ್ಲಿ ಪರಸ್ಪರ {{LEASE_PERIOD_NUM}} ತಿಂಗಳ ಅವಧಿ ಮುಂಚಿತ {{NOTICE_PERIOD_NUM}} ({{NOTICE_PERIOD}}) ತಿಂಗಳ ಮುಂಚಿತವಾಗಿ ತಿಳಿಸತಕ್ಕದ್ದು.",
    "ಸದರಿ  ಮನೆಯಲ್ಲಿ  ಯಾವುದೇ  ತಂಟೆ ತಕರಾರು ಬಂದಲ್ಲಿ ಮಾಲೀಕರಾದ ನೀವು ನಮ್ಮನ್ನು ಅವಧಿಯ ಮುಂಚಿತವಗಿ ಖಾಲಿ ಮಾಡಿಸುವುದಕ್ಕೆ ಸಂಪೂರ್ಣ ಜವಬ್ದಾರನಾಗಿರುತ್ತೀರಿ. ಹಾಗೂ ಈ ಕರಾರು ಪತ್ರದ ಅಸಲು ಪ್ರತಿಯಾಗಲೀ ನಕಲು ಪ್ರತಿಯಾಗಲೀ ಅಡಮಾನವಿಟ್ಟು ಸಾಲ ಪಡೆಯುವಂತಿಲ್ಲ.",
    "ಸದರಿ ಮನೆಯನ್ನು ನಾನು ಬಾಡಿಗೆಗೆ ಪಡೆಯುವಾಗ ಯಾವ ಸ್ಥಿತಿಯಲ್ಲಿ ಪಡೆದಿರುತ್ತೇನೊ, ಅದೇ ರೀತಿ ನಾನು ಸಹ ಪೈಂಟಿಂಗ್ ಮಾಡಿಸಿ ಹಿಂದಿರುಗಿಸುವುದಾಗಿ ಒಪ್ಪಿರುತ್ತೇನೆ. ಡ್ಯಾಮೇಜುಗಳನ್ನು ಸರಿಪಡಿಸಿಕೊಡುವುದಾಗಿ ಒಪ್ಪಿರುತ್ತೇನೆ, ಸದರಿ ಮನೆಗೆ ಪೈಂಟಿಂಗ್ ಮಾಡಿಸುವ ವೆಚ್ದ ತಮ್ಮ ಬಳಿ ಇರುವ ಮುಂಗಡ ಹಣದಲ್ಲಿ ಮುಟ್ಟುಗೋಲು ಹಾಕಿಕೊಳ್ಳಲು ಒಪ್ಪಿರುತ್ತೇನೆ ಹಾಗೂ  ಸದರಿ ಕರಾರು ಪತ್ರದ  ಅಸಲು ಪ್ರತಿಯನ್ನು ಬಾಡಿಗೆದಾರರಾದ ನನ್ನ ವಶದಲ್ಲಿ ಮತ್ತು ನಕಲು ಪ್ರತಿಯನ್ನು ಮಾಲೀಕರಾದ ನಿಮ್ಮ ವಶದಲ್ಲಿ ಇಟ್ಟುಕೊಂಡಿರಲು ನಾನು ಒಪ್ಪಿ ತಮಗೂ ಒಪ್ಪಿಸಿ ಬರೆದುಕೊಟ್ಟ ವಾಸದ  ಮನೆ ಬಾಡಿಗೆ ಒಪ್ಪಂದದ  ಕರಾರು ಪತ್ರದ ಸಹಿ."
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

# --- SMTP AND 2FA UTILITIES ---

OTP_STORE = {} # format: {email: {"otp": str, "expires": float, "type": str, "data": dict}}

def generate_otp() -> str:
    return f"{random.randint(100000, 999999)}"

def send_email(to_email: str, subject: str, html_body: str) -> bool:
    smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    try:
        smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    except ValueError:
        smtp_port = 587
    smtp_user = os.environ.get("SMTP_USER", "qryvanta.technologies@gmail.com")
    smtp_pass = os.environ.get("SMTP_PASS", "ndparpwhmvkqxpab").replace(" ", "")

    if not smtp_user or not smtp_pass:
        print("SMTP credentials not configured. Email not sent.")
        return False

    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(html_body, 'html'))

        server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, to_email, msg.as_string())
        server.quit()
        print(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        return False

def send_email_otp(to_email: str, otp: str, purpose: str) -> bool:
    subject = f"Verification Code: {otp}"
    html_body = f"""
    <div style="font-family: sans-serif; padding: 20px; color: #333;">
        <h2>Verify Your Email</h2>
        <p>You requested a verification code for <strong>{purpose}</strong> on Rental Pro.</p>
        <div style="font-size: 24px; font-weight: bold; background: #f3f4f6; padding: 15px; text-align: center; border-radius: 8px; margin: 20px 0; letter-spacing: 5px;">
            {otp}
        </div>
        <p>This code is valid for 5 minutes. If you did not make this request, you can safely ignore this email.</p>
        <hr style="border: 0; border-top: 1px solid #e5e7eb; margin: 20px 0;" />
        <p style="font-size: 12px; color: #6b7280;">Sent by Rental Pro. Developed by Qryvanta Technologies.</p>
    </div>
    """
    return send_email(to_email, subject, html_body)

def send_registration_notifications(user_email: str, full_name: str):
    welcome_subject = "Welcome to Rental Pro!"
    welcome_body = f"""
    <div style="font-family: sans-serif; padding: 20px; color: #333;">
        <h2>Welcome to Rental Pro, {full_name}!</h2>
        <p>Thank you for registering. Your account has been successfully created and verified.</p>
        <p>You can now start generating and managing your rental agreements.</p>
        <hr style="border: 0; border-top: 1px solid #e5e7eb; margin: 20px 0;" />
        <p style="font-size: 12px; color: #6b7280;">Sent by Rental Pro. Developed by Qryvanta Technologies.</p>
    </div>
    """
    threading.Thread(target=send_email, args=(user_email, welcome_subject, welcome_body), daemon=True).start()

    admin_email = os.environ.get("SMTP_USER", "qryvanta.technologies@gmail.com")
    admin_subject = f"New User Registered: {full_name}"
    admin_body = f"""
    <div style="font-family: sans-serif; padding: 20px; color: #333;">
        <h2>New User Registration</h2>
        <p>A new user has registered on Rental Pro:</p>
        <ul>
            <li><strong>Name:</strong> {full_name}</li>
            <li><strong>Email:</strong> {user_email}</li>
            <li><strong>Time:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</li>
        </ul>
        <hr style="border: 0; border-top: 1px solid #e5e7eb; margin: 20px 0;" />
        <p style="font-size: 12px; color: #6b7280;">Sent by Rental Pro. Developed by Qryvanta Technologies.</p>
    </div>
    """
    threading.Thread(target=send_email, args=(admin_email, admin_subject, admin_body), daemon=True).start()

def create_notification_record(db: Session, user_id: int, title: str | None = None, desc: str | None = None, title_key: str | None = None, desc_key: str | None = None, params: str | None = None, background_tasks: BackgroundTasks = None):
    notif = Notification(
        user_id=user_id,
        title=title,
        desc=desc,
        title_key=title_key,
        desc_key=desc_key,
        params=params
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    
    user = db.query(User).filter(User.id == user_id).first()
    if user and user.email:
        subject = title or f"Notification Alert: {title_key or 'New Alert'}"
        body = desc or f"You have a new notification on Rental Pro: {desc_key or ''}"
        
        email_body = f"""
        <div style="font-family: sans-serif; padding: 20px; color: #333;">
            <h2>{subject}</h2>
            <p>{body}</p>
            <p><strong>Recipient:</strong> {user.full_name or user.email} ({user.email})</p>
            <hr style="border: 0; border-top: 1px solid #e5e7eb; margin: 20px 0;" />
            <p style="font-size: 12px; color: #6b7280;">Sent by Rental Pro. Developed by Qryvanta Technologies.</p>
        </div>
        """
        
        if background_tasks:
            background_tasks.add_task(send_email, user.email, f"Rental Pro - {subject}", email_body)
        else:
            threading.Thread(target=send_email, args=(user.email, f"Rental Pro - {subject}", email_body), daemon=True).start()
            
        admin_email = os.environ.get("SMTP_USER", "qryvanta.technologies@gmail.com")
        if admin_email and user.email.lower() != admin_email.lower():
            if background_tasks:
                background_tasks.add_task(send_email, admin_email, f"[Admin CC] Rental Pro - {subject}", email_body)
            else:
                threading.Thread(target=send_email, args=(admin_email, f"[Admin CC] Rental Pro - {subject}", email_body), daemon=True).start()
                
    return notif


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
        pass

    # Attempt to add template_id column dynamically to agreements table
    try:
        with engine.begin() as conn:
            import sqlalchemy
            conn.execute(sqlalchemy.text("ALTER TABLE agreements ADD COLUMN template_id INTEGER"))
        print("[MIGRATION] Added template_id column to agreements table successfully.")
    except Exception as e:
        pass

    # Attempt to add output_dir column dynamically to users table
    try:
        with engine.begin() as conn:
            import sqlalchemy
            conn.execute(sqlalchemy.text("ALTER TABLE users ADD COLUMN output_dir TEXT"))
        print("[MIGRATION] Added output_dir column to users table successfully.")
    except Exception as e:
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
                master_conditions=json.dumps({
                    "en": DEFAULT_CONDITIONS,
                    "kn": DEFAULT_KANNADA_CONDITIONS
                })
            )
            tenant_user = User(
                email="tenant@rentalpro.com",
                hashed_password=hash_password("tenant123"),
                full_name="Tenant User",
                master_conditions=json.dumps({
                    "en": DEFAULT_CONDITIONS,
                    "kn": DEFAULT_KANNADA_CONDITIONS
                })
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
        
        # Seed default notifications for users if they don't have any
        users = db.query(User).all()
        for u in users:
            if db.query(Notification).filter(Notification.user_id == u.id).count() == 0:
                print(f"Seeding default notifications for user: {u.email}...")
                n1 = Notification(
                    user_id=u.id,
                    title_key="verifyApproved",
                    desc_key="aadharVerified"
                )
                n2 = Notification(
                    user_id=u.id,
                    title_key="systemReady",
                    desc_key="systemReadyDesc"
                )
                db.add(n1)
                db.add(n2)
        # Seed default tenants if they don't exist yet
        admin_user = db.query(User).filter(User.email == "admin@rentalpro.com").first()
        if admin_user:
            default_tenants_info = [
                {
                    "name": "Mr. RAJUGOWDA",
                    "phone": "+91 9900112233",
                    "email": "rajugowda@gmail.com",
                    "guardian": "S/O Subbegowda",
                    "age": 47,
                    "address": "No. 18, 3rd Cross, Rajeev Gandhi Nagar, Laggere, Bengaluru-560 058",
                    "aadhar": "1234-5678-9012"
                },
                {
                    "name": "Mr. AMIT KUMAR",
                    "phone": "+91 9876543210",
                    "email": "amit.kumar@outlook.com",
                    "guardian": "S/O Ram Kumar",
                    "age": 30,
                    "address": "Flat 402, Greenfield Apartments, Laggere, Bengaluru-560 058",
                    "aadhar": "9876-5432-1098"
                },
                {
                    "name": "Mrs. LAKSHMI DEVI",
                    "phone": "+91 9448833221",
                    "email": "lakshmi.devi@yahoo.com",
                    "guardian": "W/O Venkatesh",
                    "age": 38,
                    "address": "No. 45, Chowdeshwari Nagar, Laggere, Bengaluru-560 058",
                    "aadhar": "4567-8901-2345"
                }
            ]
            for t_info in default_tenants_info:
                exists = db.query(Tenant).filter(
                    Tenant.user_id == admin_user.id,
                    Tenant.name == t_info["name"]
                ).first()
                if not exists:
                    print(f"=== SEEDING TENANT: {t_info['name']} ===")
                    new_t = Tenant(
                        user_id=admin_user.id,
                        name=t_info["name"],
                        phone=t_info["phone"],
                        email=t_info["email"],
                        guardian=t_info["guardian"],
                        age=t_info["age"],
                        address=t_info["address"],
                        aadhar=t_info["aadhar"]
                    )
                    db.add(new_t)

            # Seed default owners if they don't exist yet
            default_owners_info = [
                {
                    "name": "Mr. MANOJ M & SANCHITHA C J",
                    "phone": "+91 9886655443",
                    "email": "manoj.sanchitha@gmail.com",
                    "guardian": "S/O T Mahesh",
                    "age": 45,
                    "address": "No,99,100 C Near Sri Kalikamba Temple, ChowdeshwariNagar, , Laggere, Bengaluru- 560 058"
                },
                {
                    "name": "Mrs. LATHA SHARMA",
                    "phone": "+91 9775533112",
                    "email": "latha.sharma@gmail.com",
                    "guardian": "W/O R K Sharma",
                    "age": 42,
                    "address": "No. 24, Greenfield Heights, Laggere, Bengaluru-560 058"
                }
            ]
            for o_info in default_owners_info:
                exists = db.query(Owner).filter(
                    Owner.user_id == admin_user.id,
                    Owner.name == o_info["name"]
                ).first()
                if not exists:
                    print(f"=== SEEDING OWNER: {o_info['name']} ===")
                    new_o = Owner(
                        user_id=admin_user.id,
                        name=o_info["name"],
                        phone=o_info["phone"],
                        email=o_info["email"],
                        guardian=o_info["guardian"],
                        age=o_info["age"],
                        address=o_info["address"]
                    )
                    db.add(new_o)

            # Seed default properties if they don't exist yet
            default_properties_info = [
                {
                    "name": "Laggere Commercial Shop",
                    "address": "No.99 & 100C, Near Sri Kalikamba Temple Chowdeshwari Nagar, Laggere, Bengaluru- 560 058",
                    "description": "One RCC Roofed Shops, with rolling Shutter and electricity, Toilet and water facility",
                    "business_name": "J S TRADERS"
                },
                {
                    "name": "Sharma Groceries Premises",
                    "address": "Flat 402, Greenfield Apartments, Laggere, Bengaluru-560 058",
                    "description": "Commercial retail ground floor shop space with basic fixtures, electricity, and private washroom.",
                    "business_name": "SHARMA GROCERIES"
                }
            ]
            for p_info in default_properties_info:
                exists = db.query(Property).filter(
                    Property.user_id == admin_user.id,
                    Property.name == p_info["name"]
                ).first()
                if not exists:
                    print(f"=== SEEDING PROPERTY: {p_info['name']} ===")
                    new_p = Property(
                        user_id=admin_user.id,
                        name=p_info["name"],
                        address=p_info["address"],
                        description=p_info["description"],
                        business_name=p_info["business_name"]
                    )
                    db.add(new_p)
        db.commit()
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
    data: dict
    template_id: int | None = None

class CreateNotificationPayload(BaseModel):
    title: str | None = None
    desc: str | None = None
    title_key: str | None = None
    desc_key: str | None = None
    params: dict | None = None

class TenantCreate(BaseModel):
    name: str
    phone: str | None = None
    email: str | None = None
    guardian: str | None = None
    age: int | None = None
    address: str | None = None
    aadhar: str | None = None

class OwnerCreate(BaseModel):
    name: str
    phone: str | None = None
    email: str | None = None
    guardian: str | None = None
    age: int | None = None
    address: str | None = None

class PropertyCreate(BaseModel):
    name: str
    address: str
    description: str | None = None
    business_name: str | None = None

# Helper to perform find-and-replace
def replace_placeholders(doc, data: dict, font_name: str = 'Times New Roman'):
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
                    run.font.name = font_name
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
            for placeholder in [f"{{{{{key}}}}}", f"[{key}]"]:
                if placeholder in text_before:
                    for run in p.runs:
                        if placeholder in run.text:
                            run.text = run.text.replace(placeholder, str(val or ""))
                            run.font.size = docx.shared.Pt(12)
                            run.font.name = font_name
                    if placeholder in p.text:
                        p.text = p.text.replace(placeholder, str(val or ""))
                        for run in p.runs:
                            run.font.size = docx.shared.Pt(12)
                            run.font.name = font_name

    # Replace in tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in list(cell.paragraphs):
                    text_before = p.text
                    for key, val in data.items():
                        if key == "AGREEMENT_CONDITIONS":
                            continue
                        for placeholder in [f"{{{{{key}}}}}", f"[{key}]"]:
                            if placeholder in text_before:
                                for run in p.runs:
                                    if placeholder in run.text:
                                        run.text = run.text.replace(placeholder, str(val or ""))
                                        if run.font.size is None:
                                            run.font.size = docx.shared.Pt(12)
                                        if run.font.name is None:
                                            run.font.name = font_name
                                if placeholder in p.text:
                                    p.text = p.text.replace(placeholder, str(val or ""))
                                    for run in p.runs:
                                        run.font.size = docx.shared.Pt(12)
                                        run.font.name = font_name

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

class UserVerifyOTP(BaseModel):
    email: str
    otp: str
    type: str

class UserResendOTP(BaseModel):
    email: str
    type: str

@app.post("/api/auth/register")
def register(payload: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists.")
    
    otp = generate_otp()
    OTP_STORE[payload.email] = {
        "otp": otp,
        "expires": time.time() + 300, # 5 minutes
        "type": "register",
        "data": {
            "password": payload.password,
            "full_name": payload.full_name
        }
    }
    
    success = send_email_otp(payload.email, otp, "Registration")
    if not success:
        # We clean up the OTP session if email fails to send
        OTP_STORE.pop(payload.email, None)
        raise HTTPException(status_code=500, detail="Failed to send verification code. Please check SMTP settings.")
        
    return {"status": "2fa_required", "email": payload.email}

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

@app.post("/api/auth/verify-2fa")
def verify_2fa(payload: UserVerifyOTP, db: Session = Depends(get_db)):
    email = payload.email
    entry = OTP_STORE.get(email)
    
    if not entry or entry["type"] != payload.type:
        raise HTTPException(status_code=400, detail="No active verification session found for this email.")
        
    if time.time() > entry["expires"]:
        OTP_STORE.pop(email, None)
        raise HTTPException(status_code=400, detail="Verification code has expired. Please try again.")
        
    if entry["otp"] != payload.otp:
        raise HTTPException(status_code=400, detail="Invalid verification code.")
        
    # Correct OTP!
    if entry["type"] == "register":
        reg_data = entry["data"]
        new_user = User(
            email=email,
            hashed_password=hash_password(reg_data["password"]),
            full_name=reg_data["full_name"],
            master_conditions=json.dumps({
                "en": DEFAULT_CONDITIONS,
                "kn": DEFAULT_KANNADA_CONDITIONS
            })
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Seed default notifications for new user
        create_notification_record(db, new_user.id, title_key="verifyApproved", desc_key="aadharVerified")
        create_notification_record(db, new_user.id, title_key="systemReady", desc_key="systemReadyDesc")
        
        # Send notifications
        send_registration_notifications(email, new_user.full_name)
        
        OTP_STORE.pop(email, None)
        token = create_access_token({"sub": new_user.email})
        return {
            "token": token,
            "user": {
                "email": new_user.email,
                "full_name": new_user.full_name
            }
        }
        
    elif entry["type"] == "login":
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
            
        OTP_STORE.pop(email, None)
        token = create_access_token({"sub": user.email})
        return {
            "token": token,
            "user": {
                "email": user.email,
                "full_name": user.full_name
            }
        }

@app.post("/api/auth/resend-2fa")
def resend_2fa(payload: UserResendOTP, db: Session = Depends(get_db)):
    email = payload.email
    entry = OTP_STORE.get(email)
    
    if not entry or entry["type"] != payload.type:
        raise HTTPException(status_code=400, detail="No active verification session. Please go back and try again.")
        
    otp = generate_otp()
    entry["otp"] = otp
    entry["expires"] = time.time() + 300 # refresh 5-minute timer
    
    success = send_email_otp(email, otp, "Registration" if entry["type"] == "register" else "Login Verification")
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send verification code. Please check SMTP settings.")
        
    return {"status": "success", "message": "Verification code resent successfully."}


@app.get("/api/auth/me")
def get_me(user: User = Depends(get_current_user)):
    try:
        conds = json.loads(user.master_conditions) if user.master_conditions else DEFAULT_CONDITIONS
    except Exception:
        conds = DEFAULT_CONDITIONS
        
    if isinstance(conds, list):
        conds = {
            "en": conds,
            "kn": DEFAULT_KANNADA_CONDITIONS
        }
    elif isinstance(conds, dict):
        if "en" not in conds:
            conds["en"] = DEFAULT_CONDITIONS
        if "kn" not in conds:
            conds["kn"] = DEFAULT_KANNADA_CONDITIONS

    return {
        "email": user.email,
        "full_name": user.full_name,
        "master_conditions": conds["en"],
        "master_conditions_kn": conds["kn"],
        "output_dir": user.output_dir
    }

class UpdateConditionsPayload(BaseModel):
    conditions: list[str]
    conditions_kn: list[str] | None = None

@app.put("/api/auth/conditions")
def update_conditions(payload: UpdateConditionsPayload, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    data = {
        "en": payload.conditions,
        "kn": payload.conditions_kn if payload.conditions_kn is not None else DEFAULT_KANNADA_CONDITIONS
    }
    user.master_conditions = json.dumps(data)
    db.commit()
    return {"detail": "Conditions updated successfully.", "conditions": payload.conditions, "conditions_kn": payload.conditions_kn}

@app.get("/api/diagnostics/db-health")
def get_db_health(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        # Check SQLite version and run simple query
        from sqlalchemy import text
        version = db.execute(text("SELECT sqlite_version()")).scalar()
        
        # Count rows in each table to ensure schemas are functional
        user_count = db.query(User).count()
        agreement_count = db.query(Agreement).count()
        template_count = db.query(Template).count()
        tenant_count = db.query(Tenant).count()
        owner_count = db.query(Owner).count()
        property_count = db.query(Property).count()
        
        # Get DB file size if available
        db_file = "database.db"
        db_size_kb = 0
        if os.path.exists(db_file):
            db_size_kb = os.path.getsize(db_file) // 1024

        return {
            "status": "healthy",
            "sqlite_version": version,
            "size_kb": db_size_kb,
            "counts": {
                "users": user_count,
                "agreements": agreement_count,
                "templates": template_count,
                "tenants": tenant_count,
                "owners": owner_count,
                "properties": property_count
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database diagnostic failed: {str(e)}")

@app.get("/api/diagnostics/run")
def run_app_diagnostics(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        results = {}
        
        # 1. Check template file presence
        results["template_exists"] = os.path.exists(TEMPLATE_PATH)
        
        # 2. Check output directory write permissions
        output_dir = user.output_dir or OUTPUT_DIR
        results["output_directory"] = output_dir
        results["output_dir_writable"] = os.access(os.path.dirname(output_dir) if not os.path.exists(output_dir) else output_dir, os.W_OK)
        
        # 3. Check win32com MS Word connection capability (optional/warning on non-Windows/missing Word)
        has_win32 = False
        try:
            import win32com.client
            has_win32 = True
        except ImportError:
            pass
        results["win32com_available"] = has_win32
        
        # 4. Check system memory/disk usage via standard os module (shutil)
        import shutil
        total, used, free = shutil.disk_usage(os.path.abspath("."))
        results["disk"] = {
            "total_gb": round(total / (2**30), 2),
            "used_gb": round(used / (2**30), 2),
            "free_gb": round(free / (2**30), 2),
            "percent_used": round((used / total) * 100, 1)
        }

        # 5. Check if Nudi transliteration helper loads correctly
        from kannada_helper import unicode_to_nudi
        test_nudi = unicode_to_nudi("ನಮಸ್ಕಾರ")
        results["kannada_nudi_support"] = test_nudi is not None

        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "diagnostics": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"System diagnostics failed: {str(e)}")

# --- USER SETTINGS ENDPOINTS ---

class SaveSettingsPayload(BaseModel):
    output_dir: str | None = None
    full_name: str | None = None
    password: str | None = None

@app.put("/api/settings")
def save_settings(payload: SaveSettingsPayload, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if payload.output_dir is not None:
        cleaned_dir = payload.output_dir.strip()
        if cleaned_dir:
            # Check if directory exists, if not, try to create it to validate path
            if not os.path.exists(cleaned_dir):
                try:
                    os.makedirs(cleaned_dir, exist_ok=True)
                except Exception as e:
                    raise HTTPException(status_code=400, detail=f"Invalid directory path or permission denied: {e}")
            user.output_dir = cleaned_dir
        else:
            user.output_dir = None
            
    if payload.full_name is not None:
        cleaned_name = payload.full_name.strip()
        if not cleaned_name:
            raise HTTPException(status_code=400, detail="Full Name cannot be empty.")
        user.full_name = cleaned_name
        
    if payload.password is not None and payload.password.strip() != "":
        user.hashed_password = hash_password(payload.password.strip())
    
    db.commit()
    return {"status": "success", "output_dir": user.output_dir, "full_name": user.full_name}

@app.post("/api/settings/browse-folder")
def browse_folder(user: User = Depends(get_current_user)):
    import tkinter as tk
    from tkinter import filedialog
    
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        folder = filedialog.askdirectory(parent=root, title="Select Output Saving Directory")
        root.destroy()
        return {"folder": folder or ""}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to open native directory browser: {e}")


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
            "template_id": ag.template_id,
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
    template = None
    custom_docx_base_path = None
    
    if payload.template_id and payload.template_id != -1:
        template = db.query(Template).filter(Template.id == payload.template_id, Template.user_id == user.id).first()
        if not template:
            raise HTTPException(status_code=404, detail="Selected custom template not found.")
            
        if template.has_file and template.file_path and os.path.exists(template.file_path):
            custom_docx_base_path = template.file_path

    try:
        # Load Template
        if payload.template_id == -1:
            template_path = os.path.join(RESOURCE_DIR, "TEMPLATE_KAN.docx")
            if not os.path.exists(template_path):
                template_path = "TEMPLATE_KAN.docx"
            if not os.path.exists(template_path):
                raise HTTPException(status_code=404, detail="TEMPLATE_KAN.docx not found.")
            doc = docx.Document(template_path)
        elif custom_docx_base_path:
            doc = docx.Document(custom_docx_base_path)
        elif template:
            doc = docx.Document()
            style = doc.styles['Normal']
            style.font.size = docx.shared.Pt(12)
            style.font.name = 'Times New Roman'
            
            paragraphs = template.content.split("\n")
            for p_text in paragraphs:
                doc.add_paragraph(p_text)
        else:
            if not os.path.exists(TEMPLATE_PATH):
                raise HTTPException(status_code=404, detail="TEMPLATE.docx not found.")
            doc = docx.Document(TEMPLATE_PATH)
        
        # Configure Normal style
        style = doc.styles['Normal']
        style.font.size = docx.shared.Pt(12)
        style.font.name = 'Nudi Akshar-02' if payload.template_id == -1 else 'Times New Roman'
        
        # Replace placeholders
        if payload.template_id == -1:
            translated_data = {}
            for k, v in payload.data.items():
                if isinstance(v, str):
                    translated_data[k] = unicode_to_nudi(v)
                elif isinstance(v, list):
                    translated_data[k] = [unicode_to_nudi(item) if isinstance(item, str) else item for item in v]
                else:
                    translated_data[k] = v
            replace_placeholders(doc, translated_data, font_name="Nudi Akshar-02")
        else:
            replace_placeholders(doc, payload.data, font_name="Times New Roman")
        
        # Generate unique filenames per agreement
        unique_id = str(uuid.uuid4())[:8]
        safe_title = "".join([c if c.isalnum() else "_" for c in payload.title])
        docx_filename = f"agreement_{user.id}_{safe_title}_{unique_id}.docx"
        pdf_filename = f"agreement_{user.id}_{safe_title}_{unique_id}.pdf"
        
        # Determine output folder: user-defined or default
        out_dir = OUTPUT_DIR
        if user.output_dir and os.path.exists(user.output_dir):
            out_dir = user.output_dir
        elif user.output_dir:
            try:
                os.makedirs(user.output_dir, exist_ok=True)
                out_dir = user.output_dir
            except Exception:
                pass
        
        docx_path = os.path.join(out_dir, docx_filename)
        pdf_path = os.path.join(out_dir, pdf_filename)
        
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
            agreement.agreement_data = json.dumps(payload.data)
            agreement.docx_path = docx_path
            agreement.pdf_path = pdf_path
            agreement.updated_at = datetime.utcnow()
            agreement.template_id = payload.template_id
        else:
            agreement = Agreement(
                user_id=user.id,
                template_id=payload.template_id,
                title=payload.title,
                agreement_data=json.dumps(payload.data),
                docx_path=docx_path,
                pdf_path=pdf_path
            )
            db.add(agreement)
            
        db.commit()
        db.refresh(agreement)

        # Add dynamic notification to DB
        create_notification_record(
            db,
            user.id,
            title_key="agreementSavedTitle",
            desc_key="agreementSavedDesc",
            params=json.dumps({"title": agreement.title})
        )
        
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

    # Add deletion notification to DB
    create_notification_record(db, user.id, title_key="agreementDeletedTitle", desc_key="agreementDeletedDesc")

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


# --- NOTIFICATION ENDPOINTS ---

@app.get("/api/notifications")
def get_notifications(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        agreements = db.query(Agreement).filter(Agreement.user_id == user.id).all()
        for ag in agreements:
            try:
                ag_data = json.loads(ag.agreement_data)
                end_date_str = ag_data.get("LEASE_END_DATE")
                if end_date_str:
                    parsed_date = None
                    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"):
                        try:
                            parsed_date = datetime.strptime(end_date_str.strip(), fmt)
                            break
                        except ValueError:
                            continue
                    
                    if parsed_date:
                        days_remaining = (parsed_date - datetime.utcnow()).days
                        if 0 <= days_remaining <= 30:
                            notif_desc = f"The lease agreement '{ag.title}' is set to expire on {end_date_str} ({days_remaining} days remaining)."
                            exists = db.query(Notification).filter(
                                Notification.user_id == user.id,
                                Notification.desc == notif_desc
                            ).first()
                            
                            if not exists:
                                create_notification_record(
                                    db,
                                    user.id,
                                    title="Lease Expiring Soon",
                                    desc=notif_desc
                                )
            except Exception as e:
                print(f"Error parsing agreement end date for ID {ag.id}: {e}")
    except Exception as e:
        print(f"Error checking lease expirations: {e}")

    notifs = db.query(Notification).filter(Notification.user_id == user.id).order_by(Notification.created_at.desc()).all()
    result = []
    for n in notifs:
        result.append({
            "id": n.id,
            "title": n.title,
            "desc": n.desc,
            "title_key": n.title_key,
            "desc_key": n.desc_key,
            "params": json.loads(n.params) if n.params else None,
            "created_at": n.created_at.isoformat()
        })
    return result

@app.delete("/api/notifications/{notification_id}")
def delete_notification(notification_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    notif = db.query(Notification).filter(Notification.id == notification_id, Notification.user_id == user.id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found.")
    db.delete(notif)
    db.commit()
    return {"status": "success", "message": "Notification deleted successfully."}

@app.post("/api/notifications")
def create_notification(payload: CreateNotificationPayload, user: User = Depends(get_current_user), db: Session = Depends(get_db), background_tasks: BackgroundTasks = None):
    notif = create_notification_record(
        db,
        user.id,
        title=payload.title,
        desc=payload.desc,
        title_key=payload.title_key,
        desc_key=payload.desc_key,
        params=json.dumps(payload.params) if payload.params else None,
        background_tasks=background_tasks
    )
    return {
        "id": notif.id,
        "title": notif.title,
        "desc": notif.desc,
        "title_key": notif.title_key,
        "desc_key": notif.desc_key,
        "params": payload.params,
        "created_at": notif.created_at.isoformat()
    }


# --- TEMPLATES ENDPOINTS ---

from fastapi import Form, UploadFile, File
import re
from pypdf import PdfReader

def extract_placeholders(text: str) -> list[str]:
    # Match {{PLACEHOLDER}}
    matches_curly = re.findall(r"\{\{([A-Za-z0-9_]+)\}\}", text)
    # Match [PLACEHOLDER]
    matches_bracket = re.findall(r"\[([A-Za-z0-9_]+)\]", text)
    
    unique = list(set(matches_curly + matches_bracket))
    return sorted(unique)

@app.post("/api/templates/parse")
async def parse_template_file(
    file: UploadFile = File(None),
    text: str = Form(None),
    user: User = Depends(get_current_user)
):
    extracted_text = ""
    if file:
        filename = file.filename.lower()
        if filename.endswith(".docx"):
            import docx
            try:
                import io
                contents = await file.read()
                doc = docx.Document(io.BytesIO(contents))
                paragraphs_text = [p.text for p in doc.paragraphs]
                for table in doc.tables:
                    for row in table.rows:
                        for cell in row.cells:
                            paragraphs_text.append(cell.text)
                extracted_text = "\n".join(paragraphs_text)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Failed to parse DOCX file: {e}")
        elif filename.endswith(".pdf"):
            try:
                import io
                contents = await file.read()
                reader = PdfReader(io.BytesIO(contents))
                pages_text = []
                for page in reader.pages:
                    txt = page.extract_text()
                    if txt:
                        pages_text.append(txt)
                extracted_text = "\n".join(pages_text)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Failed to parse PDF file: {e}")
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload a .docx or .pdf file.")
    elif text:
        extracted_text = text
    else:
        raise HTTPException(status_code=400, detail="No file or text provided for parsing.")

    placeholders = extract_placeholders(extracted_text)
    return {
        "text": extracted_text,
        "placeholders": placeholders
    }

@app.get("/api/templates")
def get_templates(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    customs = db.query(Template).filter(Template.user_id == user.id).order_by(Template.created_at.desc()).all()
    result = []
    for c in customs:
        result.append({
            "id": c.id,
            "title": c.title,
            "description": c.description,
            "content": c.content,
            "placeholders": json.loads(c.placeholders) if c.placeholders else [],
            "has_file": c.has_file,
            "file_path": c.file_path,
            "is_custom": True
        })
    return result

@app.post("/api/templates")
async def create_template(
    title: str = Form(...),
    description: str = Form(""),
    content: str = Form(""),
    placeholders: str = Form("[]"),
    file: UploadFile = File(None),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    templates_dir = os.path.join(data_dir(), "templates")
    os.makedirs(templates_dir, exist_ok=True)
    
    file_path = None
    has_file = 0
    parsed_placeholders = json.loads(placeholders)
    
    if file:
        has_file = 1
        filename = file.filename.lower()
        unique_prefix = str(uuid.uuid4())[:8]
        safe_filename = f"user_template_{user.id}_{unique_prefix}_{file.filename}"
        file_path = os.path.join(templates_dir, safe_filename)
        
        file_contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(file_contents)
            
        if not content:
            import io
            if filename.endswith(".docx"):
                try:
                    doc = docx.Document(io.BytesIO(file_contents))
                    content = "\n".join([p.text for p in doc.paragraphs])
                except Exception:
                    pass
            elif filename.endswith(".pdf"):
                try:
                    reader = PdfReader(io.BytesIO(file_contents))
                    content = "\n".join([page.extract_text() or "" for page in reader.pages])
                except Exception:
                    pass

    new_template = Template(
        user_id=user.id,
        title=title,
        description=description,
        content=content,
        placeholders=json.dumps(parsed_placeholders),
        file_path=file_path,
        has_file=has_file
    )
    db.add(new_template)
    db.commit()
    db.refresh(new_template)
    
    create_notification_record(
        db,
        user.id,
        title="Custom Template Added",
        desc=f"Template \"{title}\" has been successfully created and registered."
    )

    return {
        "id": new_template.id,
        "title": new_template.title,
        "description": new_template.description,
        "placeholders": parsed_placeholders,
        "has_file": new_template.has_file
    }

@app.delete("/api/templates/{template_id}")
def delete_template(template_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tmpl = db.query(Template).filter(Template.id == template_id, Template.user_id == user.id).first()
    if not tmpl:
        raise HTTPException(status_code=404, detail="Template not found.")
        
    if tmpl.file_path and os.path.exists(tmpl.file_path):
        try: os.remove(tmpl.file_path)
        except Exception: pass
        
    db.delete(tmpl)
    db.commit()
    return {"status": "success", "detail": "Template deleted successfully."}


# --- TENANTS ENDPOINTS ---

@app.get("/api/tenants")
def get_tenants(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tenants = db.query(Tenant).filter(Tenant.user_id == user.id).order_by(Tenant.name.asc()).all()
    result = []
    for t in tenants:
        result.append({
            "id": t.id,
            "name": t.name,
            "phone": t.phone,
            "email": t.email,
            "guardian": t.guardian,
            "age": t.age,
            "address": t.address,
            "aadhar": t.aadhar,
            "created_at": t.created_at.isoformat()
        })
    return result

@app.post("/api/tenants")
def create_tenant(payload: TenantCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    t = Tenant(
        user_id=user.id,
        name=payload.name,
        phone=payload.phone,
        email=payload.email,
        guardian=payload.guardian,
        age=payload.age,
        address=payload.address,
        aadhar=payload.aadhar
    )
    db.add(t)
    db.commit()
    db.refresh(t)
    
    # Save a notification
    create_notification_record(
        db,
        user.id,
        title="Tenant Registered",
        desc=f"Tenant \"{t.name}\" has been successfully added to your registry."
    )
    
    return {
        "id": t.id,
        "name": t.name,
        "phone": t.phone,
        "email": t.email,
        "guardian": t.guardian,
        "age": t.age,
        "address": t.address,
        "aadhar": t.aadhar,
        "created_at": t.created_at.isoformat()
    }

@app.put("/api/tenants/{tenant_id}")
def update_tenant(tenant_id: int, payload: TenantCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    t = db.query(Tenant).filter(Tenant.id == tenant_id, Tenant.user_id == user.id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Tenant not found.")
    
    t.name = payload.name
    t.phone = payload.phone
    t.email = payload.email
    t.guardian = payload.guardian
    t.age = payload.age
    t.address = payload.address
    t.aadhar = payload.aadhar
    
    db.commit()
    db.refresh(t)
    return {
        "id": t.id,
        "name": t.name,
        "phone": t.phone,
        "email": t.email,
        "guardian": t.guardian,
        "age": t.age,
        "address": t.address,
        "aadhar": t.aadhar,
        "created_at": t.created_at.isoformat()
    }

@app.delete("/api/tenants/{tenant_id}")
def delete_tenant(tenant_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    t = db.query(Tenant).filter(Tenant.id == tenant_id, Tenant.user_id == user.id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Tenant not found.")
    
    db.delete(t)
    db.commit()
    return {"status": "success", "detail": "Tenant deleted successfully."}


# --- OWNERS ENDPOINTS ---

@app.get("/api/owners")
def get_owners(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    owners = db.query(Owner).filter(Owner.user_id == user.id).order_by(Owner.name.asc()).all()
    result = []
    for o in owners:
        result.append({
            "id": o.id,
            "name": o.name,
            "phone": o.phone,
            "email": o.email,
            "guardian": o.guardian,
            "age": o.age,
            "address": o.address,
            "created_at": o.created_at.isoformat()
        })
    return result

@app.post("/api/owners")
def create_owner(payload: OwnerCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    o = Owner(
        user_id=user.id,
        name=payload.name,
        phone=payload.phone,
        email=payload.email,
        guardian=payload.guardian,
        age=payload.age,
        address=payload.address
    )
    db.add(o)
    db.commit()
    db.refresh(o)
    
    # Save a notification
    create_notification_record(
        db,
        user.id,
        title="Owner Registered",
        desc=f"Owner \"{o.name}\" has been successfully added to your registry."
    )
    
    return {
        "id": o.id,
        "name": o.name,
        "phone": o.phone,
        "email": o.email,
        "guardian": o.guardian,
        "age": o.age,
        "address": o.address,
        "created_at": o.created_at.isoformat()
    }

@app.put("/api/owners/{owner_id}")
def update_owner(owner_id: int, payload: OwnerCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    o = db.query(Owner).filter(Owner.id == owner_id, Owner.user_id == user.id).first()
    if not o:
        raise HTTPException(status_code=404, detail="Owner not found.")
    
    o.name = payload.name
    o.phone = payload.phone
    o.email = payload.email
    o.guardian = payload.guardian
    o.age = payload.age
    o.address = payload.address
    
    db.commit()
    db.refresh(o)
    return {
        "id": o.id,
        "name": o.name,
        "phone": o.phone,
        "email": o.email,
        "guardian": o.guardian,
        "age": o.age,
        "address": o.address,
        "created_at": o.created_at.isoformat()
    }

@app.delete("/api/owners/{owner_id}")
def delete_owner(owner_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    o = db.query(Owner).filter(Owner.id == owner_id, Owner.user_id == user.id).first()
    if not o:
        raise HTTPException(status_code=404, detail="Owner not found.")
    
    db.delete(o)
    db.commit()
    return {"status": "success", "detail": "Owner deleted successfully."}


# --- PROPERTIES ENDPOINTS ---

@app.get("/api/properties")
def get_properties(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    properties = db.query(Property).filter(Property.user_id == user.id).order_by(Property.name.asc()).all()
    result = []
    for p in properties:
        result.append({
            "id": p.id,
            "name": p.name,
            "address": p.address,
            "description": p.description,
            "business_name": p.business_name,
            "created_at": p.created_at.isoformat()
        })
    return result

@app.post("/api/properties")
def create_property(payload: PropertyCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    p = Property(
        user_id=user.id,
        name=payload.name,
        address=payload.address,
        description=payload.description,
        business_name=payload.business_name
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    
    # Save a notification
    create_notification_record(
        db,
        user.id,
        title="Property Registered",
        desc=f"Property asset \"{p.name}\" has been successfully added to your registry."
    )
    
    return {
        "id": p.id,
        "name": p.name,
        "address": p.address,
        "description": p.description,
        "business_name": p.business_name,
        "created_at": p.created_at.isoformat()
    }

@app.put("/api/properties/{property_id}")
def update_property(property_id: int, payload: PropertyCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    p = db.query(Property).filter(Property.id == property_id, Property.user_id == user.id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Property not found.")
    
    p.name = payload.name
    p.address = payload.address
    p.description = payload.description
    p.business_name = payload.business_name
    
    db.commit()
    db.refresh(p)
    return {
        "id": p.id,
        "name": p.name,
        "address": p.address,
        "description": p.description,
        "business_name": p.business_name,
        "created_at": p.created_at.isoformat()
    }

@app.delete("/api/properties/{property_id}")
def delete_property(property_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    p = db.query(Property).filter(Property.id == property_id, Property.user_id == user.id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Property not found.")
    
    db.delete(p)
    db.commit()
    return {"status": "success", "detail": "Property deleted successfully."}


# Serve Static files at root
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
