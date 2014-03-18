from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime, time
from django.core.exceptions import ValidationError
from django.db import models
# User model
class UserInfo(models.Model):
	# One to one field implies inheritance from User class
	user = models.OneToOneField(User)

	website = models.URLField(blank = True)
	picture = models.ImageField(upload_to = 'profile_images', blank = True)
	office = models.CharField(max_length="30",blank=True)
	is_peng = models.BooleanField(default=False)
	
	# Define different user types
	USER_TYPES = (('PR','Professor'), ('TA', 'Teaching Assistant'), ('GN','General'), ('SP', 'Special'))
	type = models.CharField(max_length = 2, choices = USER_TYPES, default = 'GN')
	
	@property
	def get_user_name(self):
		user_name_url = self.user.username
		user_name_url = user_name_url.replace(' ', '_')
		return user_name_url		
		
	@property 
	def get_full_name(self):
		return self.user.last_name+', '+self.user.first_name
	
	def __str__(self):
		return self.user.username
		
# Track information for a particular program stream, over a certain period of time
class ContactHoursCohort(models.Model):
	user = models.ForeignKey(UserInfo)
	
	date_start = models.DateField(blank=True)
	date_end = models.DateField(blank=True)
	graduating_year = models.CharField(max_length = 4, blank=False)
	public = models.BooleanField(default = False, blank = True)
	program = models.CharField(max_length = 400, blank=True)
	
	@property
	def get_date_start(self):
		DATE_FORMAT = "%Y-%m-%d" 
		date_url = self.date_start
		d = date_url.strftime(DATE_FORMAT)
		d = d.replace('-', '_')
		return d
		
	@property	
	def get_date_end(self):
		DATE_FORMAT = "%Y-%m-%d" 
		date_url = self.date_end
		d = date_url.strftime(DATE_FORMAT)
		d = d.replace('-', '_')
		return d	
	
	def __str__(self):
		return self.user.user.username

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
	height = models.PositiveIntegerField(blank = True, default=0)
	
	# Options for CEAB accreditation units
	ACCREDITATION_TYPES = (('MA', 'Math'), ('SC', 'Science'), ('ES', 'Engineering Science'),
							('ED', 'Engineering Design'), ('CO', 'Complementary Studies'))
	ceab_unit = models.CharField(max_length = 2, choices = ACCREDITATION_TYPES, blank = False)
	
	# Relate concepts to to themselves
	related_concepts = models.ManyToManyField('self',blank = True, symmetrical = False)
	
	@property
	def get_url(self):
		concept_url = self.name.replace(' ', '_')
		return concept_url
		
	def __str__(self):
		return self.name
		
# Course model
class Course(models.Model):
	course_code = models.CharField(max_length = 12, unique = True)
	name = models.CharField(max_length = 128)
    
	lecture_hours = models.FloatField(default=0.0, blank = False)
	lab_hours = models.FloatField(default=0.0, blank = False)
	tut_hours = models.FloatField(default = 0.0, blank = False)
	credit = models.FloatField(blank = False)
    
	description = models.CharField(max_length = 500, blank = True)
	website = models.URLField(blank = True)
	
	typical_concepts = models.ManyToManyField(Concept, blank = True)
    
	
	# Define options for class year
	YEAR_TYPES = (('FI','First'), ('SE', 'Second'), ('TH','Third'), ('FO', 'Fourth'), ('GR', 'Graduate'))
	year = models.CharField(max_length = 2, choices = YEAR_TYPES, blank = False)
	
	# Create a recursive relationship with other course 
	# objects to link a course to its requisite courses
	# *** REMEMBER TO MAKE THESE MUTUALLY EXCLUSIVE ***
	pre_requisites = models.ManyToManyField('self', symmetrical = False, related_name='pre', blank = True)
	anti_requisites = models.ManyToManyField('self', symmetrical = False, related_name='anti', blank = True)
	co_requisites = models.ManyToManyField('self', symmetrical = False, related_name='co', blank = True)
	
	
	
	# Definte a function to get half the combined lab and tutorial hours + lecture hours, all times weeks per semester. Multiply that by credit value
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
	course = models.ForeignKey(Course, related_name='instance_set')
	date = models.CharField(blank = False, max_length = 4)
	#textbook = models.CharField(max_length = 128, blank = True)

	# Professors and T.A.'s require m2m relations so that multiple teachers can teacher multiple courses
	professors = models.ManyToManyField(UserInfo, related_name = 'teaches',blank=True)
	assistants = models.ManyToManyField(UserInfo, related_name = 'assists', blank = True)
    
	# Hold the percent values for accreditation categories (calculated automatically?)
	acc_math = models.PositiveIntegerField(blank = True, default=0)
	acc_science = models.PositiveIntegerField(blank = True, default=0)
	acc_eng_science = models.PositiveIntegerField(blank = True, default=0)
	acc_eng_design = models.PositiveIntegerField(blank = True, default=0)
	acc_comp = models.PositiveIntegerField(blank = True, default=0)
	
	# Define options for semester course is taught in
	SEMESTER_TYPES = (('F', 'First'), ('S', 'Second'), ('Y', 'Year'))
	semester = models.CharField(max_length = 1, choices = SEMESTER_TYPES, blank = False)
	
	# Define concepts covered in this course
	concepts = models.ManyToManyField(Concept, through = 'ConceptRelation', blank = True)
	
	@property
	def get_date(self):
		return self.date
	
	@property
	def get_professors(self):
		return self.professors.all()

	@property
	def get_assistants(self):
		return self.assistants.all()

	@property
	def get_concepts(self):
		return self.concepts.all()

	def clean(self):
		# If the total of the CEAB units are not 100 (or 0 i.e. left blank), raise a validation error
		if (self.acc_math + self.acc_science + self.acc_eng_science + self.acc_eng_design + self.acc_comp) == 100 or (self.acc_math + self.acc_science + self.acc_eng_science + self.acc_eng_design + self.acc_comp) == 0:
			pass
		else:
			raise ValidationError('Total of CEAB unit percentages must equal 100, or be left blank for future calculation.')


	def __str__(self):
		return "Instance of "+self.course.course_code+" ("+self.get_date+")"
		
