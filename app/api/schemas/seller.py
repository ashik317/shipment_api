from pydantic import BaseModel, EmailStr

class SellerBase(BaseModel):
    name: str
    email: EmailStr

class SellerRead(SellerBase):
    id: int
    model_config = {"from_attributes": True}

class SellerCreate(SellerBase):
    password: str

class SellerLogin(BaseModel):
    email: EmailStr
    password: str
