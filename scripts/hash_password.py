#!/usr/bin/env python3
"""
Generate argon2 password hash for admin authentication
Usage: python scripts/hash_password.py
"""

from argon2 import PasswordHasher
import getpass


def main():
    print("=" * 50)
    print("Admin Password Hash Generator")
    print("=" * 50)
    print("\nThis script generates an argon2 password hash")
    print("for use in the ADMIN_PASSWORD_HASH environment variable.\n")
    
    # Get password from user
    while True:
        password = getpass.getpass("Enter admin password: ")
        confirm = getpass.getpass("Confirm password: ")
        
        if password == confirm:
            if len(password) < 8:
                print("\n❌ Password must be at least 8 characters long.\n")
                continue
            break
        else:
            print("\n❌ Passwords do not match. Please try again.\n")
    
    # Generate hash
    ph = PasswordHasher()
    password_hash = ph.hash(password)
    
    # Display results
    print("\n" + "=" * 50)
    print("✓ Password hash generated successfully!")
    print("=" * 50)
    print("\nAdd this to your .env file:")
    print("-" * 50)
    print(f"ADMIN_PASSWORD_HASH={password_hash}")
    print("-" * 50)
    print("\n⚠️  Keep this hash secure and never commit it to version control!")
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