class ConceptRelation(models.Model):
	concept = models.ForeignKey(Concept)
	course_instance = models.ForeignKey(CourseInstance)
	lectures = models.FloatField(blank = True,default=0.0)
	
	def __str__(self):
		return "Relationship between "+self.concept.name+" concept, and course "+self.course_instance

	def save(self, *args, **kwargs):
		super(ConceptRelation, self).save(*args, **kwargs)
		
# Simple textbook model to accomodate having multiple textbooks/keeping a record
class Textbook(models.Model):
	name = models.CharField(unique=False,max_length=75,blank=False)
	required=models.BooleanField(default=False, blank=False)
	isbn = models.CharField(max_length=25,blank=True)

	instance = models.ForeignKey(CourseInstance)

	def __str__(self):
		return self.name

# Group of students; each instance will containt multiple groups of students which constitue the class (i.e. 10 software 3 computer and 5 electrical make a class of 18.)
class StudentGroup(models.Model):
	instance = models.ForeignKey(CourseInstance)
	size = models.PositiveIntegerField(blank=False)

	STUDENT_TYPES = (('che', 'Chemical'),('civ', 'Civil'), ('com', 'Computer'), ('ele', 'Electrical'), ('gre', 'Green Process'),('int','Integrated'),('mec','Mechanical'),('mse','Mechatronic'),('sof','Software'),('gen','General (1st year)'))
	type = models.CharField(max_length = 3  , choices = STUDENT_TYPES)

	def __str__(self):
		return self.get_type_display() +" students for " + str(self.instance)

# Model for a course deliverable (Assignment, Quiz, Test, etc...)
class Deliverable(models.Model):
	DELIVERABLE_TYPES = (('A', 'Assignment'),('Q', 'Quiz'), ('T', 'Test'), ('M', 'Midterm'), ('F', 'Final Exam'))
	type = models.CharField(max_length = 1, choices = DELIVERABLE_TYPES)
	percent = models.PositiveIntegerField(blank = False)
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
	
	# Link this program stream to a cohort, 1 to many 
	cohorts = models.ForeignKey(ContactHoursCohort, blank = True, null = True)
	
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
	num_years = models.IntegerField(blank=True)
	
	@property
	def get_url(self):
		return self.name.replace(' ','_')

	#use this function to get the courses from the program_stream, add the added_courses, remove the removed_courses, and return the resultant list
	#@property
	def get_courses(self):
		courses = set()
		try:
			for c in self.program_stream.courses.all():
				courses.add(c)

			added = set()
			for c in self.added_courses.all():
				added.add(c)
			courses = courses.union(added)

			removed = set()
			for c in self.removed_courses.all():
				removed.add(c)
			courses = courses.difference(removed)

			return courses
		except:
			return courses



	def __str__(self):
		return self.name

