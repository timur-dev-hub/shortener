from fastapi import APIRouter

from app.schemas.user import UserRegister, LoginRegister

router = APIRouter()

@router.post("/registration")
async def registration(register_data: UserRegister):
    pass

@router.post("/login")
async def login(login_data: LoginRegister):
    pass
