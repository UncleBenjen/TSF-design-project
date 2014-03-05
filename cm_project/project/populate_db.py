import os
from django.contrib.auth.models import User
from curriculum.models import UserInfo, Department, ProgramStream, Option, Course

#call each populate method in correct order
def populate_db():
	populate_departments()
	populate_courses()
	populate_prgrm_strms()
	populate_options()
	connect_courses()
	populate_mechanical()

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

#populate the options
def populate_options():
	print("Populating Options")

	#Try to find the chemical program and create the options associated with it, else print fail-message
	try:
		chem_eng = ProgramStream.objects.get(name = "Chemical Engineering")
		add_option(name="Chemical Engineering Option", program_stream=chem_eng)
		add_option(name="Biochemical and Environmental Engineering Option", program_stream=chem_eng)
		add_option(name="Chemical Engineering and Management Option", program_stream=chem_eng)
		add_option(name="Chemical Engineering and Law Option", program_stream=chem_eng)
		print(" - Successfully populated chemical engineering options...")
	except ProgramStream.DoesNotExist:
		print(" ~ Could not populate chemical engineering options...")

	#Try to find the civil program and create the options associated with it, else print fail-message
	try:
		civil_eng = ProgramStream.objects.get(name = "Civil Engineering")
		add_option(name="Civil and Structural Engineering Option", program_stream=civil_eng)
		add_option(name="Environmental Engineering Option", program_stream=civil_eng)
		add_option(name="Civil Engineering and Law Option", program_stream=civil_eng)
		add_option(name="Civil Engineering and Medicine Option", program_stream=civil_eng)
		add_option(name="Environmental Engineering with International Development Option", program_stream=civil_eng)
		add_option(name="Structural Engineering with International Development Option", program_stream=civil_eng)
		print(" - Successfully populated civil engineering options...")
	except ProgramStream.DoesNotExist:
		print(" ~ Could not populate civil engineering options...")

	#Try to find the computer program and create the options associated with it, else print fail-message
	try:
		comp_eng = ProgramStream.objects.get(name = "Computer Engineering")
		add_option(name="Computer Engineering Option", program_stream=comp_eng)
		print(" - Successfully populated civil engineering options...")
	except ProgramStream.DoesNotExist:
		print(" ~ Could not populate computer engineering options...")

	#Try to find the electrical program and create the options associated with it, else print fail-message
	try:
		elec_eng = ProgramStream.objects.get(name = "Electrical Engineering")
		add_option(name="Electrical Engineering Option", program_stream=elec_eng)
		add_option(name="Electrical Engineering and Management Option", program_stream=elec_eng)
		add_option(name="Electrical Engineering and Wireless Communication Option", program_stream=elec_eng)
		add_option(name="Electrical Engineering and Law Option", program_stream=elec_eng)
		add_option(name="Electrical Engineering Power Systems Engineering Option", program_stream=elec_eng)
		add_option(name="Electrical Engineering and Medicine Option", program_stream=elec_eng)
		add_option(name="Electrical Engineering Biomedical Signals and Systems Option", program_stream=elec_eng)
		print(" - Successfully populated electrical engineering options...")
	except ProgramStream.DoesNotExist:
		print(" ~ Could not populate electrical engineering options...")

	#Try to find the green process program and create the options associated with it, else print fail-message
	try:
		green_eng = ProgramStream.objects.get(name = "Green Process Engineering")
		add_option(name="Green Process Engineering Option", program_stream=green_eng)
		add_option(name="Green Process Engineering with Management Option", program_stream=green_eng)
		add_option(name="Green Process Engineering with Law Option", program_stream=green_eng)
		print(" - Successfully populated green process engineering options...")
	except ProgramStream.DoesNotExist:
		print(" ~ Could not populate green process engineering options...")

	#Try to find the integrated program and create the options associated with it, else print fail-message
	try:
		integrated_eng = ProgramStream.objects.get(name = "Integrated Engineering")
		add_option(name="Integrated Engineering Option", program_stream=integrated_eng)
		add_option(name="Integrated Engineering and Management Option", program_stream=integrated_eng)
		add_option(name="Integrated Engineering and Medicine Option", program_stream=integrated_eng)
		add_option(name="Integrated Engineering and Law Option", program_stream=integrated_eng)
		print(" - Successfully populated integrated engineering options...")
	except ProgramStream.DoesNotExist:
		print(" ~ Could not populate green process engineering options...")

	#Try to find the mechanical program and create the options associated with it, else print fail-message
	try:
		mech_eng = ProgramStream.objects.get(name = "Mechanical Engineering")
		add_option(name="Mechanical Engineering Option", program_stream=mech_eng)
		add_option(name="Mechanical Engineering and Law Option", program_stream=mech_eng)
		add_option(name="Mechanical Engineering and Medicine Option", program_stream=mech_eng)
		add_option(name="Mechanical Engineering and Business Option", program_stream=mech_eng)
		print(" - Successfully populated mechanical engineering options...")
	except ProgramStream.DoesNotExist:
		print(" ~ Could not populate mechanical engineering options...")

	#Try to find the mechatronic systems program and create the options associated with it, else print fail-message
	try:
		mechatronic_eng = ProgramStream.objects.get(name = "Mechatronic Systems Engineering")
		add_option(name="Mechatronic Systems Engineering Option", program_stream=mechatronic_eng)
		add_option(name="Mechatronic Systems Engineering and Management Option", program_stream=mechatronic_eng)
		add_option(name="Mechatronic Systems Engineering and Law Option", program_stream=mechatronic_eng)
		print(" - Successfully populated mechatronic systems engineering options...")
	except ProgramStream.DoesNotExist:
		print(" ~ Could not populate mechatronic systems engineering options...")

	#Try to find the software program and create the options associated with it, else print fail-message
	try:
		soft_eng = ProgramStream.objects.get(name = "Software Engineering")
		add_option(name="Software Engineering Option", program_stream=soft_eng)
		add_option(name="Software Engineering and Management Option", program_stream=soft_eng)
		add_option(name="Software Engineering and Law Option", program_stream=soft_eng)
		add_option(name="Software Engineering Embedded Systems Option", program_stream=soft_eng)
		add_option(name="Software Engineering Health Informatics Option", program_stream=soft_eng)
		add_option(name="Software Engineering and Medicine Option", program_stream=soft_eng)
		print(" - Successfully populated software engineering options...")
	except ProgramStream.DoesNotExist:
		print(" ~ Could not populate software engineering options...")

