from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model import *
from base import *

app = FastAPI()

# To combine the frontend and backend since both are on different domains
origins = ['http://localhost:3000', 'http://192.168.43.48:3000'] # frontend URL

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# FGPA calculation endpoint
@app.post('/api/calculate-fgpa')
async def fgpa(data: Fgpa):
    try:
        result = calculate_fgpa(data)
        return result
    except Exception as e:
        return {"result": str(e)}


# Minimum and Maximum GPA calculation endpoint
@app.post('/api/calc-min-max-gpa-per-sem')
async def min_max_cgpa(data: Min_max_cgpa ):
    try:
        result = calculate_min_max_cgpa(data)
        return result
    except Exception as e:
        return {"result": str(e)}


# GPA and CGPA calculation endpoint
@app.post('/api/calc-gpa-and-cgpa')
async def calc_new_gpa(data: Cgpa ):
    try:
        result = calculate_new_gpa(data)
        return result
    except Exception as e:
        return{"result" : str(e)}


# Required grades calculation endpoint
@app.post('/api/calc-req-grades')
async def required_grades(data: Required_grades):
    try:
        result = calculate_req_grades(data)
        return result
    except Exception as e:
        return{"error": str(e)}