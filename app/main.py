from fastapi import FastAPI

from app.database import Base, engine
from app.models.todo_model import Todo
from app.models.user_model import User
from app.database import SessionLocal
from app.seed import seed_admin
from app.controllers.todo_controller import router as todo_router
from app.controllers.auth_controller import router as auth_router
from app.controllers.admin_controller import router as admin_router
from fastapi.middleware.cors import CORSMiddleware
Base.metadata.create_all(bind=engine)
db = SessionLocal()
try:
    seed_admin(db)
finally:
    db.close()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(todo_router)