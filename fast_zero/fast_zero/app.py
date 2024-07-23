from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session


from fast_zero.models import User
from .database import get_session
from .schemas import UserSchema, UserPublic, UserList, Message, Token
from .security import get_password_hash, verify_password, create_access_token, get_current_user

app = FastAPI()


@app.get('/')
async def home():
    return {'hello': 'world'}


@app.post('/users/', status_code=status.HTTP_201_CREATED,
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


@ app.get('/users/', response_model=UserList)
async def read_users(
    limit: int = 10, offset: int = 0,
    session: Session = Depends(get_session),

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
    user_id: int, user: UserSchema,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Not enough permission'
        )

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)

    session.commit()
    session.refresh(current_user)

    return current_user


@app.delete('/users/{user_id}', response_model=Message)
async def delete(
    user_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Not enough permission'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'user deleted'}


@app.post('/token/', response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):

    user = session.scalar(
        select(User).where(User.username == form_data.username)
    )

    if not user or not verify_password(
        form_data.password, user.password
    ):

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect username or password')

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}
