import requests

BASE_URL = "http://127.0.0.1:8000"

def test_settings_update():
    print("=== Testing User Name & Password Settings Update API ===")
    
    # 1. Login with original credentials
    login_url = f"{BASE_URL}/api/auth/login"
    login_payload = {"email": "admin@rentalpro.com", "password": "admin123"}
    try:
        res = requests.post(login_url, json=login_payload)
        res.raise_for_status()
        token = res.json()["token"]
        original_name = res.json()["user"]["full_name"]
        print(f"[OK] Logged in. Original name: '{original_name}'")
    except Exception as e:
        print(f"[FAIL] Initial login failed: {e}")
        return

    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Update settings: Change Name and Password
    settings_url = f"{BASE_URL}/api/settings"
    test_name = "Admin User - Updated Name"
    test_password = "admin123_new"
    
    update_payload = {
        "full_name": test_name,
        "password": test_password
    }
    
    try:
        res = requests.put(settings_url, json=update_payload, headers=headers)
        res.raise_for_status()
        resp = res.json()
        print(f"[OK] PUT /api/settings returned: {resp}")
    except Exception as e:
        print(f"[FAIL] Settings update API request failed: {e}")
        return

    # 3. Fetch profile with old token to verify name update
    me_url = f"{BASE_URL}/api/auth/me"
    try:
        res = requests.get(me_url, headers=headers)
        res.raise_for_status()
        profile = res.json()
        if profile.get("full_name") == test_name:
            print(f"[OK] Verified user full_name was updated to: '{test_name}'")
        else:
            print(f"[FAIL] Expected full_name '{test_name}', got '{profile.get('full_name')}'")
            return
    except Exception as e:
        print(f"[FAIL] Fetching profile failed: {e}")
        return

    # 4. Try logging in with the new password
    print("Checking login with the new password...")
    new_login_payload = {"email": "admin@rentalpro.com", "password": test_password}
    try:
        res = requests.post(login_url, json=new_login_payload)
        res.raise_for_status()
        new_token = res.json()["token"]
        print("[OK] Successfully logged in with the new password!")
    except Exception as e:
        print(f"[FAIL] Login with new password failed: {e}")
        return

    # 5. Revert settings using the new token
    new_headers = {"Authorization": f"Bearer {new_token}"}
    revert_payload = {
        "full_name": original_name,
        "password": "admin123"
    }
    
    try:
        res = requests.put(settings_url, json=revert_payload, headers=new_headers)
        res.raise_for_status()
        print("[OK] Reverted name and password settings back to original defaults.")
    except Exception as e:
        print(f"[FAIL] Reverting settings failed: {e}")
        return

    # 6. Verify original credentials work again
    print("Verifying original credentials work again...")
    try:
        res = requests.post(login_url, json=login_payload)
        res.raise_for_status()
        print("[OK] Successfully verified original login credentials after reversion!")
    except Exception as e:
        print(f"[FAIL] Re-login verification failed: {e}")
        return

    print("=== All settings update API tests passed! ===")

if __name__ == "__main__":
    test_settings_update()
