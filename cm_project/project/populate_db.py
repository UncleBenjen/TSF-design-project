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
	CHEM_CHAIR = add_user(user=User.objects.create(username="ben",password="password",email = "fakeEmail1@lolwut.com"),type = "SP")
	CIVIL_CHAIR = add_user(user=User.objects.create(username="james",password="password", email = "fakeEmail2@lolwut.com"),type = "SP")
	ECE_CHAIR = add_user(user=User.objects.create(username="mccrae",password="password", email = "fakeEmail3@lolwut.com"),type = "SP")
	MECH_CHAIR = add_user(user=User.objects.create(username="speir",password="password", email = "fakeEmail4@lolwut.com"),type = "SP")
    
    # Create 4 departments...
	print("Populating departments...")
	add_department(name = "Chemical and Biochemical Engineering",head = CHEM_CHAIR, website = "http://www.eng.uwo.ca/chemical/")
	add_department(name = "Civil and Environmental Engineering", head = CIVIL_CHAIR,  website = "http://www.eng.uwo.ca/civil/")
	add_department(name = "Electrical and Computer Engineering", head = ECE_CHAIR, website = "http://www.eng.uwo.ca/electrical/")
	add_department(name = "Mechanical and Materials Engineering", head = MECH_CHAIR, website = "http://www.eng.uwo.ca/mechanical/")

# Function to populate program streams (9 of them)
def populate_prgrm_strms():
	print("Populating program streams...")
	
	add_program_strm(name="Chemical Engineering", department=Department.objects.get(name="Chemical and Biochemical Engineering"), description = "Chemical and Biochemical Engineering is a versatile discipline broadly based upon physical and life sciences. Today the world faces significant challenges due to increasing populations, air, water and soil pollution, and world-wide energy and food shortages. Chemical engineers are well positioned through their training to address and find solutions to these challenges. This program educates engineers to design, develop and operate chemical processes to make useful products such as plastics, polymers, medicines, food, fuels, fertilizers, detergents, cosmetics, and consumer goods at minimum cost in a safe and environmentally sustainable way. Chemical engineers also translate and scale-up processes developed by basic scientists into practical applications that benefit society and lead to economic development.")

	add_program_strm(name="Civil Engineering", department=Department.objects.get(name="Civil and Environmental Engineering"), description = "Civil Engineering is a broad discipline that uses applied and leading-edge science to improve the quality of life by providing essential services, solving environmental problems resulting from industrialization and resource consumption, and mitigating natural disasters. The design course in final year allows you to gain practical experience working on group projects with the City of London and industry professionals. Over the years, projects have included a new grandstand for a baseball park, proposals for storm water management and bridge and tower designs.")

	add_program_strm(name="Computer Engineering", department=Department.objects.get(name="Electrical and Computer Engineering"), description = "Computer Engineering studies the design of hardware elements and the building of computer systems of various levels of complexity. These systems may vary from high performance parallel supercomputers, to special servers that operate computer networks, to micro devices that will operate the next generation of home appliances.")

	add_program_strm(name="Electrical Engineering", department=Department.objects.get(name="Electrical and Computer Engineering"), description = "Electrical Engineering is a diverse, fast growing and vibrant field of engineering. In this program you will learn how to harness electrical energy for human benefit. Use of electrical energy is versatile and our program covers a broad range of applications. Examples include telecommunications, digital electronics, computers, robots, electric motors, all sizes of generators, electric power distribution systems, and electric cars.")

	add_program_strm(name="Green Process Engineering", department=Department.objects.get(name="Chemical and Biochemical Engineering"), description = "Western Engineering is proud to offer Canada’s first Green Process Engineering program. The curriculum integrates the fundamental principles of chemical engineering to design commercial products and processes that are safe, economical and environmentally friendly by reducing waste generation. The program also explores alternative sources of energy with reduced carbon emissions.  Some of the distinguishing features of the program include the emphasis on green chemistry, green power, solar and bio-fuel cells, and conversion of waste, such as agricultural byproducts to bio-diesel and bio-ethanol products.")

	add_program_strm(name="Integrated Engineering", department=Department.objects.get(name="Civil and Environmental Engineering"), description = "Our newly redesigned Integrated Engineering program is different than any other program offered in Canada. We offer students the opportunity to learn all areas of engineering while developing skills in management, leadership and innovation. Integrated Engineering students will participate in class lectures, engineering laboratories and tutorials as well as group discussions and case-based learning, in courses such as business administration, venture creation, and marketing and design thinking.")

	add_program_strm(name="Mechanical Engineering", department=Department.objects.get(name="Mechanical and Materials Engineering"), description = "Mechanical Engineering is one of the broadest engineering disciplines and its products are found everywhere. Our program focuses on a broadly based mechanical and materials engineering education that stresses fundamental engineering concepts, contemporary design practices, development of interpersonal skills and interaction with engineering practitioners. You will work closely with faculty and industry partners to apply knowledge and leadership skills by participating in real world design and construction projects.")

	add_program_strm(name="Mechatronic Systems Engineering", department=Department.objects.get(name="Mechanical and Materials Engineering"), description = "Mechatronics is the combination of mechanical, electrical, computer, control, and systems design engineering to create useful products. The combination of these engineering principles helps generate simpler, more economical, reliable and versatile systems. Our program will be unique in its multi-year design focus. Throughout the program, you will take core courses in Electrical and Computer Engineering as well as core courses in Mechanical and Materials Engineering.")

	add_program_strm(name="Software Engineering", department=Department.objects.get(name="Electrical and Computer Engineering"), description = "The development of software systems is now regarded among the most innovative work performed by mankind. Software engineers are trained for the specification, design, implementation, and maintenance of software systems. Western’s Software Engineering program has a core of disciplines that covers all phases of the software cycle. This program offers a solid foundation in computer hardware and computer networks, while exploring the essentials of computer science.")

