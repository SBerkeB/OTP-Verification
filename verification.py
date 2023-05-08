from fastapi import APIRouter, Form, Request, Depends, status
from fastapi.responses import RedirectResponse
from dotenv import dotenv_values
from fastapi.templating import Jinja2Templates
from dataclasses import dataclass
from mail_sender import jwtDecoder

import pyotp
import time

CFG = dotenv_values(".env")

templates = Jinja2Templates(directory="templates")

@dataclass
class Code():
    otp_code: str = Form(...)

router = APIRouter()

@router.get("/verification")
async def FunctionName(request: Request):
    return templates.TemplateResponse("verification.html", {"request": request})

@router.post("/verification_post")
async def FunctionName(code: Code = Depends()):
    timeot_interval = CFG["TIMEOUT_INTERVAL"]
    totp = pyotp.TOTP(CFG["OTP_SECRET"], interval=int(timeot_interval))
    if totp.verify(code.otp_code):
        return RedirectResponse(url="http://127.0.0.1:8000/", status_code=status.HTTP_302_FOUND)
    else:
        return {"message": "Timeout!!"}
    



@router.get("/jwt/{encoded}")
async def FunctionName(request: Request, encoded: str):
    decoded = jwtDecoder(encoded)
    if time.time() - decoded["timestamp"] < 300:
        user_info = {"username": decoded["username"], "mail_address": decoded["mail_address"], "hash_password": decoded["hash_password"]}
        user_info = user_info
        request.app.database["users"].insert_one(user_info)
        return RedirectResponse(url="http://127.0.0.1:8000/", status_code=status.HTTP_302_FOUND)
    else:
        return {"message": "Timeout!"}