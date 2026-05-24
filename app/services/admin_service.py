from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.events.todo_events import todo_deleted_by_admin_event
from app.repositories.todo_repository import TodoRepository


class AdminService:
    def __init__(self, db: Session):
        self.todo_repository = TodoRepository(db)

    def get_all_todos(self):
        todos = self.todo_repository.get_all()

        return [    
            {
                "id": todo.id,
                "title": todo.title,
                "description": todo.description,
                "completed": todo.completed,
                "owner_id": todo.owner_id,
                "owner_email": todo.owner.email
            }
            for todo in todos
        ]

    def delete_any_todo(self, todo_id: int, admin_id: int):
        todo = self.todo_repository.get_by_id(todo_id)

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )

        self.todo_repository.delete(todo)

        todo_deleted_by_admin_event(todo_id, admin_id)

        return {"message": "Todo deleted by admin"}