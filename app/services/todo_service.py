from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.todo_repository import TodoRepository
from app.schemas.todo_schema import TodoCreate, TodoUpdate


class TodoService:
    def __init__(self, db: Session):
        self.repository = TodoRepository(db)

    def get_my_todos(self, user_id: int):
        return self.repository.get_all_by_owner(user_id)

    def get_my_todo_by_id(self, todo_id: int, user_id: int):
        todo = self.repository.get_by_id_and_owner(todo_id, user_id)

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )

        return todo

    def create_todo(self, todo_data: TodoCreate, user_id: int):
        return self.repository.create(todo_data, user_id)

    def update_todo(self, todo_id: int, todo_data: TodoUpdate, user_id: int):
        todo = self.get_my_todo_by_id(todo_id, user_id)
        return self.repository.update(todo, todo_data)

    def delete_todo(self, todo_id: int, user_id: int):
        todo = self.get_my_todo_by_id(todo_id, user_id)
        self.repository.delete(todo)
        return {"message": "Todo deleted successfully"}