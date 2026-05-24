from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.auth_dependencies import require_admin
from app.schemas.todo_schema import AdminTodoResponse
from app.services.admin_service import AdminService


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/todos", response_model=list[AdminTodoResponse])
def get_all_todos(
    db: Session = Depends(get_db),
    admin = Depends(require_admin)
):
    service = AdminService(db)
    return service.get_all_todos()


@router.delete("/todos/{todo_id}")
def delete_any_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    admin = Depends(require_admin)
):
    service = AdminService(db)
    return service.delete_any_todo(todo_id, admin.id)