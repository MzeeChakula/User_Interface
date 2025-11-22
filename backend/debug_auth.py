#!/usr/bin/env python3
"""
Debug script to test password hashing and verification
"""
import sys
sys.path.insert(0, '/home/dev-kiran/Projects/MzeeChakula/User_Interface/backend')

from api.core.security import get_password_hash, verify_password
from api.models.database import SessionLocal
from api.models.user import UserDB

def test_password_functions():
    """Test password hashing and verification"""
    print("=" * 60)
    print("Testing Password Functions")
    print("=" * 60)
    
    # Test 1: Hash and verify a simple password
    test_password = "Test123"
    print(f"\n1. Testing with password: '{test_password}'")
    try:
        hashed = get_password_hash(test_password)
        print(f"   Hashed: {hashed[:50]}...")
        print(f"   Hash length: {len(hashed)}")
        
        # Verify the password
        is_valid = verify_password(test_password, hashed)
        print(f"   Verification: {'✓ PASS' if is_valid else '✗ FAIL'}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Check database users
    print(f"\n2. Checking database users:")
    db = SessionLocal()
    try:
        users = db.query(UserDB).all()
        print(f"   Total users in database: {len(users)}")
        
        for user in users:
            print(f"\n   User: {user.email}")
            print(f"   Hash: {user.hashed_password[:50]}...")
            print(f"   Hash length: {len(user.hashed_password)}")
            print(f"   Active: {user.is_active}")
            
            # Try to verify with a test password
            test_passwords = ["Test123", "test123", "Password123", "password123"]
            for pwd in test_passwords:
                try:
                    is_valid = verify_password(pwd, user.hashed_password)
                    if is_valid:
                        print(f"   ✓ Password '{pwd}' works!")
                except Exception as e:
                    print(f"   Error testing '{pwd}': {e}")
                    
    finally:
        db.close()

if __name__ == "__main__":
    test_password_functions()
