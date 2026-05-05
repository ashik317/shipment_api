from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.api.dependencies import SellerServiceDep
from app.api.schemas.seller import SellerCreate, SellerRead  # ✅ SellerRead import করো

router = APIRouter(
    prefix="/sellers",
    tags=["Sellers"],
)

@router.post("/signup", response_model=SellerRead, status_code=201)
async def register_seller(
    seller: SellerCreate,
    service: SellerServiceDep
):
    return await service.add(seller) 

@router.post("/login")
async def login_seller(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: SellerServiceDep,
):
    token = await service.token(request_form.username, request_form.password)
    return {"access_token": token, "token_type": "bearer"}