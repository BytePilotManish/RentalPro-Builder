import json
import requests
from database import SessionLocal, User, Owner, Property

def test_owners_properties_backend():
    db = SessionLocal()
    try:
        # Fetch the admin user
        admin = db.query(User).filter(User.email == "admin@rentalpro.com").first()
        if not admin:
            print("[ERROR] Admin user not found.")
            return

        print("=== Backend Verification: Owners DB CRUD ===")
        # 1. Create an Owner
        test_owner = Owner(
            user_id=admin.id,
            name="Mr. TEST OWNER",
            phone="+91 9900001111",
            email="testowner@example.com",
            guardian="S/O Test Guardian",
            age=45,
            address="Owner Mansion, City Center"
        )
        db.add(test_owner)
        db.commit()
        db.refresh(test_owner)
        print(f"[OK] Created Owner ID: {test_owner.id}, Name: {test_owner.name}")

        # 2. Query/Read
        fetched_owner = db.query(Owner).filter(Owner.id == test_owner.id).first()
        assert fetched_owner is not None
        assert fetched_owner.phone == "+91 9900001111"
        print(f"[OK] Fetched Owner phone: {fetched_owner.phone}")

        # 3. Update
        fetched_owner.name = "Mr. UPDATED OWNER"
        db.commit()
        db.refresh(fetched_owner)
        assert fetched_owner.name == "Mr. UPDATED OWNER"
        print(f"[OK] Updated Owner name to: {fetched_owner.name}")

        # 4. Delete
        db.delete(fetched_owner)
        db.commit()
        deleted_owner = db.query(Owner).filter(Owner.id == test_owner.id).first()
        assert deleted_owner is None
        print("[OK] Deleted Owner successfully")

        print("\n=== Backend Verification: Properties DB CRUD ===")
        # 1. Create a Property
        test_property = Property(
            user_id=admin.id,
            name="Premium Test Villa 101",
            address="Green Meadows Sector 4",
            description="Premium 3 BHK Villa with amenities",
            business_name="Green Meadows Properties"
        )
        db.add(test_property)
        db.commit()
        db.refresh(test_property)
        print(f"[OK] Created Property ID: {test_property.id}, Name: {test_property.name}")

        # 2. Query/Read
        fetched_prop = db.query(Property).filter(Property.id == test_property.id).first()
        assert fetched_prop is not None
        assert fetched_prop.address == "Green Meadows Sector 4"
        print(f"[OK] Fetched Property address: {fetched_prop.address}")

        # 3. Update
        fetched_prop.name = "Updated Premium Villa 101"
        db.commit()
        db.refresh(fetched_prop)
        assert fetched_prop.name == "Updated Premium Villa 101"
        print(f"[OK] Updated Property name to: {fetched_prop.name}")

        # 4. Delete
        db.delete(fetched_prop)
        db.commit()
        deleted_prop = db.query(Property).filter(Property.id == test_property.id).first()
        assert deleted_prop is None
        print("[OK] Deleted Property successfully")

    finally:
        db.close()

def test_rest_api_endpoints():
    print("\n=== REST API Endpoints Verification ===")
    
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
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # --- OWNERS API TEST ---
    print("\n--- Testing Owner API Endpoints ---")
    owner_payload = {
        "name": "API Test Landlord",
        "phone": "+91 9876543210",
        "email": "apilandlord@example.com",
        "guardian": "W/O Previous Owner",
        "age": 55,
        "address": "API Heights, Floor 5"
    }
    
    # POST /api/owners
    res = requests.post("http://127.0.0.1:8000/api/owners", json=owner_payload, headers=headers, timeout=5)
    assert res.status_code == 200, f"POST owner failed: {res.text}"
    owner_data = res.json()
    owner_id = owner_data["id"]
    print(f"[OK] POST /api/owners successful. Created owner ID: {owner_id}")
    
    # GET /api/owners
    res = requests.get("http://127.0.0.1:8000/api/owners", headers=headers, timeout=5)
    assert res.status_code == 200, f"GET owners failed: {res.text}"
    owners_list = res.json()
    assert any(o["id"] == owner_id for o in owners_list), "Created owner not in owners list"
    print(f"[OK] GET /api/owners list verified. Contains Owner {owner_id}")
    
    # PUT /api/owners/{id}
    owner_payload["name"] = "API Test Landlord UPDATED"
    res = requests.put(f"http://127.0.0.1:8000/api/owners/{owner_id}", json=owner_payload, headers=headers, timeout=5)
    assert res.status_code == 200, f"PUT owner failed: {res.text}"
    assert res.json()["name"] == "API Test Landlord UPDATED", "Update did not reflect"
    print(f"[OK] PUT /api/owners/{owner_id} successful.")
    
    # DELETE /api/owners/{id}
    res = requests.delete(f"http://127.0.0.1:8000/api/owners/{owner_id}", headers=headers, timeout=5)
    assert res.status_code == 200, f"DELETE owner failed: {res.text}"
    print(f"[OK] DELETE /api/owners/{owner_id} successful.")
    
    # --- PROPERTIES API TEST ---
    print("\n--- Testing Property API Endpoints ---")
    property_payload = {
        "name": "API Test Property Asset",
        "address": "API Avenue, Sector 99",
        "description": "Commercial space with office setup",
        "business_name": "API Office Ventures"
    }
    
    # POST /api/properties
    res = requests.post("http://127.0.0.1:8000/api/properties", json=property_payload, headers=headers, timeout=5)
    assert res.status_code == 200, f"POST property failed: {res.text}"
    prop_data = res.json()
    prop_id = prop_data["id"]
    print(f"[OK] POST /api/properties successful. Created property ID: {prop_id}")
    
    # GET /api/properties
    res = requests.get("http://127.0.0.1:8000/api/properties", headers=headers, timeout=5)
    assert res.status_code == 200, f"GET properties failed: {res.text}"
    props_list = res.json()
    assert any(p["id"] == prop_id for p in props_list), "Created property not in properties list"
    print(f"[OK] GET /api/properties list verified. Contains Property {prop_id}")
    
    # PUT /api/properties/{id}
    property_payload["name"] = "API Test Property Asset UPDATED"
    res = requests.put(f"http://127.0.0.1:8000/api/properties/{prop_id}", json=property_payload, headers=headers, timeout=5)
    assert res.status_code == 200, f"PUT property failed: {res.text}"
    assert res.json()["name"] == "API Test Property Asset UPDATED", "Update did not reflect"
    print(f"[OK] PUT /api/properties/{prop_id} successful.")
    
    # DELETE /api/properties/{id}
    res = requests.delete(f"http://127.0.0.1:8000/api/properties/{prop_id}", headers=headers, timeout=5)
    assert res.status_code == 200, f"DELETE property failed: {res.text}"
    print(f"[OK] DELETE /api/properties/{prop_id} successful.")

if __name__ == "__main__":
    test_owners_properties_backend()
    test_rest_api_endpoints()
