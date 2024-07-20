from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session


from fast_zero.models import User
from .database import get_session
from .schemas import UserSchema, UserPublic, UserList, Message

app = FastAPI()


@app.get('/')
async def home():
    return {'hello': 'world'}


@app.post('/users/', status_code=status.HTTP_201_CREATED,
          response_model=UserPublic)
async def create_user(user: UserSchema, session: Session = Depends(get_session)):

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
                   password=user.password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@ app.get('/users/', response_model=UserList)
async def read_users(
    limit: int = 10, offset: int = 0, session: Session = Depends(get_session)
):

    users = session.scalars(
        select(User).limit(limit).offset(offset)
    )
    return {'users': users}


@ app.get('/users/detail/{user_id}', response_model=UserPublic)
async def user_detail(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(User.id == user_id)
    )
    if not db_user:
        raise HTTPException(
            status_code=404, detail='User not foud'
        )

    return db_user


@app.put('/users/{user_id}', response_model=UserPublic)
async def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):

    db_user = session.scalar(
        select(User).where(User.id == user_id)
    )

    if not db_user:
        raise HTTPException(
            status_code=404, detail='User not foud'
        )

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password

    session.commit()
    session.refresh(db_user)

    return db_user


@app.delete('/users/{user_id}', response_model=Message)
async def delete(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(User.id == user_id)
    )

    if not db_user:
        raise HTTPException(status_code=404, detail='User not foud')

    session.delete(db_user)
    session.commit()

    return {'message': 'user deleted'}
