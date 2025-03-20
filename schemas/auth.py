# schema.py

from pydantic import BaseModel, EmailStr, UUID4


class CasbinRuleCreate(BaseModel):
    ptype: str
    v0: str
    v1: str
    v2: str
    v3: str = None
    v4: str = None
    v5: str = None

    class Config:
        orm_mode = True


class UserRegistration(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    password: str


class UserRegistrationResponse(BaseModel):
    id: UUID4
    email: EmailStr


class ProfileCreation(BaseModel):
    user_id: UUID4
    gender: str
    ethnicity: str
    country: str
    language: str


class ProfileCreationResponse(BaseModel):
    user_id: UUID4
    gender: str
    ethnicity: str
    country: str
    language: str


class AddressCreation(BaseModel):
    user_id: UUID4
    street: str
    city: str
    country: str
    zip_code: int


class LoginRequest(BaseModel):
    username: str
    password: str