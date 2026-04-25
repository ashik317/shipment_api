from typing import Annotated
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.services.shipment import ShipmentService
from app.database.session import get_session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

def get_shipment_service(session: Annotated[AsyncSession, Depends(get_session)]) -> ShipmentService:
    return ShipmentService(session)

ServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]