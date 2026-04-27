from fastapi import APIRouter, HTTPException, status  # ← add APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.api.dependencies import SellerServiceDep
from app.api.schemas.seller import SellerCreate, SellerLogin

# ← define your own local router, don't import the master one
router = APIRouter(
    prefix="/sellers",
    tags=["Sellers"],
)

@router.post("/register")
async def register_seller(seller: SellerCreate, service: SellerServiceDep):
    await service.add(seller)
    return {"message": "Seller registered successfully"}

@router.post("/login")
async def login_seller(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: SellerServiceDep,
):
    token = await service.token(request_form.username, request_form.password)
    return {"access_token": token, "type": "jwt"}