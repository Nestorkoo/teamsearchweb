# filepath: d:\Python_Projects\FastAPI Projects\test\backend\deps.py
from fastapi import Depends, HTTPException
from authx import AuthX
from config import security
import logging

async def get_current_user_id(
        token: str = Depends(security.access_token_required),
) -> int:
    """Get the user ID from the token."""
    try:
        logging.info(f"Token: {token}")
        user_id = token.sub 
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials deps")
        return int(user_id)
    except Exception as e:
        logging.error(f"Error: {e}")
        raise HTTPException(status_code=401, detail="Invalid authentication credentials deps") from e