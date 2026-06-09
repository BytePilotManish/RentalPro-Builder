import os
import json
import shutil
import requests

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print("=== Testing Settings & Output Directory API ===")
    
    # 1. Login to get token
    login_url = f"{BASE_URL}/api/auth/login"
    login_payload = {"email": "admin@rentalpro.com", "password": "admin123"}
    try:
        res = requests.post(login_url, json=login_payload)
        res.raise_for_status()
        token = res.json()["token"]
        print("[OK] JWT Token obtained successfully.")
    except Exception as e:
        print(f"[FAIL] Login failed: {e}")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Get profile before setting custom output_dir
    me_url = f"{BASE_URL}/api/auth/me"
    try:
        res = requests.get(me_url, headers=headers)
        res.raise_for_status()
        profile = res.json()
        print(f"[OK] Profile fetched. Current output_dir: {profile.get('output_dir')}")
    except Exception as e:
        print(f"[FAIL] Fetch profile failed: {e}")
        return

    # 3. Create a temporary folder for custom output
    custom_dir = os.path.abspath("scratch/test_output_dir")
    if os.path.exists(custom_dir):
        shutil.rmtree(custom_dir)
    
    # 4. Save settings with custom_dir
    settings_url = f"{BASE_URL}/api/settings"
    try:
        res = requests.put(settings_url, json={"output_dir": custom_dir}, headers=headers)
        res.raise_for_status()
        save_resp = res.json()
        print(f"[OK] PUT /api/settings successful. Response: {save_resp}")
    except Exception as e:
        print(f"[FAIL] PUT /api/settings failed: {e}")
        return

    # 5. Fetch profile to verify setting was persisted
    try:
        res = requests.get(me_url, headers=headers)
        res.raise_for_status()
        profile = res.json()
        if profile.get("output_dir") == custom_dir:
            print(f"[OK] Verified output_dir persisted correctly: {profile.get('output_dir')}")
        else:
            print(f"[FAIL] Expected output_dir '{custom_dir}', got '{profile.get('output_dir')}'")
            return
    except Exception as e:
        print(f"[FAIL] Fetch profile check failed: {e}")
        return

    # 6. Generate an agreement to test path output redirection
    agreements_url = f"{BASE_URL}/api/agreements"
    agreement_payload = {
        "title": "API Settings Test Agreement",
        "data": {
            "AGREEMENT_DATE": "08th June 2026",
            "AGREEMENT_PLACE": "Test City",
            "OWNER_NAME": "Test Landlord",
            "OWNER_PARENT": "Test Parent",
            "OWNER_AGE": "45",
            "OWNER_ADDRESS": "123 Landlord Lane",
            "TENANT_NAME": "Test Tenant",
            "TENANT_PARENT": "Tenant Parent",
            "TENANT_AGE": "30",
            "TENANT_ADDRESS": "456 Tenant Road",
            "BUSINESS_NAME": "Test Shop",
            "PREMISES_ADDRESS": "789 Commercial Block",
            "PREMISES_DESCRIPTION": "Retail Space 10A",
            "LEASE_PERIOD": "11 Months",
            "LEASE_PERIOD_NUM": "11",
            "LEASE_END_DATE": "07th May 2027",
            "RENT_AMOUNT": "15,000",
            "RENT_AMOUNT_WORDS": "Fifteen Thousand",
            "RENT_PAYMENT_DAY": "5th",
            "ESCALATION_RATE": "5%",
            "DEPOSIT_AMOUNT": "50,000",
            "DEPOSIT_AMOUNT_WORDS": "Fifty Thousand",
            "DEPOSIT_MODE": "Cheque",
            "NOTICE_PERIOD": "1 Month",
            "OWNER_SIG_NAMES": "Test Landlord",
            "TENANT_SIG_NAMES": "Test Tenant",
            "WITNESS_1_NAME": "Witness A",
            "WITNESS_1_ADDRESS": "Witness A Road",
            "WITNESS_2_NAME": "Witness B",
            "WITNESS_2_ADDRESS": "Witness B Road"
        }
    }
    
    try:
        res = requests.post(agreements_url, json=agreement_payload, headers=headers)
        res.raise_for_status()
        agreement_resp = res.json()
        print(f"[OK] Agreement created successfully. ID: {agreement_resp.get('id')}")
        
        # Verify physical files exist in the custom_dir
        # Let's inspect custom_dir files
        files = os.listdir(custom_dir)
        print(f"Files found in custom directory: {files}")
        
        docx_found = any(f.endswith(".docx") for f in files)
        pdf_found = any(f.endswith(".pdf") for f in files)
        
        if docx_found and pdf_found:
            print("[OK] Verified both .docx and .pdf files were generated in custom output directory!")
        else:
            print(f"[FAIL] Missing files in custom directory. Found: {files}")
            
        # Clean up database record
        del_url = f"{BASE_URL}/api/agreements/{agreement_resp.get('id')}"
        requests.delete(del_url, headers=headers)
        print("[OK] Cleaned up test agreement record.")
        
    except Exception as e:
        print(f"[FAIL] Agreement creation/generation test failed: {e}")
        return

    # 7. Clean up Settings (reset output_dir to None)
    try:
        res = requests.put(settings_url, json={"output_dir": ""}, headers=headers)
        res.raise_for_status()
        print("[OK] Reset user output_dir back to default.")
    except Exception as e:
        print(f"[FAIL] Reset settings failed: {e}")

    # Remove temporary folder
    try:
        shutil.rmtree(custom_dir)
        print("[OK] Cleaned up temporary directory.")
    except Exception:
        pass

if __name__ == "__main__":
    run_tests()
