main_grades = {"A": 4.0, "B+": 3.5,
		 "B": 3.0, "C+": 2.5, 
		 "C": 2.0, "D+": 1.5,
		 "D": 1.0, "E": 0,
		 "F": 0}


def getList(dict):
	"""Returns dict keys as list.

	Args: 
		dict: Dictionary. Type: dict

	Returns:
		Dictionary keys of type list

	Raises:
		None
	""" 
	return list(dict.keys())


def grade_to_classification(gpa):
	"""Transorm a GPA to it's corresponding level.

	Args: 
		GPA: Users gpa. Type: float

	Returns:
		The corresponding level of inputted GPA. Type: String	

	Raises:
		None
	"""
	if gpa >= 3.60:
		return "First Class"
	elif gpa >= 3.00: 
		return "Second Class Upper"
	elif gpa >= 2.00:
		return "Second class Lower"
	elif gpa >= 1.50:
		return "Third Class"
	elif gpa >= 1.00:
		return "Pass"
	elif gpa < 1.00:
		return "Fail"
	else:
		return "Invalid Input"
	

def gpa_to_grades(gpa, course_num):
    """Converts GPA to grades

    Args: 
        gpa: Your current cgpa. Type: float or int.
        course_num: number of courses. Type: int

    Returns:
        The grades needed to acquire a specific GPA as a string. Format: "<grade>: <count>, <grade>: <count>, ..."

    Raises:
        None
    """
    if type(gpa) == str:  # Handles error
        return gpa

    i = 0  # Grade
    temp = 0.00  # Temporary GPA
    grade = getList(main_grades)  # Get the grades (A to F)
    grades_needed = {}

    while True:
        temp += main_grades[grade[i]] / course_num  # Add gradepoint of grade to temp

        if temp > gpa and i > 5:  # E and F carry zero weight. So end loop when grade is on 5(E) and temp > gpa
            break

        if temp > gpa:  # If Grade[i] can't be added without exceeding GPA, delete added value and rollover to next grade.
            temp -= main_grades[grade[i]] / course_num
            i += 1
        else:
            if grade[i] in grades_needed:
                grades_needed[grade[i]] += 1
            else:
                grades_needed[grade[i]] = 1

    return ', '.join([f"{grade}: {count}" for grade, count in grades_needed.items()])


def calculate_fgpa(data):
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

          # GPA statistics
        cgpa_list = [cgpa1, cgpa2, cgpa3, cgpa4]
        highest_cgpa = max(cgpa_list)
        lowest_cgpa = min(cgpa_list)
        average_cgpa = sum(cgpa_list) / len(cgpa_list)
        
        return {
            "cgpa1": str(cgpa1),
            "cgpa2": str(cgpa2),
            "cgpa3": str(cgpa3),
            "cgpa4": str(cgpa4),
            "fgpa": str(final_gpa),
            "classification": levels,
            "highest_cgpa": str(highest_cgpa),
            "lowest_cgpa": str(lowest_cgpa),
            "average_cgpa": str(round(average_cgpa, 2)),
            }
    
    except Exception as e:
        return {"error": str(e)}

def calculate_min_max_cgpa(data):
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


def calculate_new_gpa(data):
    grades_list = data.grades
    credits_list = data.credit
    
    try:
        total_gpt = 0
        for i in range(len(grades_list)):
            if grades_list[i] not in main_grades.keys():
                return {"result" : "Invalid Grades"}
            
            grades_list[i] = main_grades[grades_list[i]]
            total_gpt += grades_list[i] * credits_list[i]		# Total gradepoint
            
        gpa = total_gpt / sum(credits_list)
        gpa = round(gpa, 2)

        levels = grade_to_classification(gpa)		# Retrieve level of maximum CGPA

        res = f"For {total_gpt} total grade point and {sum(credits_list)} credit hours, your CGPA is {gpa} ({levels})"
        return {"feedback": res}
    
    except Exception as e:
        return{"result" : str(e)}


def calculate_req_grades(data):
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
