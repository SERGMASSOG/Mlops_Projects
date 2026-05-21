from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path
import models
from models import Todo
from pydantic import BaseModel, Field
from starlette import status
from database import engine, sessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TodoSchema(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

#Get request     
@app.get("/")
async def root(db: Annotated[Session, Depends(get_db)]):
    return db.query(Todo).all()

@app.get("/Todos/{id}", status_code=status.HTTP_200_OK)
async def get_todo(db: Annotated[Session, Depends(get_db)], id: int = Path(gt=0)):
    todo_model = db.query(Todo).filter(Todo.id == id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")

#Post request
@app.post("/create_todo", status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoSchema, db: Annotated[Session, Depends(get_db)]):
    new_todo = Todo(**todo.dict())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

#Put request
@app.put("/update_todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(todo: TodoSchema, db: Annotated[Session, Depends(get_db)],id: int = Path(gt=0)):
    todo_model = db.query(Todo).filter(Todo.id == id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    db.commit()
    return

#Delete request
@app.delete("/delete_todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: Annotated[Session, Depends(get_db)],id: int = Path(gt=0)):
    todo_model = db.query(Todo).filter(Todo.id == id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo_model)
    db.commit()
    return