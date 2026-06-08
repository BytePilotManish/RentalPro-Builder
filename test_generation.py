import requests
import os

def test_generation():
    # 1. Login to obtain access token
    login_url = "http://127.0.0.1:8000/api/auth/login"
    login_payload = {
        "email": "admin@rentalpro.com",
        "password": "admin123"
    }
    
    print("Logging in to obtain JWT token...")
    try:
        login_res = requests.post(login_url, json=login_payload, timeout=15)
        if login_res.status_code != 200:
            print(f"[ERROR] Login failed ({login_res.status_code}): {login_res.text}")
            return False
        
        token_data = login_res.json()
        token = token_data.get("token")
        print("[OK] Logged in successfully. Token acquired.")
        
    except Exception as e:
        print("[ERROR] Login request failed:", e)
        return False
        
    # 2. Call save & generate endpoint
    url = "http://127.0.0.1:8000/api/agreements"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Payload matching SaveAgreementPayload schema
    payload = {
        "title": "Integration Test Agreement",
        "data": {
            "AGREEMENT_DATE": "12th Day of June 2026",
            "AGREEMENT_PLACE": "Bengaluru",
            "OWNER_NAME": "Test Owner Name",
            "OWNER_PARENT": "S/O Test Owner Parent",
            "OWNER_AGE": "50",
            "OWNER_ADDRESS": "123 Owner Lane, Bengaluru",
            "TENANT_NAME": "Test Tenant Name",
            "TENANT_PARENT": "S/O Test Tenant Parent",
            "TENANT_AGE": "35",
            "TENANT_ADDRESS": "456 Tenant Road, Bengaluru",
            "PREMISES_ADDRESS": "Shop No 1, Main Bazaar, Bengaluru",
            "PREMISES_DESCRIPTION": "RCC Roofed Commercial Shop Premises",
            "BUSINESS_NAME": "SUPER TRADERS",
            "LEASE_PERIOD": "eleven months",
            "LEASE_PERIOD_NUM": "11",
            "LEASE_END_DATE": "11/05/2027",
            "RENT_AMOUNT": "12,000.00",
            "RENT_AMOUNT_WORDS": "Twelve Thousand only",
            "RENT_PAYMENT_DAY": "5th",
            "ESCALATION_RATE": "10%",
            "DEPOSIT_AMOUNT": "60,000",
            "DEPOSIT_AMOUNT_WORDS": "Sixty Thousand only",
            "DEPOSIT_MODE": "bank transfer",
            "NOTICE_PERIOD": "three months",
            "OWNER_SIG_NAMES": "Test Owner Name",
            "TENANT_SIG_NAMES": "Test Tenant Name"
        }
    }
    
    print("\nSending POST request to generate document...")
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=45)
        print("Response status:", r.status_code)
        
        if r.status_code == 200:
            res_data = r.json()
            print("API Response:", res_data)
            
            # Check if output files actually exist
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # In the API response we receive docxUrl and pdfUrl which map to physical files
            # Let's inspect the files in the output directory
            output_dir = os.path.join(current_dir, "output")
            files = os.listdir(output_dir)
            
            docx_found = any(f.endswith(".docx") and "Integration_Test" in f for f in files)
            pdf_found = any(f.endswith(".pdf") and "Integration_Test" in f for f in files)
            
            print(f"Checking files in output/:\n  DOCX found: {docx_found}\n  PDF found: {pdf_found}")
            
            if docx_found and pdf_found:
                print("[SUCCESS] Integration test passed. PDF and DOCX files are present.")
                return True
            else:
                print("[ERROR] Generated files are missing from output folder.")
                return False
        else:
            print("[ERROR] API returned error:", r.text)
            return False
            
    except Exception as e:
        print("[ERROR] Connection or execution error:", e)
        return False

if __name__ == "__main__":
    test_generation()
