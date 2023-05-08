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
		The grades needed to acquire a specific gpa. Type: list

	Raises:
		None
	"""
	if type(gpa) == str:	# Handles error
		return gpa 

	i = 0 								# Grade
	temp = 0.00							# Temporary gpa, 
	grade = getList(main_grades)		# Get the grades (A to F)
	grades_needed = []			
	while True:					
		temp += main_grades[grade[i]]/course_num	# Add gradepoint of grade to temp	

		if temp > gpa and i > 5: 	# E and F carry zero weight. So end loop, when grade is on 5(E) and temp > gpa
			break

		if temp > gpa:				# If Grade[i] can't be added without exceeding gpa, delete added value and rollover to next grade.
			temp -= main_grades[grade[i]]/course_num		
			i += 1
		else:
			grades_needed.append(grade[i])			#If it can, add grade letter to list and continue.
	return grades_needed
	# 	if len(grades_needed) == 0:
	# 		return f"For the specifics above, you'll need a {gpa} GPA which requries you to fail all courses."

	# return f"For this info, you'll need a {gpa} GPA which requires minimum grade(s) of {grades_needed}"

