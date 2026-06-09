import requests
import json
import os

def test_api():
    base_url = "http://127.0.0.1:8000"
    
    # 1. Login
    login_url = f"{base_url}/api/auth/login"
    payload = {
        "email": "admin@rentalpro.com",
        "password": "admin123"
    }
    
    print("Logging in...")
    res = requests.post(login_url, json=payload)
    if res.status_code != 200:
        print(f"Login failed: {res.text}")
        return
        
    token = res.json()["token"]
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 2. Save and generate Kannada Agreement (template_id = -1)
    ag_payload = {
        "title": "API_Test_Kannada_Agreement",
        "template_id": -1,
        "data": {
            "AGREEMENT_YEAR_WORDS": "ಎರಡು ಸಾವಿರದ ಇಪ್ಪತ್ತಾರನೇ",
            "AGREEMENT_MONTH": "ಮೇ",
            "AGREEMENT_DATE": "ಹತ್ತೊಂಭತ್ತು (19-05-2026)",
            "OWNER_NAME": "ಶ್ರೀ.ಷಣ್ಮುಖಪ್ಪ.ಬಿ.ಸಿ",
            "OWNER_PARENT": "ಲೇಟ್.ಚಂದ್ರಪ್ಪ.ಬಿ",
            "OWNER_AGE": "41",
            "OWNER_ADDRESS": "ಬೆಂಗಳೂರು–562162, ಗಂಗೊಂಡನಹಳ್ಳಿ, ಲಕ್ಷ್ಮಿಪುರ ಅಂಚೆ, ಲೇಕ್ ರಸ್ತೆ, ಧರ್ಮರಾಯ ರಸ್ತೆ, 51 ನೇ ನಂಬರುಳ್ಳ ಶ್ರೀ ಭೂವರಹ ನಿಲಯ",
            "TENANT_NAME": "ಶ್ರೀಮತಿ.ಪಾರ್ವತಮ್ಮ",
            "TENANT_PARENT": "ಗಂಡ ಲೇಟ್ ರಂಗಯ್ಯ",
            "TENANT_AGE": "52",
            "TENANT_ADDRESS": "ಬೆಂಗಳೂರು–562162, ಗಂಗೊಂಡನಹಳ್ಳಿ, ಲಕ್ಷ್ಮಿಪುರ ಅಂಚೆ, ಲೇಕ್ ರಸ್ತೆ, ಧರ್ಮರಾಯ ರಸ್ತೆ, 51 ನೇ ನಂಬರುಳ್ಳ ಶ್ರೀ ಭೂವರಹ ನಿಲಯ",
            "PREMISES_ADDRESS": "ಬೆಂಗಳೂರು–562162, ಗಂಗೊಂಡನಹಳ್ಳಿ, ಲಕ್ಷ್ಮಿಪುರ ಅಂಚೆ, ಲೇಕ್ ರಸ್ತೆ, ಧರ್ಮರಾಯ ರಸ್ತೆ, 51ನೇ ನಂಬರುಳ್ಳ ಶ್ರೀ ಭೂವರಹ ನಿಲಯ",
            "PREMISES_DESCRIPTION": "ನೆಲ ಮಾಹಡಿಯಲ್ಲಿರುವ ಆರ್.ಸಿ.ಸಿ ಛಾವಣಿಯುಳ್ಳ ಪೂರ್ವದ ಬಾಗಿಲುಳ್ಳ, ಒಂದು ಅಡಿಗೆ ಮನೆ, ಒಂದು ಹಾಲ್, ಒಂದು ರೂಮ್, ಮತ್ತು ಬಾತ್ ರೂಮ್, ಶೌಚಾಲಯ, ಹಾಗೂವಿದ್ಯುತ್ ಮೀಟರ್ / ನೀರಿನ ಅನುಕೂಲವಿರುವ",
            "DEPOSIT_AMOUNT": "20,000",
            "DEPOSIT_AMOUNT_WORDS": "ಇಪ್ಪತ್ತು ಸಾವಿರ",
            "RENT_AMOUNT": "4,500",
            "RENT_AMOUNT_WORDS": "ನಾಲ್ಕು ಸಾವಿರದ ಐನೂರು",
            "RENT_PAYMENT_DAY": "28",
            "LEASE_START_DATE": "15-01-2026",
            "LEASE_PERIOD_NUM": "11",
            "LEASE_PERIOD": "ಹನ್ನೊಂದು",
            "ESCALATION_RATE": "5%",
            "NOTICE_PERIOD_NUM": "3",
            "NOTICE_PERIOD": "ಮೂರು",
            "OWNER_SIG_NAMES": "ಷಣ್ಮುಖಪ್ಪ.ಬಿ.ಸಿ",
            "TENANT_SIG_NAMES": "ಪಾರ್ವತಮ್ಮ",
            "SERVICE_FEE": "500"
        }
    }
    
    print("Generating Kannada agreement...")
    gen_url = f"{base_url}/api/agreements"
    res = requests.post(gen_url, json=ag_payload, headers=headers)
    if res.status_code != 200:
        print(f"Agreement generation failed: {res.text}")
        return
        
    data = res.json()
    print("Generation Success!")
    print(f"  Agreement ID: {data['id']}")
    print(f"  DOCX Url: {data['docxUrl']}")
    print(f"  PDF Url: {data['pdfUrl']}")
    
    # Check if files exist
    list_url = f"{base_url}/api/agreements"
    res = requests.get(list_url, headers=headers)
    agreements = res.json()
    for ag in agreements:
        if ag["id"] == data["id"]:
            print(f"Found record in database!")
            break
            
if __name__ == "__main__":
    test_api()
