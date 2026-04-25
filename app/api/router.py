from fastapi import APIRouter, HTTPException, status
from app.api.dependencies import ServiceDep
from app.api.schemas.schemas import ShipmentCreate, ShipmentUpdate
from app.database.models import Shipment

router = APIRouter(
    prefix="/shipments", 
    tags=["Shipments"],
)

@router.get("/{id}", response_model=Shipment)
async def get_shipments(id: int, service: ServiceDep) -> Shipment:
    shipment = await service.get(id)
    if shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")
    return shipment

@router.post("")
async def create_shipment(shipment: ShipmentCreate, service: ServiceDep) -> Shipment:
    await service.add(shipment)
    return {"message": "Shipment created successfully"}

@router.patch("/{id}", response_model=Shipment)
async def update_shipment(id: int, shipment_update: ShipmentUpdate, service: ServiceDep):
    update = shipment_update.model_dump(exclude_unset=True)
    if not update:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update")
    shipment = await service.update(id, shipment_update)
    return shipment

@router.delete("/{id}")
async def delete_shipment(id: int, service: ServiceDep) -> dict[str, str]:
    await service.delete_shipment(id)
    return {"message": f"Shipment with id {id} has been deleted"}