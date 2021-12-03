from fastapi import status, HTTPException

from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash(password: str):
    return pwd_ctx.hash(password)

def raise_404_or_not(rsrc, id=None, msg="No post with ID {}"):
    if not rsrc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=msg.format(id)
        )