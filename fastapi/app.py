from fastapi import FastAPI

from fast_zero.routers import users, auth, todo


app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todo.router)


@app.get('/')
async def home():
    return {'hello': 'world'}
