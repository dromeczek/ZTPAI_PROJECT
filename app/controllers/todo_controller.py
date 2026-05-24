from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.todo_schema import TodoCreate, TodoUpdate, TodoResponse
from app.services.todo_service import TodoService
from app.core.auth_dependencies import get_current_user
from app.models.user_model import User


router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)


@router.get("/", response_model=list[TodoResponse])
def get_todos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = TodoService(db)
    return service.get_my_todos(current_user.id)


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = TodoService(db)
    return service.get_my_todo_by_id(todo_id, current_user.id)

@router.post("/", response_model=TodoResponse, status_code=201)
def create_todo(
    todo_data: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = TodoService(db)
    return service.create_todo(todo_data, current_user.id)


@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = TodoService(db)
    return service.update_todo(todo_id, todo_data, current_user.id)


@router.delete("/{todo_id}")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = TodoService(db)
    return service.delete_todo(todo_id, current_user.id)