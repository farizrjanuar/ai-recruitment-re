#!/usr/bin/env python3
"""
Generate secure secret keys for production deployment.
Run: python generate_secrets.py
"""
import secrets

def generate_secret_key(length=32):
    """Generate a secure random secret key."""
    return secrets.token_hex(length)

if __name__ == "__main__":
    print("=" * 60)
    print("🔐 Secret Keys for Production Deployment")
    print("=" * 60)
    print("\nCopy these to your Railway/Render environment variables:\n")
    
    print("SECRET_KEY:")
    print(generate_secret_key(32))
    print()
    
    print("JWT_SECRET_KEY:")
    print(generate_secret_key(32))
    print()
    
    print("=" * 60)
    print("⚠️  IMPORTANT: Keep these keys SECRET and SECURE!")
    print("   Never commit them to git or share publicly.")
    print("=" * 60)
