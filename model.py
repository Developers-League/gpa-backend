from pydantic import BaseModel

# FGPA form data
class Fgpa(BaseModel):
    cgpa1: float
    cgpa2: float
    cgpa3: float
    cgpa4: float

# CGPA form data
class Cgpa(BaseModel):
    grades: list
    credit: list 

# Minimum and Maximum CGPA form data
class Min_max_cgpa(BaseModel):
    oldCgpa: float
    oldChours: float
    newChours: float

# Required grades to hit a desired CGPA form data
class Required_grades(BaseModel):
    oldCgpa : float
    oldChours: float
    newCgpa : float
    newChours: float
    courseNum: float
