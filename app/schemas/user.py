from pydantic import BaseModel, EmailStr

# -------- SIGNUP --------
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# -------- LOGIN --------
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# -------- RESPONSE --------
class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