#populate first year courses
def populate_courses():
	print("Populating first year courses...")
	add_course(course_code="ES1050", name="Introductory Engineering Design and Innovation Studio", lecture_hours='3', lab_hours='4', credit='2', description="Introduction to the principles and practices of professional engineering. The design studio fosters innovative thinking, improves problem solving, and provides context. Includes elements of need recognition, conceptualization, prototyping, and engineering design to satisfy commercial specifications. Emphasis on creativity, teamwork, communication and engineering skills necessary to practice in any engineering discipline.", year="FI")

	add_course(course_code="AM1413", name="Applied Mathematics for Engineers", lecture_hours='3', lab_hours='0', credit='1', description="The calculus of functions of one and more variables with emphasis on applications in Engineering.", year="FI")

	add_course(course_code="ES1022A/B/Y", name="Engineering Statics", lecture_hours='2', lab_hours='1', credit='0.5', description="Analysis of forces on structures and machines, including addition and resolution of forces and moments in two and three-dimensions. The application of the principles of equilibrium. Topics: trusses; frames; friction; and centroids.",year="FI")

	add_course(course_code="AM1411A/B", name="Linear Algebra for Engineers", lecture_hours='3', lab_hours='2', credit='0.5', description="Matrix operations, systems of linear equations, linear spaces and transformations, determinants, eigenvalues and eigenvectors, applications of interest to Engineers including diagonalization of matrices, quadratic forms, orthogonal transformations.",year='FI')

	add_course(course_code="CHEM1024A/B", name="General Chemistry for Engineers", lecture_hours='3', lab_hours='3', credit='0.5', description="This course provides a basic understanding of the following topics: gas laws; chemical equilibrium; acid-base equilibria; thermodynamics and thermochemistry; chemical kinetics; electrochemistry. Restricted to students in Engineering and Geophysics programs.",year='FI')
    
	add_course(course_code="ES1021A/B", name="Properties of Materials", lecture_hours='3', lab_hours='2', credit='0.5', description="An introduction to the relationship between the microstructure and engineering properties of metals, ceramics, polymers, semi-conductors and composites.", year='FI')
    
	add_course(course_code="ES1036A/B", name="Programming Fundamentals for Engineers", lecture_hours='3', lab_hours='3', credit='0.5', description="Designing, implementing and testing computer programs using a modern object-oriented language such as C++ to fulfill given specifications for small problems using sound engineering principles and processes. Awareness of the engineering aspects of the process of constructing a computer program.", year='FI')
    
	add_course(course_code="PHYS1401A/B", name="Physics for Engineering Students I", lecture_hours='2', lab_hours='3', credit='0.5', description="A calculus-based laboratory course in physics for Engineering students. Kinematics, Newton’s laws of motion, work, energy, linear momentum, rotational motion, torque and angular momentum, oscillations.", year='FI')
    
	add_course(course_code="PHYS1402A/B", name="Physics for Engineering Students II", lecture_hours='2', lab_hours='3', credit='0.5', description="A calculus-based laboratory course in physics for Engineering students. Electric fields and potential, Gauss’ law, capacitance, DC circuits, magnetic fields, electromagnetic induction.", year='FI')
    
	add_course(course_code="1 NTE", name="Approved Non-Technical Elective", lecture_hours='3', lab_hours='0', credit='1.0', description="The Canadian Engineering Accreditation Board (CEAB) requires that engineering programs include a course requirement that teaches the central issues, methodologies and thought processes of the Humanities and Social Sciences.  Please note that language courses do not meet this requirement.", year='FI')

