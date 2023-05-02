from pydantic import BaseModel

# FGPA form data
class fgpa(BaseModel):
    cgpa1: float
    cgpa2: float
    cgpa3: float
    cgpa4: float

# CGPA form data
class cgpa(BaseModel):
    grades: str
    credit: list 

# Minimum and Maximum CGPA form data
class min_max_cgpa(BaseModel):
    old_chours: int
    new_chours: int
    old_cgpa: float

# Required grades to hit a desired CGPA form data
class required_cgpa(BaseModel):
    old_cgpa : float
    new_cgpa : float
    old_chours: int
    new_chours: int
