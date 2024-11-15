from typing import List, Set, Callable

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status


from app.core.security import oauth2_scheme, decode_token
from app.dependencies import get_db
from app.db.models.user_model import User


async def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
) -> User:
    payload = decode_token(token)
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid authentication credentials.")
    
    # Fetch user from the database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        # Optionally, create a new user in the database
        user = User(
            id=user_id,
            username=payload.get("username"),
            email=payload.get("email"),
            legal_name = payload.get("legal_name"),
            preferred_name = payload.get("preferred_name")
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    # Extract roles from token
    token_roles = payload.get('realm_access', {}).get('roles', [])
    user.token_roles = token_roles
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            details="Inactive user")
    return current_user