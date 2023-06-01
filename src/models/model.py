"""Model file for the API."""
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
class MinMaxCgpa(BaseModel):
    old_cgpa: float
    old_chours: float
    new_chours: float


# Required grades to hit a desired CGPA form data
class RequiredGrades(BaseModel):
    old_cgpa: float
    old_chours: float
    new_cgpa: float
    new_chours: float
    course_num: float
