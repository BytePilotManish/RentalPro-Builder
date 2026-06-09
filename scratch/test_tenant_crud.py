import json
from database import SessionLocal, User, Tenant

def test_tenant_backend():
    db = SessionLocal()
    try:
        # Fetch the admin user
        admin = db.query(User).filter(User.email == "admin@rentalpro.com").first()
        if not admin:
            print("[ERROR] Admin user not found.")
            return

        print("=== Backend Verification: Tenant CRUD ===")
        # 1. Create a tenant
        test_tenant = Tenant(
            user_id=admin.id,
            name="Mr. VERIFIED TENANT",
            phone="+91 9900881122",
            email="verified@tenant.com",
            guardian="S/O Test Father",
            age=32,
            address="Tenant Address Street 10",
            aadhar="1234-5678-9012"
        )
        db.add(test_tenant)
        db.commit()
        db.refresh(test_tenant)
        print(f"[OK] Created Tenant ID: {test_tenant.id}, Name: {test_tenant.name}")

        # 2. Query/Read
        fetched = db.query(Tenant).filter(Tenant.id == test_tenant.id).first()
        assert fetched is not None
        assert fetched.phone == "+91 9900881122"
        print(f"[OK] Fetched Tenant phone: {fetched.phone}")

        # 3. Update
        fetched.name = "Mr. UPDATED TENANT"
        db.commit()
        db.refresh(fetched)
        assert fetched.name == "Mr. UPDATED TENANT"
        print(f"[OK] Updated Tenant name to: {fetched.name}")

        # 4. Delete
        db.delete(fetched)
        db.commit()
        deleted = db.query(Tenant).filter(Tenant.id == test_tenant.id).first()
        assert deleted is None
        print("[OK] Deleted Tenant successfully")

    finally:
        db.close()

if __name__ == "__main__":
    test_tenant_backend()
