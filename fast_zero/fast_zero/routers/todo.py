from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from fast_zero.schemas import (
    TodoSchema, TodoPublic, TodoList, TodoUpdate, Message
)
from fast_zero.database import get_session
from fast_zero.models import User, Todo
from fast_zero.security import get_current_user
from fast_zero.models import TodoState


router = APIRouter(prefix='/todos', tags=['todos'])

T_Session = Annotated[Session, Depends(get_session)]
T_USER = Annotated[User, Depends(get_current_user)]


@router.post('/')
async def create_todo(
        todo: TodoSchema,
        session: T_Session,
        user: T_USER) -> TodoPublic:

    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.get('/')
async def list_todos(
    session: T_Session,
    user: T_USER,
    title: str | None = None,
    description: str | None = None,
    state: TodoState | None = None,
    offset: int = 0,
    limit: int = 10
) -> TodoList:
    query = select(Todo).where(Todo.user_id == user.id)

    if title:
        query = query.filter(Todo.title.contains(title))

    if description:
        query = query.filter(Todo.description.contains(description))

    if state:
        query = query.filter(Todo.state == state)

    todos = session.scalars(query.offset(offset).limit(limit)).all()

    return {'todos': todos}


@router.patch('/{todo_id}', response_model=TodoPublic)
async def patch_todo(
    todo_id: int, session: T_Session, user: T_USER, todo: TodoUpdate
):

    db_todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Task not found'
        )

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.delete('/{todo_id}')
async def delete_todo(
        todo_id: int, session: T_Session, user: T_USER) -> Message:

    todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Task not found'
        )

    session.delete(todo)
    session.commit()

    return {'message': 'Task has been deleted successfuly'}
