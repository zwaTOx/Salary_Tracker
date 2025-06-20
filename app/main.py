from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Sessionlocal, Base

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
async def get_user(db: db_dependency):
    return {"Test": 'OK'}

if __name__ == '__main__':
    config = uvicorn.Config(app, port=8000, reload=True)
    server = uvicorn.Server(config)
    server.run()