from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.api.dependencies import SellerServiceDep
from app.api.schemas.schemas import SellerCreate, SellerLogin

router = APIRouter(
    prefix="/sellers",
    tags=["Sellers"],
)

# Register a new seller
@router.post("/register")
async def register_seller(
    seller: SellerCreate, 
    service: Annotated[SellerServiceDep, Depends()]
):
    await service.add(seller)
    return {"message": "Seller registered successfully"}

# Login a seller
@router.post("/login")
async def login_seller(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
   service: Annotated[SellerServiceDep, Depends()],
):
    token = await service.token(request_form.username, request_form.password)
    return {
        "access_token": token, 
        "type": "jwt"
    }