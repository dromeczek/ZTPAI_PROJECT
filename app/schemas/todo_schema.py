from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str | None = None


class TodoUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = None
    completed: bool | None = None


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool

    class Config:
        from_attributes = True

class AdminTodoResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    owner_id: int
    owner_email: str

    class Config:
        from_attributes = True