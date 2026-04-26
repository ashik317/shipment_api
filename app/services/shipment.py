from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.schemas import ShipmentCreate, ShipmentUpdate
from app.database.models import Shipment, ShipmentStatus

# ← removed: from app.api.dependencies import ServiceDep (not needed here)

class ShipmentService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get(self, id: int) -> Shipment:
        return await self.session.get(Shipment, id)

    async def add(self, shipment_create: ShipmentCreate) -> Shipment:
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.now() + timedelta(days=7)
        )
        self.session.add(new_shipment)
        await self.session.commit()
        await self.session.refresh(new_shipment)
        return new_shipment

    async def update(self, id: int, shipment_update: ShipmentUpdate) -> Shipment:
        shipment = await self.session.get(Shipment, id)
        shipment.sqlmodel_update(shipment_update)
        await self.session.commit()
        await self.session.refresh(shipment)
        return shipment

    async def delete_shipment(self, id: int) -> None:
        shipment = await self.session.get(Shipment, id)
        await self.session.delete(shipment)
        await self.session.commit()