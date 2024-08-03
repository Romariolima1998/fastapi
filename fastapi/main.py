from typing import Dict, List, Union, Annotated, Any
from http import HTTPStatus

from enum import Enum

from fastapi import (FastAPI, Query, Path, Body,
                     Cookie, Header, Form, status,
                     File, UploadFile, HTTPException)

from serializer import Item, User


class ModelName(str, Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'


app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {
    "item_name": "Bar"}, {"item_name": "Baz"}]


# ########### urls ######################

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


@app.get('/models/{model_name}')
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {'model_name': model_name}

    elif model_name is ModelName.resnet:
        return {'model_name': model_name}

    return {'model_name': model_name}


# ############## serializando dados ######################

# o query e para configuracao de query da url, parametros apos o ?
# o path e para configuaracoes do parametro da uri como id passado como parametros
# o Body serve para um parametro sem serializer funcionar como corpo do post
# o embed do body serve para requisitar o nome da class serializer como chave do corpo
@app.post("/items/{item_id}")
async def create_item(
    *,
    item: Item = Body(
        example=[
            {
                "item": {
                    "name": "string",
                    "description": "string",
                    "price": 1,
                    "tax": 0,
                    "tags": [],
                    "image": {
                        "url": "https://example.com/",
                        "name": "string"
                    }
                },
                "user": {
                    "username": "string"
                },
                "importance": 0
            }
        ]
    ),
    user: User,
    importance: int = Body(embed=True),
    item_id: int = Path(title="the ID of the item", ge=1),
    q: str | None = Query(default=None, max_length=50, pattern='^[a-zA-Z].$')
):

    result = {'item': {**item.model_dump()}, 'user': {**user.model_dump()}}
    if q:
        result.update({'q': q})
    return result


@app.post('cookie', response_model=Dict[str, Union[List[str], str]], status_code=status.HTTP_201_CREATED)
async def cookie(
    ads_id: str | None = Cookie(default=None),
    x_token: list[str] | None = Header(default=None)
) -> Any:
    return {'ads_id': ads_id, 'x-token values': x_token}


# ######### form ##################################################

@app.post('/login/')
async def login(username: str = Form(), password: str = Form()) -> Dict[str, str]:
    return {'username': username}


########################## upload files #####################################

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


# ###################### HTTPException ##########################################

items = {'foo': "the foo wrestlers"}


@app.get('/items/{item_id}')
async def httpexeption(item_id: str) -> Dict[str, str]:
    if item_id not in items:
        raise HTTPException(status_code=404, detail='item not found')

    return {'item': items[item_id]}
