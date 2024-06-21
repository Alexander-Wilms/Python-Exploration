# Cf. https://fastapi.tiangolo.com/tutorial/first-steps/
# Start server with
# fastapi dev rest_api.py

from fastapi import FastAPI
from math import sqrt
import os

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/square_path_parameter/{input}")
async def square_path_parameter(input: float):
    return {"square": input**2}


@app.get("/square_query_parameter")
async def square_query_parameter(input: float):
    return {"square": input**2}


@app.get("/square_root")
async def square_root(input: float):
    return {"sqrt": sqrt(float(input))}


@app.get("/start_dolphin")
async def start_dolphin():
    os.system("dolphin &")