def populate_courses():
	print("Populating courses...")
	add_course(course_code="ES1050", name="Introductory Engineering Design and Innovation Studio", lecture_hours='3', lab_hours='4', credit='2', year="FI")

	add_course(course_code="AM1413", name="Applied Mathematics for Engineers", lecture_hours='3', lab_hours='0', credit='1', year="FI")

	add_course(course_code="ES1022A/B/Y", name="Engineering Statics", lecture_hours='2', lab_hours='1', credit='0.5', year="FI")

	add_course(course_code="AM1411A/B", name="Linear Algebra for Engineers", lecture_hours='3', lab_hours='2', credit='0.5', year='FI')

	add_course(course_code="CHEM1024A/B", name="General Chemistry for Engineers", lecture_hours='3', lab_hours='3', credit='0.5', year='FI')
    
	add_course(course_code="ES1021A/B", name="Properties of Materials", lecture_hours='3', lab_hours='2', credit='0.5', year='FI')
    
	add_course(course_code="ES1036A/B", name="Programming Fundamentals for Engineers", lecture_hours='3', lab_hours='3', credit='0.5', year='FI')
    
	add_course(course_code="PHYS1401A/B", name="Physics for Engineering Students I", lecture_hours='2', lab_hours='3', credit='0.5', year='FI')
    
	add_course(course_code="PHYS1402A/B", name="Physics for Engineering Students II", lecture_hours='2', lab_hours='3', credit='0.5', year='FI')
    
	add_course(course_code="1 NTE", name="Approved Non-Technical Elective", lecture_hours='3', lab_hours='0', credit='1.0', year='FI')

# Methods to add objects to the database:
def add_user(user, type):
	u = UserInfo.objects.get_or_create(user= user, type = type)[0]
	return u

def add_department(name, head, website):
	d = Department.objects.get_or_create(name=name, head=head, website=website)[0]
	return d

def add_program_strm(name, department, description):
	ps = ProgramStream.objects.get_or_create(name=name, department=department, description=description)[0]
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