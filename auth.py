from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import base64
import secrets

# Configuration
SECRET_KEY = "super_secret_`key"
TOKEN_EXPIRATION_MINUTES = 30


# Function to generate a hashed password
def hash_password(password: str) -> str:
    """Hash a password using HMAC and SHA256."""
    return hmac.new(SECRET_KEY.encode(), password.encode(), hashlib.sha256).hexdigest()


# Function to verify a hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify that a plain password matches a hashed password."""
    return hmac.compare_digest(hash_password(plain_password), hashed_password)


# Function to create a token
def create_token(user_id: str) -> str:
    """Create a basic token with user_id and expiration time."""
    expiration = (datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRATION_MINUTES)).isoformat()
    token_data = f"{user_id}:{expiration}"
    token = base64.urlsafe_b64encode(token_data.encode()).decode()
    signature = hmac.new(SECRET_KEY.encode(), token.encode(), hashlib.sha256).hexdigest()
    return f"{token}.{signature}"


# Function to decode and verify a token
def decode_token(token: str) -> str:
    """Decode and verify a token."""
    try:
        token, signature = token.rsplit(".", 1)
        valid_signature = hmac.new(SECRET_KEY.encode(), token.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(valid_signature, signature):
            raise ValueError("Invalid token signature")

        user_id, expiration = base64.urlsafe_b64decode(token).decode().split(":")
        if datetime.now(timezone.utc) > datetime.fromisoformat(expiration):
            raise ValueError("Token expired")

        return user_id
    except Exception as e:
        return "Problem while decoding token: " + str(e)
