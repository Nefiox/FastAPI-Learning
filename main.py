# Server: uvicorn main:app --reload
# Python
from typing import Optional
from enum import Enum
from fastapi.datastructures import DefaultType # Para validar enumeraciones de strings

# Pydantic (FastAPI funciona sobre Pydantic, es por eso que se pone abajo)
from pydantic import BaseModel
from pydantic import Field # Para validar modelos

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Query, Path, Form
from starlette.status import HTTP_200_OK

app = FastAPI()

# Models
class HairColor(Enum):
    white = 'white'
    brown = 'brown'
    black = 'black'
    blonde = 'blonde'
    red = 'red'

class Location(BaseModel):
    city: str = Field(
        min_length=1,
        max_length=50,
        example='Coatzacoalcos'
    )
    state: str = Field(
        min_length=1,
        max_length=50,
        example='Veracruz'
    )
    country: str = Field(
        min_length='1',
        max_length='50',
        example='México'
    )

class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='John'
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='McLane'
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example='25'
        )
    hair_color: Optional[HairColor] = Field(default=None, example='black')
    is_married: Optional[bool] = Field(default=None, example='False')

class Person(PersonBase):
    password: str = Field(
        ...,
        min_length=8
        )
    # class Config:
    #     schema_extra = {
    #         'example': {
    #             'first_name': 'Mike',
    #             'last_name': 'Shultz',
    #             'age': 21,
    #             'hair_color': 'black',
    #             'is_married': False,
    #         }
    #     }

class PersonOut(PersonBase):
    pass

class LoginOut(BaseModel):
    username: str = Field(
        ...,
        max_length=20,
        example='john2021'
    )
    message: str = Field(default='Login Successfully!')

# Path operation decorator
@app.get(
    path='/',
    status_code=status.HTTP_200_OK
    )
def home():
    return {'Hello': 'World'}

# Request and Response body
@app.post(
    path='/person/new',
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED
    )
def create_person(person: Person = Body(...)):
    return person

# Validaciones: Query Parameters
@app.get(
    path='/person/detail',
    status_code=status.HTTP_200_OK
    )
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title='Person name',
        description='This is the person name. It is between 1 and 50 characters',
        example='Dulce'
        ),
    age: str = Query(
        ...,
        title='Person age',
        description='This is the person age. It is required',
        example=22
        )
):
    return {name: age}

# Validaciones: Path Parameters
@app.get(
    path='/person/detail/{person_id}',
    status_code=status.HTTP_200_OK
    )
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title='Person ID',
        description='This is the person ID. It is required',
        example=30
        )
):
    return {person_id: 'It exists!'}

# Validaciones: Request Body
@app.put(
    path='/person/{person_id}',
    status_code=status.HTTP_200_OK
    )
def update_person(
    person_id: int = Path(
        ...,
        title='Person ID',
        description='This is the person ID. It is required',
        gt=0,
        example=32
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results

@app.post(
    path='/login',
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(
    username: str = Form(...),
    password: str = Form(...)
    ):
    return LoginOut(username=username)