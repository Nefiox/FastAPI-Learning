from fastapi import FastAPI

app = FastAPI()

# Path operation decorator
@app.get('/')
def home():
    return {'Hello': 'World'}