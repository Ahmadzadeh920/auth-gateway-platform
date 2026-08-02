from fastapi import FastAPI, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordBearer
from fastapi.routing import APIRoute
from jose import jwt
import httpx
import logging


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

KEYCLOAK_URL = "http://keycloak:8080/keycloak" 
 # This should match the internal URL of Keycloak in your Docker network
REALM = "AdrinaopsClient"


KEYCLOAK_EXTERNAL_URL = "http://localhost:8088/keycloak" 
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


async def get_public_key():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{KEYCLOAK_URL}/realms/{REALM}")
        response.raise_for_status()
        realm_data = response.json()

    return (
    "-----BEGIN PUBLIC KEY-----\n"
    + realm_data["public_key"]
    + "\n-----END PUBLIC KEY-----"
        )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Dependency to get and verify the current user from a Bearer token."""
    return await verify_jwt_token(token)



@app.get("/secure-endpoint")
async def secure_endpoint(user=Depends(get_current_user)):
    """An example secure endpoint demonstrating direct use of token verification."""
    return {"message": "Welcome to a secure API endpoint!", "user": user}



async def verify_jwt_token(token: str):

    try:
        public_key = await get_public_key()

        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience="account",
        )

        


    except jwt.ExpiredSignatureError as err:
        log.warning("Token expired")

        raise HTTPException(
            status_code=401,
            detail="Token expired" ) from err


    except jwt.JWTError as e:
        log.warning(
            "Invalid token: %s",
            e,
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        ) from e


    except httpx.HTTPError:
        log.exception(
            "Keycloak request failed"
        )

        raise HTTPException(
            status_code=503,
            detail="Authentication service unavailable"
        )


    except HTTPException:
        raise
    
    else:
        log.info(
            "Token validated for user: %s",
            payload.get("preferred_username", "N/A")
        )

        return payload


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
        response.headers["X-User-Preferred-Username"] = (payload.get("preferred_username", ""))
        response.headers["X-User-Roles"] = ",".join(
            payload.get("realm_access", {}).get("roles", [])
            )
            
    except HTTPException as e:
        # verify_jwt_token already raises 401 with appropriate detail
        # Re-raise it, FastAPI will handle converting it to a response
        log.info("Token verification failed for Traefik: %s", e.detail, )
        raise 
    except Exception:
        # Catch any other unexpected errors during the /verify process
        log.exception(
        "Unexpected error in /verify endpoint"
            )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during verification"
        )

    else:
        return response


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