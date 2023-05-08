from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from dotenv import dotenv_values

import mail_sender
import verification


CFG = dotenv_values(".env")


app = FastAPI()

app.include_router(mail_sender.router)
app.include_router(verification.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")



@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(CFG["DB_URL"])
    app.database = app.mongodb_client[CFG["DB_NAME"]]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


@app.get("/")
async def FunctionName(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})