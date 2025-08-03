import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

security = HTTPBearer()

def _config():
    """Read Keycloak configuration from environment at runtime."""
    public_key = os.getenv("KEYCLOAK_PUBLIC_KEY", "")
    algorithms = [os.getenv("KEYCLOAK_ALGORITHM", "RS256")]
    audience = os.getenv("KEYCLOAK_CLIENT_ID", "gateway-client")
    return public_key, algorithms, audience


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify incoming JWT using Keycloak public key.

    Raises HTTPException if token is invalid. Returns token payload otherwise.
    """
    token = credentials.credentials
    public_key, algorithms, audience = _config()
    if not public_key:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Missing public key")
    try:
        payload = jwt.decode(token, public_key, algorithms=algorithms, audience=audience)
    except JWTError as exc:  # pragma: no cover - error path
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc
    return payload