# List of courses a 'program stream' will take in a given year
# Several of these objects will be used to define a 'course progression'
class YearlyCourseList(models.Model):
	option = models.ForeignKey(Option)
	year = models.IntegerField(blank = True, default = 0)
	courses = models.ManyToManyField(Course, blank=True)
	
	def __str__(self):
		return self.option+'/'+self.year		
		
def auto_create_course_lists(instance, *args, **kwargs):
	for i in range(instance.num_years):
		YearlyCourseList.objects.create(option=instance, year=i+1)
	#option.save()
models.signals.post_save.connect(auto_create_course_lists, sender=Option, dispatch_uid='auto_create_course_lists')
# CEAB Accreditation Units
#
class ContactHours(models.Model):
	instance = models.ForeignKey(CourseInstance)
	
	contact_es = models.DecimalField(blank = True, default = 0.0,editable=False, decimal_places=1, max_digits=8)
	contact_ed = models.DecimalField(blank = True, default = 0.0,editable=False, decimal_places=1, max_digits=8)
	contact_ma = models.DecimalField(blank = True, default = 0.0,editable=False, decimal_places=1, max_digits=8)
	contact_sc = models.DecimalField(blank = True, default = 0.0,editable=False, decimal_places=1, max_digits=8)
	contact_co = models.DecimalField(blank = True, default = 0.0,editable=False, decimal_places=1, max_digits=8)
	
	def save(self, *args, **kwargs):
		contact_coefficient = self.instance.course.get_contact_value
		self.contact_es = (self.instance.acc_eng_science)/100 * contact_coefficient
		self.contact_ed = (self.instance.acc_eng_design)/100 * contact_coefficient
		self.contact_ma = (self.instance.acc_math)/100 * contact_coefficient
		self.contact_sc = (self.instance.acc_science)/100 * contact_coefficient
		self.contact_co = (self.instance.acc_comp)/100 * contact_coefficient
		super(ContactHours, self).save(*args, **kwargs)
	
	def __str__(self):
		return self.instance.course.name+" contact hours"
		
# CEAB Graduate Attributes
class CEABGrad(models.Model):
	name = models.CharField(max_length = 128, unique = True)
	date = models.DateField(blank = False)
	measurement_text = models.TextField(max_length = 500, blank = True)
	measurement_file = models.FileField(upload_to = 'ceab_files', blank = True)
	rubrik = models.FileField(upload_to = 'rubrik_files', blank = True)
	
	# Attribute types
	ATTRIBUTE_TYPES = (('KB', 'Knowledge Base'), ('PA', 'Problem Analysis'), ('IV','Investigation'), ('DE','Design'), ('ET','Engineering Tools'),
						('IT','Individual and Team Work'), ('CS','Communication Skills'), ('PR','Professionalism'), ('EI','Engineering Impact'),
						('EE','Ethics and Equity'), ('EP','Economics and Project Management'), ('LL','Lifelong Learning'))
	attribute = models.CharField(max_length = 2, choices = ATTRIBUTE_TYPES, blank = False)
	
	# Link this Graduate Attribute measurement to a course_instance
	course = models.ForeignKey(CourseInstance)
	
	student_groups = models.ManyToManyField(StudentGroup, through = 'Measurement', blank = True)

	@property
	def get_url(self):
		return self.name.replace(' ','_')
		
	@property
	def get_id(self):
		return self.id

	def __str__(self):
		return self.name

# Measurement class foreign key's to a ceab grad attribute, and a group of students. It tracks the scores for a student group
class Measurement(models.Model):
	ceab_grad = models.ForeignKey(CEABGrad)
	students = models.ForeignKey(StudentGroup)
	
	level1 = models.PositiveIntegerField(default = 0)
	level2 = models.PositiveIntegerField(default = 0)
	level3 = models.PositiveIntegerField(default = 0)
	level4 = models.PositiveIntegerField(default = 0)

	average = models.FloatField(blank = True, editable=False)

    # method to check if total = total defined be the chosen student group, throw's error if not
	def clean(self):
		if (self.level1 + self.level2 + self.level3 + self.level4) != self.students.size:
			err_msg = "The number of scorse must equal "+str(self.students.size)
			raise ValidationError(err_msg)

	# overwrite save to auto-calculate the average field
	def save(self, *args, **kwargs):
		total = (self.level1 + self.level2 + self.level3 + self.level4)
		if total != 0:
			self.average = ((self.level1*1 + self.level2*2 + self.level3*3 + self.level4*4))/total
		else:
			self.average = 0.0
		super(Measurement, self).save(*args, **kwargs)

	def __str__(self):
		return "Measurement of " + self.ceab_grad.name +" for "+self.students.get_type_display() +" students"

