import os
from django.contrib.auth.models import User

#call each populate method
def populate_db():
	populate_departments()
	populate_prgrm_strms()
	populate_courses()

# Function to populate the department table
def populate_departments():
    # Create some department chairs as they are necessary for department creation
	print("Populating department chair's...")
	CHEM_CHAIR = add_user(user=User.objects.create(username="ben",password="password"),type = "SP", email = "fakeEmail1@lolwut.com")
	CIVIL_CHAIR = add_user(user=User.objects.create(username="james",password="password"),type = "SP", email = "fakeEmail2@lolwut.com")
	ECE_CHAIR = add_user(user=User.objects.create(username="mccrae",password="password"),type = "SP", email = "fakeEmail3@lolwut.com")
	MECH_CHAIR = add_user(user=User.objects.create(username="speir",password="password"),type = "SP", email = "fakeEmail4@lolwut.com")
    
    # Create 4 departments...
	print("Populating departments...")
	add_department(name = "Chemical and Biochemical Engineering",head = CHEM_CHAIR, website = "http://www.eng.uwo.ca/chemical/")
	add_department(name = "Civil and Environmental Engineering", head = CIVIL_CHAIR,  website = "http://www.eng.uwo.ca/civil/")
	add_department(name = "Electrical and Computer Engineering", head = ECE_CHAIR, website = "http://www.eng.uwo.ca/electrical/")
	add_department(name = "Mechanical and Materials Engineering", head = MECH_CHAIR, website = "http://www.eng.uwo.ca/mechanical/")

# Function to populate program streams (9 of them)
def populate_prgrm_strms():
	print("Populating program streams...")
	
	add_program_strm(name="Chemical Engineering", department=Department.objects.get(name="Chemical and Biochemical Engineering"))

	add_program_strm(name="Civil Engineering", department=Department.objects.get(name="Civil and Environmental Engineering"))

	add_program_strm(name="Computer Engineering", department=Department.objects.get(name="Electrical and Computer Engineering"))

	add_program_strm(name="Electrical Engineering", department=Department.objects.get(name="Electrical and Computer Engineering"))

	add_program_strm(name="Green Process Engineering", department=Department.objects.get(name="Chemical and Biochemical Engineering"))

	add_program_strm(name="Integrated Engineering", department=Department.objects.get(name="Civil and Environmental Engineering"))

	add_program_strm(name="Mechanical Engineering", department=Department.objects.get(name="Mechanical and Materials Engineering"))

	add_program_strm(name="Mechatronic Systems Engineering", department=Department.objects.get(name="Mechanical and Materials Engineering"))

	add_program_strm(name="Software Engineering", department=Department.objects.get(name="Electrical and Computer Engineering"))

def populate_courses():
	print("Populating courses...")
	add_course(course_code="ES1050", name="Introductory Engineering Design and Innovation Studio", lecture_hours='3', lab_hours='4', credit='2', year="FI")

	add_course(course_code="AM1413", name="Applied Mathematics for Engineers", lecture_hours='3', lab_hours='0', credit='1', year="FI")


# Methods to add objects to the database:
def add_user(user, type, email):
	u = UserInfo.objects.get_or_create(user= user, email=email, type = type)[0]
	return u

def add_department(name, head, website):
	d = Department.objects.get_or_create(name=name, head=head, website=website)[0]
	return d

def add_program_strm(name, department):
	ps = ProgramStream.objects.get_or_create(name=name, department=department)[0]
	return ps

def add_course(course_code, name, lecture_hours, lab_hours, credit, year):
	c = Course.objects.get_or_create(course_code=course_code, name=name, lecture_hours=lecture_hours, lab_hours=lab_hours, credit=credit, year=year)[0]
	return c

# Start script execution here
if __name__ == '__main__':
	print("Starting curriculum-map population script...")
	os.environ.setdefault('DJANGO_SETTINGS_MODULE','project.settings')
	from curriculum.models import UserInfo, Department, ProgramStream, Course
	populate_db()
	print("Database population complete.")