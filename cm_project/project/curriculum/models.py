from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime, time

# User model
class UserInfo(models.Model):
	# One to one field implies inheritance from User class
	user = models.OneToOneField(User)
	website = models.URLField(blank = True)
	picture = models.ImageField(upload_to = 'profile_images', blank = True)
	
	# Define different user types
	USER_TYPES = (('PR','Professor'), ('TA', 'Teaching Assistant'), ('GN','General'), ('SP', 'Special'))
	type = models.CharField(max_length = 2, choices = USER_TYPES, default = 'GN')
	
	def __str__(self):
		return self.user.username

# Department model
class Department(models.Model):
	name = models.CharField(max_length = 128, unique = True)
	head = models.OneToOneField(UserInfo)
	website = models.URLField(blank = True)
	
	@property
	def get_url(self):
		department_url = self.name.replace(' ', '_')
		return department_url
	
	def __str__(self):
		return self.name
		
		
# Concept model
class Concept(models.Model):
	name = models.CharField(max_length = 128, unique = True)
	description = models.CharField(max_length = 500, blank = False)
	highscool = models.BooleanField(default = False)
	
	# Options for CEAB accreditation units
	ACCREDITATION_TYPES = (('MA', 'Math'), ('SC', 'Science'), ('ES', 'Engineering Science'),
							('ED', 'Engineering Design'), ('CO', 'Complementary Studies'))
	ceab_unit = models.CharField(max_length = 2, choices = ACCREDITATION_TYPES, blank = False)
	
	# Relate concepts to to themselves
	related_concepts = models.ManyToManyField('self',blank = True)
	
	def get_url(self):
		concept_url = self.name.replace(' ', '_')
		return concept_url
		
	def __str__(self):
		return self.name
		
# Course model
class Course(models.Model):
	course_code = models.CharField(max_length = 12, unique = True)
	name = models.CharField(max_length = 128, unique = True)
    
	lecture_hours = models.FloatField(default=0.0, blank = False)
	lab_hours = models.FloatField(default=0.0, blank = False)
	tut_houts = models.FloatField(default = 0.0, blank = False)
	credit = models.FloatField(blank = False)
    
	description = models.CharField(max_length = 500, blank = True)
	website = models.URLField(blank = True)
    
	
	# Define options for class year
	YEAR_TYPES = (('FI','First'), ('SE', 'Second'), ('TH','Third'), ('FO', 'Fourth'), ('GR', 'Graduate'))
	year = models.CharField(max_length = 2, choices = YEAR_TYPES, blank = False)
	
	# Create a recursive relationship with other course 
	# objects to link a course to its requisite courses
	# *** REMEMBER TO MAKE THESE MUTUALLY EXCLUSIVE ***
	pre_requisites = models.ManyToManyField('self', symmetrical = False, related_name='pre', blank = True)
	anti_requisites = models.ManyToManyField('self', symmetrical = False, related_name='anti', blank = True)
	co_requisites = models.ManyToManyField('self', symmetrical = False, related_name='co', blank = True)
	
	# Definte a function to get the combined lab and tutorial hours
	@property
	def get_contact_value(self):
		hours = self.lab_hours + self.tut_hours
		hours = hours * 0.5
		hours = hours + self.lecture_hours
		weeks = 12.6 * self.credit * 2
		hours = hours * weeks

		return hours
	
	# Define a function that can be used within templates that will return the url for the course
	@property
	def get_url(self):
		return self.course_code.replace('/','_')		

	def __str__(self):
		return self.course_code
		
# Course instance model, an actualization of a course
# Course instance(s) and a course have a many to one relationship 
class CourseInstance(models.Model):
	course = models.ForeignKey(Course)
	date = models.DateField(blank = False)
	textbook = models.CharField(max_length = 128, blank = True)

	# Professors and T.A.'s require m2m relations so that multiple teachers can teacher multiple courses
	professors = models.ManyToManyField(UserInfo, related_name = 'teaches')
	assistants = models.ManyToManyField(UserInfo, related_name = 'assists', blank = True)
    
	# Hold the percent values for accreditation categories (calculated automatically?)
	acc_math = models.IntegerField(blank = True, default=0)
	acc_science = models.IntegerField(blank = True, default=0)
	acc_eng_science = models.IntegerField(blank = True, default=0)
	acc_eng_design = models.IntegerField(blank = True, default=0)
	acc_comp = models.IntegerField(blank = True, default=0)
	
	# Define options for semester course is taught in
	SEMESTER_TYPES = (('F', 'First'), ('S', 'Second'), ('Y', 'Year'))
	semester = models.CharField(max_length = 1, choices = SEMESTER_TYPES, blank = False)
	
	# Define concepts covered in this course
	concepts = models.ManyToManyField(Concept, blank = True)
	
	# concept timeline of when concepts are taught
	concept_timeline = list()
	
	# Define contact hours for each accreditation unit
	@property
	def get_date(self):
		DATE_FORMAT = "%Y-%m-%d" 
		date_url = self.date
		d = date_url.strftime(DATE_FORMAT)
		d = d.replace('-', '_')
		return d
	
	@property
	def get_professors(self):
		return self.professors.all()

	@property
	def get_assistants(self):
		return self.assistants.all()

	@property
	def get_concepts(self):
		return self.concepts.all()

	def __str__(self):
		return "Instance of "+self.course.course_code+" ("+self.get_date+")"
		
