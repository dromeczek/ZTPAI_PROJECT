from sqlalchemy.orm import Session
from app.models.todo_model import Todo
from app.schemas.todo_schema import TodoCreate, TodoUpdate


class TodoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_by_owner(self, owner_id: int):
        return self.db.query(Todo).filter(Todo.owner_id == owner_id).all()

    def get_by_id_and_owner(self, todo_id: int, owner_id: int):
        return (
            self.db.query(Todo)
            .filter(Todo.id == todo_id, Todo.owner_id == owner_id)
            .first()
        )

    def create(self, todo_data: TodoCreate, owner_id: int):
        todo = Todo(
            title=todo_data.title,
            description=todo_data.description,
            owner_id=owner_id
        )

        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)

        return todo

    def update(self, todo: Todo, todo_data: TodoUpdate):
        if todo_data.title is not None:
            todo.title = todo_data.title

        if todo_data.description is not None:
            todo.description = todo_data.description

        if todo_data.completed is not None:
            todo.completed = todo_data.completed

        self.db.commit()
        self.db.refresh(todo)

        return todo

    def delete(self, todo: Todo):
        self.db.delete(todo)
        self.db.commit()
    def get_all(self):
        return self.db.query(Todo).all()
    def get_by_id(self, todo_id: int):
        return self.db.query(Todo).filter(Todo.id == todo_id).first()