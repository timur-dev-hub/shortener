from fastapi import APIRouter, Response, Depends

from app.core.security import security
from app.schemas.user import UserRegister, LoginRegister

router = APIRouter()

@router.post("/registration")
async def registration(register_data: UserRegister, response: Response):
    if register_data.email == "user@example.com":

        token = security.create_access_token(uid="10881088")
        security.set_access_cookies(token, response)

        return {"massage": "reg TRUE"}
    return {"massage": "reg FALSE"}

@router.get("/login")
async def login(token_payload = Depends(security.access_token_required)):

    return {"massage": "login TRUE"}
