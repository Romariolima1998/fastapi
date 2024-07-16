from fastapi import FastAPI, status, HTTPException
from .schemas import UserSchema, UserPublic, UserDB, UserList, Message

app = FastAPI()

database = []


@app.get('/')
async def home():
    return {'hello': 'world'}


@app.post('/users/', status_code=status.HTTP_201_CREATED,
          response_model=UserPublic)
async def create_user(user: UserSchema):
    user_with_id = UserDB(id=len(database)+1,
                          **user.dict())
    database.append(user_with_id)
    return user_with_id


@app.get('/users/', response_model=UserList)
async def read_users():
    return {'users': database}


@app.get('/users/detail/{user_id}', response_model=UserPublic)
async def user_detail(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=404, detail='User not foud'
        )

    user = database[user_id - 1]
    return user


@app.put('/users/{user_id}', response_model=UserPublic)
async def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=404, detail='User not foud'
        )

    user_with_id = UserDB(id=user_id, **user.dict())
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
async def delete(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=404, detail='User not foud')

    del database[user_id - 1]

    return {'message': 'user deleted'}
