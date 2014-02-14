from django.db import models
from django.contrib.auth.models import User


# User model
class UserInfo(models.Model):
	# One to one field implies inheritance from User class
	user = models.OneToOneField(User)
	email = models.EmailField(blank = False, unique = True)
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
	related_concepts = models.ManyToManyField('self')
	
	def __str__(self):
		return self.name
		
# Course model
class Course(models.Model):
	name = models.CharField(max_length = 6, unique = True)
	credit = models.IntegerField(blank = False)
	description = models.CharField(max_length = 500, blank = False)
	website = models.URLField(blank = True)
	
	# Define options for class year
	YEAR_TYPES = (('FI','First'), ('SE', 'Second'), ('TH','Third'), ('FO', 'Fourth'), ('GR', 'Graduate'))
	year = models.CharField(max_length = 2, choices = YEAR_TYPES, blank = False)
	
	# Create a recursive relationship with other course 
	# objects to link a course to its requisite courses
	# *** REMEMBER TO MAKE THESE MUTUALLY EXCLUSIVE ***
	pre_requisites = models.ManyToManyField('self')
	anti_requisites = models.ManyToManyField('self')
	co_requisites = models.ManyToManyField('self')
	
	# Department this course belongs to
	department = models.ForeignKey(Department)

	def __str__(self):
		return self.name
		
# Course instance model, an actualization of a course
# Course instance(s) and a course have a many to one relationship 
class CourseInstance(models.Model):
	name = models.CharField(max_length = 6, unique = False)
	course = models.ForeignKey(Course)
	professors = models.ManyToManyField(UserInfo, related_name = 'teaches')
	assistants = models.ManyToManyField(UserInfo, related_name = 'assists')
	
	# Hold the percent values for accreditation categories
	acc_math = models.IntegerField(blank = True)
	acc_science = models.IntegerField(blank = True)
	acc_eng_science = models.IntegerField(blank = True)
	acc_eng_design = models.IntegerField(blank = True)
	acc_comp = models.IntegerField(blank = True)
	
	# Define options for semester course is taught in
	SEMESTER_TYPES = (('F', 'First'), ('S', 'Second'), ('Y', 'Year'))
	semester = models.CharField(max_length = 1, choices = SEMESTER_TYPES, blank = False)
	
	# Define concepts covered in this course
	concepts = models.ManyToManyField(Concept)
	
	def __str__(self):
		return self.name	
		
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
	description = models.CharField(max_length= 500, blank = False)
	
	# Department is the parent of a program stream
	department = models.ForeignKey(Department)
	
	# Program stream is made up of courses
	courses = models.ManyToManyField(Course, related_name = 'course_list')
	
	def __str__(self):
		return self.name

# CEAB Accreditation Units
class CEABUnit(models.Model):
	name = models.CharField(max_length = 128, unique = True)
	description = models.CharField(max_length = 128, blank = False)
	
	def __str__(self):
		return self.name
		
# CEAB Graduate Attributes
class CEABGrad(models.Model):
	name = models.CharField(max_length = 128, unique = True)
	date = models.DateField(blank = False)
	measurement = models.FileField(upload_to = 'ceab_files', blank = False)
	average = models.IntegerField(blank = False)
	
	# Attribute types
	ATTRIBUTE_TYPES = (('KB', 'Knowledge Base'), ('PA', 'Problem Analysis'), ('IV','Investigation'), ('DE','Design'), ('ET','Engineering Tools'),
						('IT','Individual and Team Work'), ('CS','Communication Skills'), ('PR','Professionalism'), ('EI','Engineering Impact'),
						('EE','Ethics and Equity'), ('EP','Economics and Project Management'), ('LL','Lifelong Learning'))
	attribute = models.CharField(max_length = 2, choices = ATTRIBUTE_TYPES, blank = False)
	
	# Link this Graduate Attribute measurement to a course_instance
	course = models.ForeignKey(CourseInstance)
	
	def __str__(self):
		return self.name
		

		
