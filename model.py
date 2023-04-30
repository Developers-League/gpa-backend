from pydantic import BaseModel

# FGPA form data
class fgpa(BaseModel):
    pass

# CGPA form data
class cgpa(BaseModel):
    pass

# Minimum and Maximum CGPA form data
class min_max_cgpa(BaseModel):
    pass

# Required grades to hit a desired CGPA form data
class required_cgpa(BaseModel):
    pass
