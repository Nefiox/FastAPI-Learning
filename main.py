# Python
from typing import Optional
from fastapi.param_functions import Query

# Pydantic (FastAPI funciona sobre Pydantic, es por eso que se pone abajo)
from pydantic import BaseModel

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models
class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

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
    Location: Location = Body(...)
):
    results = person.dict()
    results.update(Location.dict())
    return results