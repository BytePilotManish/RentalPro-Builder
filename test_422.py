import requests

def test_login():
    login_url = "http://127.0.0.1:8000/api/auth/login"
    login_payload = {
        "email": "admin@rentalpro.com",
        "password": "admin123"
    }
    r = requests.post(login_url, json=login_payload)
    return r.json().get("token")

def test_fields():
    token = test_login()
    url = "http://127.0.0.1:8000/api/fields"
    r = requests.get(url)
    fields_data = r.json()
    
    # Construct default payload
    data = {}
    for cat in fields_data.values():
        for key, field in cat["fields"].items():
            data[key] = field["default"]
            
    payload = {
        "title": "Test Default Agreement",
        "data": data
    }
    
    post_url = "http://127.0.0.1:8000/api/agreements"
    headers = {"Authorization": f"Bearer {token}"}
    
    res = requests.post(post_url, json=payload, headers=headers)
    print("STATUS:", res.status_code)
    try:
        print("RESPONSE:", res.json())
    except:
        print("RESPONSE TEXT:", res.text)

if __name__ == "__main__":
    test_fields()
