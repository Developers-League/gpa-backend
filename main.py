from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from functions import *
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

# Minimum and Maximum GPA calculation endpoint
@app.post('/api/calc-min-max-gpa-per-sem')
async def calc_min_max_cgpa(data: Min_max_cgpa ):
    old_chours = data.oldChours
    new_chours = data.newChours
    old_cgpa = data.oldCgpa

    try:
        total_chours = old_chours + new_chours  # Total credit hours.
        old_points = old_chours * old_cgpa      # Weight of current gpa over current credit hours.
        
        max_cgpa = ((new_chours * 4) + old_points) / total_chours	# Weight of new gpa over sem's credit hours/ divided by total credit hours.
        max_cgpa = round(max_cgpa, 2)
        
        min_cgpa = (old_points) / total_chours	# Weight of new gpa over sem's credit hours/ divided by total credit hours.
        min_cgpa = round(min_cgpa, 2)

        levels_max_cgpa = grade_to_classification(max_cgpa)
        levels_min_cgpa = grade_to_classification(min_cgpa)

        return {
            "oldCgpa" : str(old_cgpa),
            "maxCgpa" : str(max_cgpa),
            "minCgpa" : str(min_cgpa),
            "classificationMaxCgpa" : levels_max_cgpa,
            "classificationMinCgpa" : levels_min_cgpa
        }
    except Exception as e:
        return {"erroer": str(e)}
    

# GPA and CGPA calculation endpoint
@app.post('/api/calc-gpa-and-cgpa')


# Required grades calculation endpoint
@app.post('/api/calc-req-grades')
async def calc_req_grades(data: Required_grades):
    old_cgpa = data.oldCgpa
    old_chours = data.oldChours
    new_cgpa = data.newCgpa
    new_chours = data.newChours
    course_num = data.courseNum
    try:
        total_chours = old_chours + new_chours
        new_points = total_chours * new_cgpa		# Average weight of your desired gpa over your total course hours.
        old_points = old_chours * old_cgpa			# Average weight of your current gpa over your current course hours.
        diff_points = new_points - old_points		# Difference between your desired weight and your current weight.

        min_gpa = diff_points / new_chours
        gpa = round(min_gpa, 2)

        req_grades = gpa_to_grades(min_gpa, course_num)

        res1 = f"You can't achieve a {new_cgpa} CGPA this semester. Too high"
        res2 = f"You can't achieve a {new_cgpa} CGPA this semester. Too low"
        res3 = f"For the data provided, you'll need a {gpa} GPA which requries you to fail all courses."
        res4 = f"For this info, you'll need a {gpa} GPA which requires minimum grade(s) of {req_grades}"


        if gpa > 4.00: return {"feedback" : res1}
        if gpa < 0.00: return {"feedback" : res2}
        if len(req_grades) == 0: return {"feedback" : res3}
        return {"feedback" : res4}
    
    except Exception as e:
        return{"error": str(e)}