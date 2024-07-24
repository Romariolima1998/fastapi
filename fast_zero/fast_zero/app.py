from fastapi import FastAPI

from fast_zero.routers import users, auth


app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)


@app.get('/')
async def home():
    return {'hello': 'world'}
