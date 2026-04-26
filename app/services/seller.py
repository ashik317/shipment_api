from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from app.database.models import Seller
from app.api.schemas.schemas import SellerCreate



password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SellerService:
    def __init__(self, Session: AsyncSession):
        self.Session = Session
    
    async def add(self, creadentials: SellerCreate)-> Seller:
        seller = Seller(
            **creadentials.model_dump(exclude={"password"}),
            password=password_context.hash(creadentials.password)
        )
        self.Session.add(seller)
        await self.Session.commit()
        await self.Session.refresh(seller)
        return seller
