"""FGPA calculation endpoint."""
from fastapi import APIRouter, HTTPException, status

from src.models.model import Cgpa, Fgpa, MinMaxCgpa, RequiredGrades
from src.services.gpa import (
    calculate_fgpa,
    calculate_min_max_cgpa,
    calculate_new_gpa,
    calculate_req_grades,
)

router = APIRouter()


@router.post("/api/calculate-fgpa")
async def fgpa(data: Fgpa):
    try:
        result = calculate_fgpa(data)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        return {"result": str(e)}


# Minimum and Maximum GPA calculation endpoint
@router.post("/api/calc-min-max-gpa-per-sem")
async def min_max_cgpa(data: MinMaxCgpa):
    try:
        result = calculate_min_max_cgpa(data)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        return {"result": str(e)}


# GPA and CGPA calculation endpoint
@router.post("/api/calc-gpa-and-cgpa")
async def calc_new_gpa(data: Cgpa):
    try:
        result = calculate_new_gpa(data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# Required grades calculation endpoint
@router.post("/api/calc-req-grades")
async def required_grades(data: RequiredGrades):
    try:
        result = calculate_req_grades(data)
        return result
    except Exception as e:
        return {"error": str(e)}


# Convert CGPA to CWA and vice versa
@router.get("/api/convert_weight")
def convert_weight(cgpa: float = None, cwa: float = None):
    """Converts between CGPA (Cumulative Grade Point Average) and CWA (Cumulative Weighted Average).

    Args:
        cgpa: CGPA to convert. Type: float.
        cwa: CWA to convert. Type: float.

    Returns:
        Converted value. Type: float.
    """
    if cgpa is not None and cwa is not None:
        raise HTTPException(
            status_code=400, detail="Only one conversion value should be provided."
        )
    elif cgpa is not None:
        if cgpa > 4.0 or cgpa < 0:
            raise HTTPException(
                status_code=400,
                detail="Invalid CGPA value. CGPA cannot be greater than 4.0 or less than 0.0.",
            )
        cwa = cgpa * 25
        return {"feedback": f"Your converted CGPA is {cwa}"}
    elif cwa is not None:
        if cwa > 100 or cwa < 0:
            raise HTTPException(
                status_code=400,
                detail="Invalid CWA value. CWA cannot be greater than 100 or less than 0.",
            )
        cgpa = cwa / 25
        return {"feedback": f"Your converted CWA is {cgpa}"}
    else:
        raise HTTPException(status_code=400, detail="No conversion value provided.")
