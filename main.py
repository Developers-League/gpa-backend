from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from base import grade_to_classification, main_grades, getList


#  API class
app = FastAPI()

# To combine the frontend and backend since both are on different domains

origins = ['http://localhost:3000/'] # frontend URL

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Default function for the API default path

'''
Endpoints 

1. calc-fgpa
2. calc-gpa-and-cgpa
3. calc-req-grades-for-rgpa
4. calc-min-max-gpa-per-sem

'''
# FGPA calculation endpoint
@app.post('/api/calc-fgpa')
async def fgpa(cgpa1, cgpa2, cgpa3, cgpa4):
    pass

# GPA and CGPA calculation endpoint
@app.post('/api/calc-gpa-and-cgpa')
async def new_gpa_calc(grades, credit):
    pass

# Required grades calculation endpoint
@app.post('/api/calc-req-grades-for-sgpa')
async def calc_gpa_needed(old_cgpa, new_cgpa, old_chours, new_chours):
    pass

# Minimum and Maximum GPA calculation endpoint
@app.post('/api/calc-min-max-gpa-per-sem')
async def min_max_cgpa(old_chours, new_chours, old_cgpa):
    pass



