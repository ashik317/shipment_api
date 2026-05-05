from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from app.database.models import Seller
from app.api.schemas.seller import SellerCreate
import hashlib
import base64

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _prehash(password: str) -> str:
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return base64.b64encode(digest).decode("utf-8")

class SellerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, credentials: SellerCreate) -> Seller:
        seller = Seller(
            **credentials.model_dump(exclude={"password"}),
            password=password_context.hash(_prehash(credentials.password)),
        )
        self.session.add(seller)

        try:                    
            await self.session.commit()
            await self.session.refresh(seller)
            return seller
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=409,
                detail=f"Email '{credentials.email}' is already registered."
            )

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return password_context.verify(_prehash(plain_password), hashed_password)