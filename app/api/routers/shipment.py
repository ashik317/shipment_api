# app/api/routers/shipment.py
from fastapi import APIRouter, HTTPException, status
from app.api.dependencies import ShipmentServiceDep
from app.api.schemas.schemas import ShipmentCreate, ShipmentRead

router = APIRouter(
    prefix="/shipments",
    tags=["Shipments"],
)

# Read a shipment by Id
@router.get("/{id}", response_model=ShipmentRead)
async def get_shipments(id: int, service: ShipmentServiceDep):
    shipment = await service.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    return shipment

# Create a new shipment
@router.post("/", response_model=ShipmentRead)
async def create_shipment(shipment: ShipmentCreate, service: ShipmentServiceDep):
    return await service.add(shipment)

# Update fields of a shipment
@router.put("/{id}", response_model=ShipmentRead)
async def update_shipment(id: int, shipment_update: ShipmentCreate, service: ShipmentServiceDep):
    update = shipment_update.model_dump(exclude_unset=True)
    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )
    return await service.update(id, update)

# Delete a shipment by Id
@router.delete("/{id}")
async def delete_shipment(id: int, service: ShipmentServiceDep) -> dict[str, str]:
    await service.delete(id)
    return {"message": "Shipment deleted successfully"}