from base import *
from model import *


def calc_fgpa(details: Fgpa):
    cgpa1 = details.cgpa1
    cgpa2 = details.cgpa2
    cgpa3 = details.cgpa3
    cgpa4 = details.cgpa4

    try:
        temp1 = cgpa1 * 1/6 	# Weight 1
        temp2 = cgpa2 * 1/6 	# Weight 2
        temp3 = cgpa3 * 2/6 	# Weight 3
        temp4 = cgpa4 * 2/6 	# Weight 4

        final_gpa = temp1 + temp2 + temp3 + temp4
        final_gpa = round(final_gpa, 2)

        levels = grade_to_classification(final_gpa)

        result = {
            "cgpa1": cgpa1,
            "cgpa2": cgpa2,
            "cgpa3": cgpa3,
            "cgpa4": cgpa4,
            "fgpa": final_gpa,
            "classification": levels
        }
        return result
    except Exception as e:
        return {"error": str(e)}
        
async def calc_new_gpa(grades, credit):
    pass

async def calc_gpa_needed(old_cgpa, new_cgpa, old_chours, new_chours):
    pass

async def calc_min_max_cgpa(old_chours, new_chours, old_cgpa):
    pass