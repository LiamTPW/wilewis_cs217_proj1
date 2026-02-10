from typing import Annotated
from fastapi import FastAPI, Query
from pydantic import BaseModel
from datetime import datetime
import todo


user_list = todo.TodoList()

class Item(BaseModel):
    note: str
    priority: int
    due: str
    done: bool

app = FastAPI()

@app.get("/")
def home():
    return {"name": "To-do Application", "description": "A to-do list with due dates and priorities"}

@app.get("/help")
def help():
    return {"message": f"Hello bob"}

@app.get("/items")
def items():
    return user_list.pp()

@app.get("/search?term={string}")
def search(term: str):
    return user_list.search(term)

@app.get("/item/{identifier}")
def item(identifier: int):
    return user_list[identifier]

@app.post("/add")
def add(new_item: Annotated[Item, Query()]):
    user_list.add(new_item.note, new_item.priority, new_item.due, new_item.done)
    return user_list

@app.get("/update/{identifier}")
def update(identifier: int, to_update: Annotated[Item, Query()]):
    user_list[identifier].update(to_update.note, to_update.priority, to_update.due, to_update.done)
    return user_list[identifier]