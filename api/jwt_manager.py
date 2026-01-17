from fastapi import Depends, HTTPException, Header
import jwt
import os

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "secret-key-to-change")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 1

def verify_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    try:
        # Expected format: "Bearer <token>"
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Admin role verification dependency
def verify_admin(current_user: dict = Depends(verify_token)):
    if "ROLE_ADMIN" not in current_user.get("roles", []):
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user