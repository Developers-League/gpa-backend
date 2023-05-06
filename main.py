from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model import Fgpa
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
async def calc_fgpa(data: Fgpa):
    cgpa1 = data.cgpa1
    cgpa2 = data.cgpa2
    cgpa3 = data.cgpa3
    cgpa4 = data.cgpa4

    try:
        temp1 = cgpa1 * 1/6 	# Weight 1
        temp2 = cgpa2 * 1/6 	# Weight 2
        temp3 = cgpa3 * 2/6 	# Weight 3
        temp4 = cgpa4 * 2/6 	# Weight 4

        final_gpa = temp1 + temp2 + temp3 + temp4
        final_gpa = round(final_gpa, 2)

        levels = grade_to_classification(final_gpa)

        return {
            "cgpa1": str(cgpa1),
            "cgpa2": str(cgpa2),
            "cgpa3": str(cgpa3),
            "cgpa4": str(cgpa4),
            "fgpa": str(final_gpa),
            "classification": levels
        }
    except Exception as e:
        return {"error": str(e)}
    
    
# # GPA and CGPA calculation endpoint
# @app.post('/api/calc-gpa-and-cgpa')


# # Required grades calculation endpoint
# @app.post('/api/calc-req-grades-for-sgpa')


# # Minimum and Maximum GPA calculation endpoint
# @app.post('/api/calc-min-max-gpa-per-sem')
