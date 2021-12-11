# Python
from typing import Optional
from enum import Enum # Para validar enumeraciones de strings

# Pydantic (FastAPI funciona sobre Pydantic, es por eso que se pone abajo)
from pydantic import BaseModel
from pydantic import Field # Para validar modelos

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models
class HairColor(Enum):
    white = 'white'
    brown = 'brown'
    black = 'black'
    blonde = 'blonde'
    red = 'red'

class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    age: int = Field(
        ...,
        gt=0,
        le=115
        )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)



# Path operation decorator
@app.get('/')
def home():
    return {'Hello': 'World'}

# Request and Response body
@app.post('/person/new')
def create_person(person: Person = Body(...)):
    return person

# Validaciones: Query Parameters
@app.get('/person/detail')
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title='Person name',
        description='This is the person name. It is between 1 and 50 characters'
        ),
    age: str = Query(
        ...,
        title='Person age',
        description='This is the person age. It is required'
        )
    
):
    return {name: age}

# Validaciones: Path Parameters
@app.get('/person/detail/{person_id}')
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID",
        description='This is the person ID. It is required'
        )
):
    return {person_id: 'It exists!'}

# Validaciones: Request Body
@app.put('/person/{person_id}')
def update_person(
    person_id: int = Path(
        ...,
        title='Person ID',
        description='This is the person ID. It is required',
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results