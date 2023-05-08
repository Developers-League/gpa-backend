from base import *
from model import *


def calc_fgpa(data: Fgpa):
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
        
async def calc_new_gpa(grades, credit):
    pass

async def calc_gpa_needed(old_cgpa, new_cgpa, old_chours, new_chours):
    pass

async def calc_min_max_cgpa(old_chours, new_chours, old_cgpa):
    pass