#create a function that will add the first year courses to the program streams...
def connect_courses():
	try:
		print("Connecting the first year courses with the programs streams...")
		streams = ProgramStream.objects.all()
		first_year_courses = Course.objects.filter(year='FI')

		#loop through the streams, and add the common first year courses to each one
		for stream in streams:
			for course in first_year_courses:
				stream.courses.add(course)

	except:
		print("Connecting courses failed... ")
		pass

def populate_mechanical():
	try:
		mech_eng = ProgramStream.objects.get(name = "Mechanical Engineering")
		print("Creating second year courses for mechanical program...")

		#create and add 2nd year courses to mech program
		mech_eng.courses.add(add_course(course_code="AM2413",name="Applied Mathematical and Numerical Methods for Mechanical Engineering",lecture_hours='3', lab_hours='1.5',credit='1.0',description="Topics include: Introduction to Matlab; numerical differentiation and integration; numerical linear algebra; ordinary differential equations including higher order systems and numerical solutions; interpolation and approximation; multiple integrals and vector integral theorems.", year='SE'))
		mech_eng.courses.add(add_course(course_code="MME2202A/B",name="Mechanics of Materials",lecture_hours='3', lab_hours='3.5',credit='0.5',description="Stress and strain, Mohr's stress circle, behaviour of structures, axial loading of columns and struts, torsion of shafts, bending of beams, buckling of columns and combined loading of components", year='SE'))
		mech_eng.courses.add(add_course(course_code="MME2204A/B",name="Thermodynamics I",lecture_hours='3', lab_hours='2.5',credit='0.5',description="Properties of a pure substance, first law of thermodynamics, processes in open and closed systems, second law of thermodynamics; ideal gases, compressors and energy conversion systems.", year='SE'))
		mech_eng.courses.add(add_course(course_code="MME2259A/B",name="Product Design and Development",lecture_hours='3', lab_hours='3',credit='0.5',description="Introduction to the engineering design and structured design methods. Topics include: mechanical design process; concept generation and evaluation; embodiment design; design for manufacture and assembly; design for product safety; principles of life-cycle engineering.", year='SE'))
		mech_eng.courses.add(add_course(course_code="MME2260A/B",name="Industrial Materials",lecture_hours='3', lab_hours='3',credit='0.5',description="The principles and practice of shaping and strengthening industrial materials.", year='SE'))
		mech_eng.courses.add(add_course(course_code="MME2200Q/Y",name="Engineering Shop Safety Training",lecture_hours='0', lab_hours='0',credit='0.0',description="This course will provide mechanical engineering undergraduate students with uniform training in the safe use of Engineering student shops.", year='SE'))
		mech_eng.courses.add(add_course(course_code="ES2211F/G",name="Engineering Communications",lecture_hours='1', lab_hours='2',credit='0.5',description="This course is concerned with the communication of concepts and ideas by written, oral and graphical means. Practical work is emphasized.", year='SE'))
		mech_eng.courses.add(add_course(course_code="MME2213A/B",name="Engineering Dynamics",lecture_hours='3', lab_hours='2',credit='0.5',description="Topics include: rectilinear, angular and curvilinear motion; kinetics of a particle, a translating rigid body and a rigid body in pure rotation; definitions of different energies and energy balance: power and efficiency; and linear impulse and momentum.", year='SE'))
		mech_eng.courses.add(add_course(course_code="MME2273A/B",name="Heat Transfer and Dynamics",lecture_hours='3', lab_hours='2.5',credit='0.5',description="To provide the student with an understanding of the basic concepts of heat transfer and the dynamics of particles and rigid bodies.", year='SE'))
		mech_eng.courses.add(add_course(course_code="MME2285A/B",name="Engineering Experimentation",lecture_hours='3', lab_hours='2.5',credit='0.5',description="Measurement of physical quantities; experiment planning and design; characteristics of measurement systems; calibration, linearity, accuracy, bias and sensitivity; data acquisition systems; sampling theorem; signal conditioning; sources of errors; uncertainty analysis; data analysis techniques; systems for the measurement of displacement; velocity; acceleration; force, strain, pressure, temperature, flow rate, etc.", year='SE'))
		mech_eng.courses.add(add_course(course_code="SS2143A/B",name="Applied Statistics and Data Analysis for Engineers",lecture_hours='3', lab_hours='1',credit='0.5',description="A data-driven introduction to statistics intended primarily for students in Chemical and Mechanical Engineering. Exploratory data analysis, probability, the Binomial, Poisson, Normal, Chi-Square and F distributions. Estimation, correlation and regression (model building and parameter estimation), analysis of variance, design of experiments. Cannot be taken for credit in any module in Statistics, Actuarial Science, or Financial Modelling.", year='SE'))
		mech_eng.courses.add(add_course(course_code="ECE2247A/B",name="Electric Circuits and Electromechanics",lecture_hours='3', lab_hours='1.5',credit='0.5',description="This course studies the principles of electrical circuits and components including common electric motors employed in mechanical engineering systems. The course also uses a series of laboratories to introduce the students to common measurement tools used to assess and troubleshoot electrical circuits. The foundations from this course are expanded on in the subsequent course which focuses on electronic components and their application.", year='SE'))

		#create and add third year courses to mech program
		print("Creating third year courses for the mechanical program...")
		mech_eng.courses.add(add_course(course_code="AM3413A/B",name="Applied Mathematics for Mechanical Engineers",lecture_hours='3',lab_hours='0',credit='0.5',description="Topics include: Fourier series, integrals and transforms; boundary value problems in cartesian coordinates; separation of variables; Fourier and Laplace methods of solution.",year='TH'))
		mech_eng.courses.add(add_course(course_code="MME3303A/B",name="Fluid Mechanics II",lecture_hours='3',lab_hours='2.5',credit='0.5',description="Rigid-body motion and rotation, control volume method of analysis, conservation of mass, linear and angular momentum, centrifugal pumps, potential flow, dimensional analysis, viscous flow in channels and ducts, open channel flow, laminar and turbulent boundary layers, statistical description of turbulence",year='TH'))
		mech_eng.courses.add(add_course(course_code="MME3379A/B",name="Materials Selection",lecture_hours='3',lab_hours='1.5',credit='0.5',description="Application of computer databases to materials selection. Identification of the composite property for a particular application. Case studies of materials selection using variable property emphases. ",year='TH'))
		mech_eng.courses.add(add_course(course_code="MME3381A/B",name="Kinematics and Dynamics of Machines",lecture_hours='3',lab_hours='2.5',credit='0.5',description="Displacement, velocity and acceleration analysis of linkage mechanisms; inertia force analysis of mechanisms; balancing of reciprocating and rotating masses; introduction to vibration analysis of single-degree-of-freedom systems.",year='TH'))
		mech_eng.courses.add(add_course(course_code="ECE3374A/B",name="Introduction to Electronics for Mechanical Engineering",lecture_hours='3',lab_hours='1.5',credit='0.5',description="This course is an introduction to the electronics used to collect data and analyse and control mechanical and electrical systems. The first half of the course introduces basic electronic components, while the second half focuses on higher-level hardware used in data acquisition, sensor integration and motor control applications.",year='TH'))
		mech_eng.courses.add(add_course(course_code="MME3307A/B",name="Heat Transfer II",lecture_hours='3',lab_hours='2.5',credit='0.5',description="Transient heat conduction. Forced and natural convection heat transfer. Advanced radiation heat transfer, including surface properties and shape factor. Condensation and boiling heat transfer. Heat exchanger design, applications of heat transfer in Engineering Systems.",year='TH'))
		mech_eng.courses.add(add_course(course_code="MME3334A/B",name="Thermodynamics II",lecture_hours='3',lab_hours='2.5',credit='0.5',description="This course emphasizes the application of thermodynamic principles to engineering systems and problem solving. Topics covered include: sonic velocity and compressible flow through nozzles, reciprocating and rotary compressors, availability and irreversibility in systems and processes, cycles, psychometry of air conditioning, thermodynamic relations and the generalized compressiblity charts, chemical reactions and equilibrium.",year='TH'))
		mech_eng.courses.add(add_course(course_code="MME3350A/B",name="System Modelling and Control",lecture_hours='3',lab_hours='2.5',credit='0.5',description="Basic analytical techniques for modeling and control of dynamic systems. Solve for response as well as design controllers to shape response of systems. Applications to vibratory, thermo-fluidic, hydraulic, pneumatic and electro-mechanical systems.",year='TH'))
		mech_eng.courses.add(add_course(course_code="MME3360A/B",name="Finite Element Methods in Mechanical Engineering",lecture_hours='3',lab_hours='4',credit='0.5',description="Linear finite element analysis using the direct equilibrium method and the principle of minimum potential energy. Focus on structural mechanics using spring and bar elements (including two-dimensional trusses), beam elements, two-dimensional plane stress/strain elements, axisymmetric elements, and isoparametric formulation. Concepts of heat transfer, fluid flow, and thermal stress also introduced.",year='TH'))
		mech_eng.courses.add(add_course(course_code="MME3380A/B",name="Mechanical Components Design",lecture_hours='3',lab_hours='3',credit='0.5',description="The objective of this course is to consider the stress analysis and design of various components of a machine, e.g. an automobile. ",year='TH'))

	except ProgramStream.DoesNotExist:
		print("Populating the mechanical program failed.")
		pass

def populate_mechatronics():
	try:
		print("Populating mechatronics program...")
	except:
		print("Populating the mechatronics program failed")

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

def add_option(name, program_stream):
	o = Option.objects.get_or_create(name = name, program_stream=program_stream)
	return o

def add_course(course_code, name, lecture_hours, lab_hours, credit, description, year):
	c = Course.objects.get_or_create(course_code=course_code, name=name, lecture_hours=lecture_hours, lab_hours=lab_hours, credit=credit, description=description, year=year)[0]
	return c

# Start script execution here
if __name__ == '__main__':
	print("Starting curriculum-map population script...")
	os.environ.setdefault('DJANGO_SETTINGS_MODULE','project.settings')
	#Call population script
	populate_db()
	print("Database population complete.")