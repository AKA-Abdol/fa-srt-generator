from fastapi import FastAPI
from subtitle.router import router

app = FastAPI()

app.include_router(router)