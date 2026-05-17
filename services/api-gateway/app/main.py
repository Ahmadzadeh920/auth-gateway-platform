from fastapi import FastAPI, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordBearer
from fastapi.routing import APIRoute
from jose import jwt
import httpx
import logging


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

KEYCLOAK_URL = "http://keycloak:8080"
REALM = "AdrinaopsClient"


KEYCLOAK_EXTERNAL_URL = "http://localhost:8088/keycloak" 
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

async def verify_token(token: str = Depends(oauth2_scheme)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{KEYCLOAK_URL}/realms/{REALM}")
        realm_data = response.json()

    public_key = "-----BEGIN PUBLIC KEY-----\n" + realm_data["public_key"] + "\n-----END PUBLIC KEY-----"

    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience="account"   # IMPORTANT: this should NOT be "preferred_username"
        )
        return payload

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Dependency to get and verify the current user from a Bearer token."""
    return await verify_jwt_token(token)

@app.get("/secure-endpoint")
async def secure_endpoint(user=Depends(get_current_user)):
    """An example secure endpoint demonstrating direct use of token verification."""
    return {"message": "Welcome to a secure API endpoint!", "user": user}



async def verify_jwt_token(token: str):
    """
    Decodes and verifies a JWT token using Keycloak's public key.
    Raises HTTPException 401 on failure.
    """
    try:
        public_key = await get_public_key()
        
        # IMPORTANT: 'audience' should match the 'aud' claim in your JWT.
        # Common values are 'account' for default Keycloak client tokens,
        # or the specific client ID if you configured it as such.
        # Check your JWT payload (e.g., using jwt.io) to confirm the 'aud' claim.
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience="account", # Adjust this if your client's 'aud' claim is different
            options={"verify_signature": True, "verify_aud": True, "exp": True}
        )
        log.info(f"Token validated for user: {payload.get('preferred_username', 'N/A')}")
        return payload
    except jwt.ExpiredSignatureError:
        log.warning("Token expired.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.JWTError as e:
        log.warning(f"Invalid token signature or claims: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {e}")
    except HTTPException: # Re-raise HTTPExceptions from get_public_key
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token verification failed: {e}")

# This dependency is useful for other API endpoints within this middleware
# if they also need to be protected and accept Bearer tokens directly.


@app.get("/verify")
async def verify_for_traefik(request: Request):
    """
    This is the endpoint Traefik's forwardAuth will hit.
    It expects a Bearer token in the Authorization header.
    Returns 200 if valid, 401 if not.
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        log.warning("Authorization header missing or malformed.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing or malformed (expected 'Bearer <token>')",
            headers={"WWW-Authenticate": "Bearer"}, # This header tells clients how to authenticate
        )
    
    token = auth_header.split(" ")[1] # Extract the token part

    # Now, try to verify the token
    try:
        payload = await verify_jwt_token(token)
        # If no exception, token is valid. Return 200 OK.
        # Optionally, you can pass user info back to the backend service via headers
        # These headers would be configured in Traefik's forwardAuth
        response = Response(status_code=200)
        # Example: Add custom headers from the JWT payload
        response.headers["X-User-ID"] = payload.get("sub", "")
        response.headers["X-User-Preferred-Username"] = payload.get("preferred_username", "")
        response.headers["X-User-Roles"] = ",".join(payload.get("realm_access", {}).get("roles", []))
        return response
    except HTTPException as e:
        # verify_jwt_token already raises 401 with appropriate detail
        # Re-raise it, FastAPI will handle converting it to a response
        log.info(f"Token verification failed for Traefik: {e.detail}")
        raise e
    except Exception as e:
        # Catch any other unexpected errors during the /verify process
        log.error(f"Unexpected error in /verify endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error during verification: {e}")

@app.get("/")
def read_root(request: Request):
    url_list = []
    for route in app.routes:
        # Check if it's an API route (to exclude internal websocket/mount routes if any)
        if isinstance(route, APIRoute): 
            url_list.append({
                "path": route.path,
                "methods": list(route.methods)
            })
    return {"message": "Hello from Auth middelware", "endpoints": url_list}