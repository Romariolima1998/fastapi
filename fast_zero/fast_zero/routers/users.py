from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session


from fast_zero.models import User
from fast_zero.database import get_session
from fast_zero.schemas import UserSchema, UserPublic, UserList, Message
from fast_zero.security import (
    get_password_hash,
    get_current_user
)

router = APIRouter(
    prefix='/users',
    tags=['users']
)
SessionAnnotated = Annotated[Session, Depends(get_session)]


@router.post('/', status_code=status.HTTP_201_CREATED,
             response_model=UserPublic)
async def create_user(
    user: UserSchema, session: Session = Depends(get_session)
):

    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            # o username ja existe
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='usename already exists'
            )

        elif db_user.email == user.email:
            # email ja existe
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='email already exists'
            )

    db_user = User(username=user.username, email=user.email,
                   password=get_password_hash(user.password))
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/', response_model=UserList)
async def read_users(
    limit: int = 10, offset: int = 0,
    session: Session = Depends(get_session),

):

    users = session.scalars(
        select(User).limit(limit).offset(offset)
    )
    return {'users': users}


@ router.get('/detail/{user_id}', response_model=UserPublic)
async def user_detail(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(User.id == user_id)
    )
    if not db_user:
        raise HTTPException(
            status_code=404, detail='User not foud'
        )

    return db_user


@router.put('/{user_id}', response_model=UserPublic)
async def update_user(
    user_id: int, user: UserSchema,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough permission'
        )

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)

    session.commit()
    session.refresh(current_user)

    return current_user

# usando SessionAnnotated ao inves de Session = Depends(get_session)
#  que e a msm coisa


@router.delete('/{user_id}', response_model=Message)
async def delete(
    user_id: int,
    session: SessionAnnotated,
    current_user=Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough permission'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'user deleted'}
