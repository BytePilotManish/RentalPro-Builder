import requests

def test_custom_template_api():
    print("=== Testing Custom Template APIs ===")
    
    # 1. Login to obtain JWT token
    login_url = "http://127.0.0.1:8000/api/auth/login"
    login_payload = {
        "email": "admin@rentalpro.com",
        "password": "admin123"
    }
    
    try:
        login_res = requests.post(login_url, json=login_payload, timeout=5)
        if login_res.status_code != 200:
            print(f"[ERROR] API Login failed ({login_res.status_code}): {login_res.text}")
            return
        token = login_res.json().get("token")
        print("[OK] JWT Token obtained successfully.")
    except Exception as e:
        print(f"[ERROR] API Login request failed: {e}")
        return
        
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # 2. Test template parsing text
    print("\n--- Testing POST /api/templates/parse ---")
    parse_payload = {
        "text": "This is a custom template text containing {{CUSTOM_VAR1}} and [CUSTOM_VAR2] to test placeholder extraction."
    }
    try:
        res = requests.post("http://127.0.0.1:8000/api/templates/parse", data=parse_payload, headers=headers, timeout=5)
        print(f"Status Code: {res.status_code}")
        print(f"Response: {res.text}")
        assert res.status_code == 200
        data = res.json()
        assert "CUSTOM_VAR1" in data["placeholders"]
        assert "CUSTOM_VAR2" in data["placeholders"]
        print("[OK] /api/templates/parse text parsing verified successfully.")
    except Exception as e:
        print(f"[ERROR] Template parse failed: {e}")
        return
        
    # 3. Test template creation (saving)
    print("\n--- Testing POST /api/templates ---")
    save_payload = {
        "title": "API Test Custom Template",
        "description": "Custom template created via API integration test",
        "content": "This is template body with {{CUSTOM_VAR1}} and [CUSTOM_VAR2].",
        "placeholders": '["CUSTOM_VAR1", "CUSTOM_VAR2"]'
    }
    try:
        res = requests.post("http://127.0.0.1:8000/api/templates", data=save_payload, headers=headers, timeout=5)
        print(f"Status Code: {res.status_code}")
        print(f"Response: {res.text}")
        assert res.status_code == 200
        template_id = res.json()["id"]
        print(f"[OK] /api/templates creation successful. Template ID: {template_id}")
    except Exception as e:
        print(f"[ERROR] Template save failed: {e}")
        return
        
    # 4. Test GET /api/templates
    print("\n--- Testing GET /api/templates ---")
    try:
        res = requests.get("http://127.0.0.1:8000/api/templates", headers=headers, timeout=5)
        print(f"Status Code: {res.status_code}")
        templates_list = res.json()
        assert any(t["id"] == template_id for t in templates_list), "Created template not found in GET templates list"
        print("[OK] GET /api/templates list verified successfully.")
    except Exception as e:
        print(f"[ERROR] GET templates failed: {e}")
        return
        
    # 5. Test DELETE /api/templates/{id}
    print("\n--- Testing DELETE /api/templates/{id} ---")
    try:
        res = requests.delete(f"http://127.0.0.1:8000/api/templates/{template_id}", headers=headers, timeout=5)
        print(f"Status Code: {res.status_code}")
        print(f"Response: {res.text}")
        assert res.status_code == 200
        print("[OK] DELETE template successful.")
    except Exception as e:
        print(f"[ERROR] DELETE template failed: {e}")
        return

if __name__ == "__main__":
    test_custom_template_api()
