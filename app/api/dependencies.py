from typing import Annotated
from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.database.models import Seller

from app.services.shipment import ShipmentService
from app.services.seller import SellerService
from app.database.session import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Asynchronous database session dependency
SessionDep = Annotated[AsyncSession, Depends(get_session)]

# Access token dependency
async def get_access_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    data = await decode_access_token(token)

    if data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid access token"
        )
    return data

# Login In Seller dependency
async def get_current_seller(
        token_data: Annotated[dict, Depends(get_access_token)],
        session: SessionDep,
):
    return await session.get(Seller, token_data["user"]["id"])

# Shipment Service dependency
async def get_shipment_service(
        session: SessionDep,
):
    return await ShipmentService(session)

# Seller Service dependency
async def get_seller_service(
        session: SessionDep,
):
    return await SellerService(session)

# Shipment Service dependency Annotated
ShipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]

# Seller Service dependency Annotated
SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]

