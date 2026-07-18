from fastapi import Header, HTTPException, status

from config import ADMIN_API_KEY



def require_admin(x_api_key: str = Header(default="")):
    """Simple shared-secret auth for admin-only endpoints (upload, delete, view messages).

    The admin panel and any admin scripts must send this key in the
    `X-API-Key` header. Good enough for a single-owner portfolio site;
    swap for real auth (OAuth, sessions) if this grows multiple users.
    """
    if not x_api_key or x_api_key != ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    return True