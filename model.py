from pydantic import BaseModel

# FGPA form data
class Fgpa(BaseModel):
    cgpa1: float
    cgpa2: float
    cgpa3: float
    cgpa4: float

# CGPA form data
class Cgpa(BaseModel):
    grades: str
    credit: list 

# Minimum and Maximum CGPA form data
class Min_max_cgpa(BaseModel):
    oldCgpa: float
    oldChours: float
    newChours: float

# Required grades to hit a desired CGPA form data
class Required_cgpa(BaseModel):
    old_cgpa : float
    new_cgpa : float
    old_chours: int
    new_chours: int
