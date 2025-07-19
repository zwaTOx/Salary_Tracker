from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware

from src.database import engine, Sessionlocal, Base
from src.routes.auth import router as auth_router
from src.routes.employee_info import router as employee_router
from src.routes.admin_route import router as admin_router

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

app.include_router(auth_router)
app.include_router(employee_router)
app.include_router(admin_router)

@app.get("/") 
async def get_user(db: db_dependency):
    return {"Test": 'OK'}

if __name__ == '__main__':
    config = uvicorn.Config(app, port=8000, reload=True)
    server = uvicorn.Server(config)
    server.run()