# Model for a course deliverable (Assignment, Quiz, Test, etc...)
class Deliverable(models.Model):
	DELIVERABLE_TYPES = (('A', 'Assignment'),('Q', 'Quiz'), ('T', 'Test'), ('M', 'Midterm'), ('F', 'Final Exam'))
	type = models.CharField(max_length = 1, choices = DELIVERABLE_TYPES)
	percent = models.IntegerField(blank = False)
	due_date = models.DateField(blank = True)
	course_instance = models.ForeignKey(CourseInstance)
	
	def __str__(self):
		return self.type
		
# Model for a course learning objective 
class LearningObjective(models.Model):
	name = models.CharField(max_length = 128, blank = False)
	description = models.CharField(max_length = 500, blank = False)
	related_concepts = models.ManyToManyField(Concept, blank = True)
	
	# Relate a learning objective to a particular course instance
	course_instance = models.ForeignKey(CourseInstance)
	
	def __str__(self):
		return self.name
		
		
# Program Stream model
class ProgramStream(models.Model):
	name = models.CharField(max_length = 128, unique = True)
	description = models.TextField(max_length= 850, blank = True)
	
	# Department is the parent of a program stream
	department = models.ForeignKey(Department)
	
	# Program stream is made up of courses
	courses = models.ManyToManyField(Course, related_name = 'course_list')
	
	@property
	def get_url(self):
		return self.name.replace(' ','_')

	
	def __str__(self):
		return self.name

# Option Model
class Option(models.Model):
	name = models.CharField(max_length=128, unique=True)
	# Linked to Program Stream through Foreign Key
	program_stream = models.ForeignKey(ProgramStream)
	#m2m relation with courses to be added to program, and removed from program
	added_courses = models.ManyToManyField(Course, related_name='courses_added', blank=True)
	removed_courses = models.ManyToManyField(Course,related_name='courses_removed', blank=True)

	@property
	def get_url(self):
		return self.name.replace(' ','_')

	#use this function to get the courses from the program_stream, add the added_courses, remove the removed_courses, and return the resultant list
	@property
	def get_courses(self):
		return

	def __str__(self):
		return self.name

# CEAB Accreditation Units
# ~~ Still not sure if we need this... might come in handy ~~
class ContactHours(models.Model):
	instance = models.ForeignKey(CourseInstance)
	
	contact_es = models.FloatField(blank = True, default = 0.0)
	contact_ed = models.FloatField(blank = True, default = 0.0)
	contact_ma = models.FloatField(blank = True, default = 0.0)
	contact_sc = models.FloatField(blank = True, default = 0.0)
	contact_co = models.FloatField(blank = True, default = 0.0)
	
	def save(self, *args, **kwargs):
		contact_coefficient = self.instance.course.get_contact_value()
		self.contact_es = self.instance.acc_eng_science * contact_coefficient
		self.contact_ed = self.instance.acc_eng_design * contact_coefficient
		self.contact_ma = self.instance.acc_math * contact_coefficient
		self.contact_sc = self.instance.acc_science * contact_coefficient
		self.contact_co = self.instance.acc_eng_comp * contact_coefficient
		super(Model, self).save(*args, **kwargs)
	
	def __str__(self):
		return self.instance.name+"contact hours"
		
# CEAB Graduate Attributes
class CEABGrad(models.Model):
	name = models.CharField(max_length = 128, unique = True)
	date = models.DateField(blank = False)
	measurement_text = models.TextField(max_length = 500, blank = True)
	measurement_file = models.FileField(upload_to = 'ceab_files', blank = True)
	rubrik = models.FileField(upload_to = 'rubrik_files', blank = True)
	average = models.FloatField(blank = True)
	median = models.FloatField(blank = True)
	low = models.FloatField(blank = True)
	high = models.FloatField(blank = True)
	num_students = models.IntegerField(blank = True)
	level1 = models.IntegerField(default = 0)
	level2 = models.IntegerField(default = 0)
	level3 = models.IntegerField(default = 0)
	level4 = models.IntegerField(default = 0)
	
	# Attribute types
	ATTRIBUTE_TYPES = (('KB', 'Knowledge Base'), ('PA', 'Problem Analysis'), ('IV','Investigation'), ('DE','Design'), ('ET','Engineering Tools'),
						('IT','Individual and Team Work'), ('CS','Communication Skills'), ('PR','Professionalism'), ('EI','Engineering Impact'),
						('EE','Ethics and Equity'), ('EP','Economics and Project Management'), ('LL','Lifelong Learning'))
	attribute = models.CharField(max_length = 2, choices = ATTRIBUTE_TYPES, blank = False)
	
	# Link this Graduate Attribute measurement to a course_instance
	course = models.ForeignKey(CourseInstance)
	
	def __str__(self):
		return self.name
		

		
