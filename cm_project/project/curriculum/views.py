from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ValidationError
from decimal import *
#
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT, TA_JUSTIFY
#
from curriculum.forms import RegisterForm, UserForm, UserInfoForm, CourseForm, InstanceForm, InstanceDirectForm, ConceptForm, ConceptFormDirect, TextbookForm,StudentGroupForm, DeliverableForm, LearningObjectiveForm, CEABGradForm, MeasurementForm, ConceptRelationForm, ContactHoursCohortForm
from curriculum.models import UserInfo, Department, ProgramStream, Option, Course, CourseInstance, Concept, LearningObjective, Textbook, StudentGroup, Deliverable, CEABGrad, Measurement, ConceptRelation, ContactHours, ContactHoursCohort, YearlyCourseList


def index(request):
	context = RequestContext(request)
	
	context_dict = {'boldmessage': "This is C-Map context"}
	
	return render_to_response('curriculum/index.html', context_dict, context)

def about(request):
	context = RequestContext(request)
	return render_to_response('curriculum/about.html', context)

@login_required	
def profile(request):
	context = RequestContext(request)
	u = User.objects.get(username = request.user)

	try:
		up = UserInfo.objects.get(user=u)
	except UserInfo.DoesNotExist:
		up = u

	context_dict = {'userprofile' : up}
	context_dict['user']=u	
		
	try:
		contact_hours_cohorts = ContactHoursCohort.objects.filter(user=up)
		context_dict['cohorts'] = contact_hours_cohorts
	except ContactHoursCohort.DoesNotExist:
		pass	
		
	except ProgramStream.DoesNotExist:	
		pass
		
	return render_to_response('curriculum/profile.html',context_dict, context)
	
def contact_hours_cohort(request, id_url):
	context = RequestContext(request)
	context_dict = {'id_url' : id_url}
	
	try:
		cohort = ContactHoursCohort.objects.get(id=id_url)
		context_dict['cohort'] = cohort
	except ContactHoursCohort.DoesNotExist:
		pass
		
	return render_to_response('curriculum/contact_hours_cohort.html', context_dict, context)	
		

def register(request):
	context = RequestContext(request)
	
	# Boolean to see if registration was successful
	registered = False
	
	# If HTTP = POST, we are inserting / processing a record
	if request.method == 'POST':
		# Get information from form
		register_form = RegisterForm(data = request.POST)
		profile_form = UserInfoForm(data = request.POST)
		
		# If forms are valid
		if register_form.is_valid(): #and profile_form.is_valid():
			user = register_form.save()
			
			# Hash the users password
			user.set_password(user.password)
			user.save()
			
			# Sort out user profile instance
			# Do not commit since we need to save the user attribute ourselves
			profile = profile_form.save(commit = False)
			#profile = UserInfo()
			profile.user = user
			user = authenticate(username=request.POST['username'], password=request.POST['password'])
			login(request, user)
			# Get the picture if it was included
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
				profile.save()
				# Registration was successful
				registered = True
			else:
				profile.save()
			return HttpResponseRedirect('/curriculum/',context)
		# Something went wrong....dude....shiiiiieetttt
		else:
			print(register_form.errors)
			print(profile_form.errors)

	# Not an HTTP POST
	# Render blank forms
	else:
		register_form = RegisterForm()
		profile_form = UserInfoForm()

	return render_to_response(
                          'curriculum/register_form.html',
                          {'register_form' : register_form, 'profile_form':profile_form, 'registered' : registered},
                          context)


@login_required
def edit_profile(request):
	context=RequestContext(request)
    
	#if the request was a post, do some shieet
	if request.method=='POST':
		#get form info for UserInfor and User
		edit_userInfo_form = UserInfoForm(data = request.POST)
		edit_user_form = UserForm(data = request.POST)
        
		#if the form is valid, save info and redirect
		if edit_userInfo_form.is_valid and edit_user_form.is_valid:
			user = edit_user_form.save()
			userInfo = edit_userInfo_form.save(commit=False)
			userInfo.user = user
			# Get the picture if it was included
			if 'picture' in request.FILES:
				userInfo.picture = request.FILES['picture']
			userInfo.save()
			return HttpResponseRedirect('/curriculum/profile/')
		#else, print errors
		else:
			print(edit_userInfo_form.errors)
			print(edit_user_form.errors)
    
	#otherwise it was a GET, return html template
	else:
		#make the form to be sent in the context_dict be an empty one
		edit_userInfo_form = UserInfoForm()
		edit_user_form = UserForm()
    
	return render_to_response('curriculum/edit_profile_form.html',{'edit_userInfo_form':edit_userInfo_form, 'edit_user_form':edit_user_form},context)

def user_login(request):
	context = RequestContext(request)
	
	# If request is a HTTP Post, get the users login info
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		
		# Attempt to validate and authenticate the user
		user = authenticate(username=username, password=password)
		
		# If user object is not empty then it worked
		if user is not None:
			# Check if the account is active and not disabled
			if user.is_active:
				# Log the user in, if account is valid and active
				login(request, user)
				return HttpResponseRedirect('/curriculum/')
			else:
				# An inactive account was used
				return HttpResponse("Damn Son! Your account strait busted!")
		else:
			# Bad login details were provided
			return render_to_response('curriculum/login.html', {'failure_msg':"Incorrect username/password; please try again..."}, context)
			
	# Must have been a HTTP GET
	# Display empty login form
	else:
		return render_to_response('curriculum/login.html', {}, context)
		
@login_required
def user_logout(request):
	logout(request)
	
	return HttpResponseRedirect('/curriculum/')

def departments(request):
	context = RequestContext(request)
	#query the database to get departments, order by name, put it into a dict for response
	department_list = Department.objects.order_by('name')[:4]
	context_dict = {'departments':department_list}
	
	return render_to_response('curriculum/departments.html',context_dict,context)

def department(request, department_name_url):
	context = RequestContext(request)

	department_name = department_name_url.replace('_',' ')

	context_dict = {'department_name': department_name}

	try:
		department = Department.objects.get(name = department_name)
		program_streams = ProgramStream.objects.filter(department=department)
		context_dict['program_streams'] = program_streams
		context_dict['department'] = department

	except Department.DoesNotExist:
		pass
	return render_to_response('curriculum/department.html',context_dict,context)
	
def program(request, program_name_url):
	context = RequestContext(request)
	
	program_name = program_name_url.replace('_',' ')
	context_dict = {'program_name' : program_name}
	context_dict['program_name_url'] = program_name_url
	
	u = User.objects.get(username = request.user)
	try:
		user_info = UserInfo.objects.get(user=u)
		user_name_url = user_info.get_user_name
		context_dict['user_name_url'] = user_name_url
	except UserInfo.DoesNotExist:
		pass
				
	try:
		program = ProgramStream.objects.get(name = program_name)
		context_dict['program'] = program
		
		department = program.department
		context_dict['department'] = department

		#Get Options associated with this program and pass in context
		options = Option.objects.filter(program_stream = program)
		context_dict['options'] = options

		courses = program.courses.all().order_by('year')
		context_dict['courses']=courses
		# Get first year courses and the urls to their pages
		courses1 = program.courses.filter(year = 'FI')
		context_dict['courses1'] = courses1
		
		# Get second year courses and the urls to their pages
		courses2 = program.courses.filter(year = 'SE')
		context_dict['courses2'] = courses2
		
		# Get third year courses and the urls to their pages
		courses3 = program.courses.filter(year = 'TH')
		context_dict['courses3'] = courses3
		
		# Get fourth year courses and the urls to their pages
		courses4 = program.courses.filter(year = 'FO')
		context_dict['courses4'] = courses4
		
	except ProgramStream.DoesNotExist:
		pass
		
	return render_to_response('curriculum/program.html', context_dict, context)

def all_courses(request):
	context = RequestContext(request)
	
	courses_es = Course.objects.filter(course_code__istartswith='ES')
	context_dict = {'ES' : courses_es}
	
	courses_cbe = Course.objects.filter(course_code__istartswith='CBE')
	context_dict['CBE'] = courses_cbe
	
	courses_cee = Course.objects.filter(course_code__istartswith='CEE')
	context_dict['CEE'] = courses_cee
	
	courses_ece = Course.objects.filter(course_code__istartswith='ECE')
	context_dict['ECE'] = courses_ece
	
	courses_gpe = Course.objects.filter(course_code__istartswith='GPE')
	context_dict['GPE'] = courses_gpe
	
	courses_mme = Course.objects.filter(course_code__istartswith='MME')
	context_dict['MME'] = courses_mme
	
	courses_mse = Course.objects.filter(course_code__istartswith='MSE')
	context_dict['MSE'] = courses_mse
	
	courses_se = Course.objects.filter(course_code__istartswith='SE')
	context_dict['SE'] = courses_se

	courses_rest = Course.objects.exclude(course_code__istartswith='ES').exclude(course_code__istartswith='CBE').exclude(course_code__istartswith='CEE').exclude(course_code__istartswith='ECE').exclude(course_code__istartswith='GPE').exclude(course_code__istartswith='MME').exclude(course_code__istartswith='MSE').exclude(course_code__istartswith='SE')
	context_dict['other'] = courses_rest
	
	return render_to_response('curriculum/all_courses.html', context_dict, context)
	
def all_concepts(request):
	context = RequestContext(request)
	
	concepts_es = Concept.objects.filter(ceab_unit = 'ES', highscool = False)
	concepts_ed = Concept.objects.filter(ceab_unit = 'ED', highscool = False)
	concepts_ma = Concept.objects.filter(ceab_unit = 'MA', highscool = False)
	concepts_sc = Concept.objects.filter(ceab_unit = 'SC', highscool = False)
	concepts_co = Concept.objects.filter(ceab_unit = 'CO', highscool = False)
	concepts_hs = Concept.objects.filter(highscool = True)
	
	context_dict = {'concepts_es' : concepts_es}
	context_dict['concepts_ed'] = concepts_ed 
	context_dict['concepts_ma'] = concepts_ma 
	context_dict['concepts_sc'] = concepts_sc 
	context_dict['concepts_co'] = concepts_co 
	context_dict['concepts_hs'] = concepts_hs 
	
	return render_to_response('curriculum/all_concepts.html', context_dict, context)
	
def option(request, option_name_url):
	context = RequestContext(request)

	option_name = option_name_url.replace('_',' ')
	context_dict={'option_name':option_name}
	context_dict['option_url'] = option_name_url
	try:
		option = Option.objects.get(name = option_name)
		context_dict['option']=option
		courses =option.get_courses()
		context_dict['courses']=courses
		
		year1 = set()
		year2 = set()
		year3 = set()
		year4 = set()
        
		for c in courses:
			if c.year == 'FI':
				year1.add(c)
			elif c.year == 'SE':
				year2.add(c)
			elif c.year == 'TH':
				year3.add(c)
			elif c.year == 'FO' or c.year == 'GR':
				year4.add(c)

		context_dict['year1']=year1
		context_dict['year2']=year2
		context_dict['year3']=year3
		context_dict['year4']=year4
		
		try:
			c_list = YearlyCourseList.objects.get(option=option, year=1)
			course = Course.objects.get(course_code='ES1050')
			c_list.courses.add(course)
		except YearlyCourseList.DoesNotExist:
			pass
		
		try:
			course_lists = YearlyCourseList.objects.filter(option=option)
			for courses in course_lists:
				year_string = courses.year
				year_string = str(year_string)
				year_string = "list"+year_string
				context_dict[year_string] = courses.courses.all()
			
		except YearlyCourseList.DoesNotExist:
			pass

	except Option.DoesNotExist:
		pass
		


	return render_to_response('curriculum/option.html',context_dict,context)

def get_programs(request):
		context = RequestContext(request)
		
		options = Option.objects.all
		context_dict = {'programs' : options}
		
		return render_to_response('curriculum/programs_for_au.html', context_dict, context)
		
# Simple view to display a course	
def course(request, course_name_url):
	context = RequestContext(request)

	# Get the name from the url that was passed with the request
	course_name = course_name_url.replace('_','/')
	context_dict={'course_name':course_name}
	context_dict['course_url'] = course_name_url
	
	course_instances = CourseInstance.objects.filter(course__course_code = course_name)
	context_dict['instances'] = course_instances
	
	try:
		# Get the course object from the database and add it to the context dict
		course = Course.objects.get(course_code = course_name)
		context_dict['course'] = course
		
		get_course_concepts(course_name_url)

    	# Add lists of pre/co/anti requisite courses to the context dict
		pre_courses = course.pre_requisites.all()
		context_dict['pre_requisites']=pre_courses

		co_courses = course.co_requisites.all()
		context_dict['co_requisites']=co_courses

		anti_courses = course.anti_requisites.all()
		context_dict['anti_requisites']=anti_courses
			
		concepts = set()
		for c in course_instances:
			concepts_list = c.concepts.all()
			for p in concepts_list:
				concepts.add(p.name)
			
		concepts_obj = set()
		for c in concepts:
			concept = Concept.objects.get(name=c)
			concepts_obj.add(concept)
			
		context_dict['concepts'] = concepts_obj
		
		concept_list = course.typical_concepts.all()
		context_dict['typical_concept_list'] = concept_list

	except Course.DoesNotExist:
		pass

	return render_to_response('curriculum/course.html', context_dict, context)

# Simple view for displaying a concept
def concept(request, concept_name_url):
	context = RequestContext(request)
	concept_name = concept_name_url.replace('_', ' ')
	
	concept = Concept.objects.get(name=concept_name)
	concept_name = concept.name
	description = concept.description
	ceab_unit = concept.ceab_unit
	highschool = concept.highscool
	#course_instances = CourseInstance.objects.filter(concepts__name = concept_name)
	courses = CourseInstance.objects.filter(concepts__name = concept_name)
	courses2 = Course.objects.filter(typical_concepts__name = concept_name)
	
	context_dict = {'concept_name' : concept_name}
	context_dict['description'] = description
	context_dict['ceab_unit'] = concept.get_ceab_unit_display
	context_dict['highschool'] = highschool
	context_dict['courses'] = courses
	context_dict['concept_url'] = concept_name_url
	context_dict['level'] = concept.height
	
	context_dict['courses2'] = courses2
	
	height = concept.height
	
	while height > 0:
		concepts = concept.related_concepts.all()
		for concept in concepts:
			pass
		height = height-1
    
	
	#concept_name = concept_url.replace('_',' ')
	concept = Concept.objects.get(name=concept_name)
	
	jsonFile = meta_display_concepts_json(concept)
	context_dict['Graph'] =jsonFile
	#height = concept.height
	#html_list = ""
	#my_children = concept.related_concepts.all()
	#context_dict['children'] = my_children
	
	#if(height > 0):
	#	html_list = display_concepts(my_children, height, html_list)
	#	context_dict['concept_html'] = html_list
	
	context_dict['concept_html'] = meta_display_concepts(concept)
	
	
	return render_to_response('curriculum/concept.html', context_dict, context)
	
# passes data to and calls display_concepts function
def meta_display_concepts(concept):
	html_list = ""
	height = concept.height
	my_children = concept.related_concepts.all()
	
	if(height > 0):
		html_list = display_concepts(my_children, height, html_list)
		
	return html_list
	
# Recursive function to get child concepts of a concept
def display_concepts(concept_list, height, html_list):
	html_list = html_list + "<ul>"
	for c in concept_list:
		html_list = html_list + "<li><a href='/curriculum/concepts/"+c.get_url+"/'>" + c.name + "</a></li>"
		one_down = height - 1
		if (one_down >= 0):
			children = c.related_concepts.all()
			html_list = display_concepts(children, one_down, html_list)
	html_list = html_list + "</ul>"

	return html_list
	
# Simple view to display an instance of a course	
def instance(request, course_name_url, instance_date_url):
	context = RequestContext(request)
	
	# Get the date from the url that was passed
	instance_date = instance_date_url.replace('_','-')
	context_dict={'instance_date':instance_date}
	context_dict['course_url'] = course_name_url
	context_dict['date_url'] = instance_date_url
	
	# Get the name from the url that was passed with the request
	course_name = course_name_url.replace('_','/')
    
	try:
		parent_course = Course.objects.get(course_code=course_name)
		context_dict['parent_course']=parent_course
		try:
			instance = CourseInstance.objects.get(course=parent_course,date=instance_date)
			context_dict['instance']=instance

			textbooks = Textbook.objects.filter(instance=instance)
			context_dict['textbooks']=textbooks

			students = StudentGroup.objects.filter(instance=instance)
			context_dict['students']=students

			objectives = LearningObjective.objects.filter(course_instance=instance)
			context_dict['objectives']=objectives
            
			deliverables = Deliverable.objects.filter(course_instance=instance)
			context_dict['deliverables'] =deliverables

			total_deliverables=0
			for deliverable in deliverables:
				total_deliverables+=deliverable.percent
			context_dict['total_deliverables']=total_deliverables

			concepts = instance.concepts.all
			context_dict['concepts']=concepts

			ceab_grads = CEABGrad.objects.filter(course = instance)
			context_dict['ceab_grads'] = ceab_grads
			
			measurements = set()
			for ceab_grad in ceab_grads:
				ceab_measurement=set()

				for student_group in students:
					try:
						#ceab_measurement.add(Measurement.objects.get(ceab_grad=ceab_grad,students=student_group))
						measurement = Measurement.objects.get(ceab_grad=ceab_grad, students=student_group)
						ceab_measurement.add(measurement)
						
					except Measurement.DoesNotExist:
						 pass
						 
				#measurements.add(ceab_measurement)
				name = ceab_grad.get_url+"_measurements"
				context_dict[name]=ceab_measurement
				
			context_dict['measurements'] = measurements

			concept_relations = ConceptRelation.objects.filter(course_instance = instance)
			context_dict['concept_relations'] = concept_relations
        
			try:
				contact_hours = ContactHours.objects.get(instance=instance)
				context_dict['contact_hours'] = contact_hours
			except ContactHours.DoesNotExist:
				pass

		except CourseInstance.DoesNotExist:
			pass
	except Course.DoesNotExist:
		pass		
        
	return render_to_response('curriculum/instance.html', context_dict, context)
	
# view for a ceab graduate attribute	
def ceab_grad(request, course_url, date_url, ceab_url):
	context = RequestContext(request)
	
	course_code = course_url.replace('_', '/')
	date = date_url.replace('_', '-')
	
	context_dict = {'course_code' : course_code}
	context_dict['date'] = date
	context_dict['course_url'] = course_url
	context_dict['date_url'] = date_url
	
	ceab = CEABGrad.objects.get(id=ceab_url)
	context_dict['ceab'] = ceab
	
	measurements = Measurement.objects.filter(ceab_grad=ceab)
	context_dict['measurements'] = measurements

	try:
		course = Course.objects.get(course_code=course_code)
		instance = CourseInstance.objects.get(course=course,date=date)
	except:
		pass

	students = StudentGroup.objects.filter(instance=instance)
	context_dict['students']=students

	total_students=0
	for s in students:
		total_students+=s.size
	context_dict['total_students']=total_students

	num_students = 0
	total_average = 0
	total_1 = 0
	total_2 = 0
	total_3 = 0
	total_4 = 0

	for m in measurements:
		num_students += m.students.size
		total_1 += m.level1
		total_2 += m.level2
		total_3 += m.level3
		total_4 += m.level4
		total_average += m.average

	if measurements.count() > 0:
		total_average = total_average/measurements.count()
	else:
		total_average = 0

	context_dict['num_students'] = num_students
	context_dict['total_average']= total_average
	context_dict['total_1']=total_1
	context_dict['total_2']=total_2
	context_dict['total_3']=total_3
	context_dict['total_4']=total_4
	
	return render_to_response('curriculum/ceab_grad.html', context_dict, context)

# Views for object creation forms
# Add course control - returns form, empty if GET, with data if POST
def add_course(request):
	context = RequestContext(request)
	success = False
    
	if request.method == 'POST':
        
		course_form = CourseForm(data = request.POST)
		
        # If forms are valid
		if course_form.is_valid():
			course = course_form.save()
			success = True
            #return HttpResponse("form complete")
		else:
			print(course_form.errors)

		return render_to_response('curriculum/add_course_form.html',{'course_form' : course_form, 'success':success},context)
	else:
		
		course_form = CourseForm()
        
		return render_to_response('curriculum/add_course_form.html',{'course_form' : course_form},context)

# Add course instance - returns form, empty if GET, with data if POST
def add_instance(request):
	context = RequestContext(request)
	success = False
	if request.method == 'POST':
		instance_form = InstanceForm(data = request.POST)

		if instance_form.is_valid():
			instance = instance_form.save()
			contact_hours = ContactHours(instance=instance)
			contact_hours.save()
			instance.save()
			success = True
			return HttpResponseRedirect('/curriculum/instances/'+instance.course.get_url+'/'+instance.get_date+'/', context)
		else:
			print(instance_form.errors)

		return render_to_response('curriculum/add_instance_form.html',{'instance_form':instance_form},context)
	else:
		instance_form = InstanceForm()

		return render_to_response('curriculum/add_instance_form.html',{'instance_form' : instance_form},context)

# Same as the add_instance function, except it will add it directly to a course
# Add course instance from a course page
def add_instance_direct(request, course_url):
	context = RequestContext(request)
	course_code = course_url.replace('_', '/')
	
	try:
		course = Course.objects.get(course_code=course_code)
	except Course.DoesNotExist:
		pass
		
	context_dict = {'course_url' : course_url}
	
	if request.method == 'POST':
		instance_form = InstanceDirectForm(data = request.POST)
		context_dict['form'] = instance_form
		
		if instance_form.is_valid():
			instance = instance_form.save(commit=False)
			instance.course = course
			instance.save()
			
			return HttpResponseRedirect('/curriculum/instances/'+instance.course.get_url+'/'+instance.get_date+'/', context)
			
		else:
			print(instance_form.errors())
	else:
		instance_form = InstanceDirectForm()
		context_dict['instance_form'] = instance_form
		
		return render_to_response('curriculum/add_instance_direct_form.html', context_dict, context)

# Add Concept - returns form, empty if GET, with data if POST
def add_concept(request):

	context = RequestContext(request)
	success = False
	
	if request.method == 'POST':
		concept_form = ConceptForm(data = request.POST)
        
		if concept_form.is_valid():
			concept = concept_form.save()
			success = True
			concept_url = concept.name
			concept_url = concept_url.replace(' ', '_')
			return HttpResponseRedirect('/curriculum/concepts/'+concept_url+'/', context)
		else:
			print(concept_form.errors)
        
		
		return render_to_response('curriculum/add_concept_form.html',{'concept_form':concept_form} ,context)
	else:
		concept_form = ConceptForm()
        
		return render_to_response('curriculum/add_concept_form.html',{'concept_form' : concept_form},context)
		
# View to get the data for a program, and graduating year	
def add_cohort(request, program_stream_url):
	context = RequestContext(request)
	program_name = program_stream_url.replace('_', ' ')
	context_dict = {'program_name' : program_name}
	context_dict['program_stream_url'] = program_stream_url
	
	if request.method == 'POST':
		cohort_form = ContactHoursCohortForm(data = request.POST)
		context_dict['cohort_form'] = cohort_form
		
		if cohort_form.is_valid():
			contact_hours_cohort = cohort_form.save(commit = False)
			contact_hours_cohort.program = program_name
			program = Option.objects.get(name=program_name)
			program.cohorts = contact_hours_cohort
			#program.save()
			#contact_hours_cohort.save()		
			
			graduating_year = contact_hours_cohort.graduating_year
			return HttpResponseRedirect('/curriculum/AU/'+program_stream_url+'/'+graduating_year+'/', context)
			
			
			#return render_to_response('/curriculum/profile/', context)
			
		else:
			print(cohort_form.errors)
			
		return render_to_response('curriculum/contact_hours_cohort_template.html', context_dict, context)
	
	else:
		cohort_form = ContactHoursCohortForm()
		context_dict['cohort_form'] = cohort_form
				
		return render_to_response('curriculum/contact_hours_cohort_template.html', context_dict, context)
	
# Get the accreditation units for a graduating year	
def get_program_au(request, program_url, year_url):
	context = RequestContext(request)
	
	program = program_url.replace('_', ' ')
	context_dict = {'program' : program}
	context_dict['program_url'] = program_url
	context_dict['year'] = year_url
	
	grad_year = int(year_url)
	fourth = grad_year - 1
	third = fourth - 1
	second = third - 1
	first = second - 1
	
	fourth = str(fourth)
	third = str(third)
	second = str(second)
	first = str(first)
	
	context_dict['fourth'] = fourth
	context_dict['third'] = third
	context_dict['second'] = second
	context_dict['first'] = first
	
	try:
		program_stream = Option.objects.get(name=program)
	except ProgramStream.DoesNotExist:
		pass
	
	total = Decimal(0.0)
	total_first = Decimal(0.0)
	total_second = Decimal(0.0)
	total_third = Decimal(0.0)
	total_fourth = Decimal(0.0)
	
	es_first = Decimal(0.0)
	es_second = Decimal(0.0)
	es_third = Decimal(0.0)
	es_fourth = Decimal(0.0)
	
	ed_first = Decimal(0.0)
	ed_second = Decimal(0.0)
	ed_third = Decimal(0.0)
	ed_fourth = Decimal(0.0)
	
	ma_first = Decimal(0.0)
	ma_second = Decimal(0.0)
	ma_third = Decimal(0.0)
	ma_fourth = Decimal(0.0)
	
	sc_first = Decimal(0.0)
	sc_second = Decimal(0.0)
	sc_third = Decimal(0.0)
	sc_fourth = Decimal(0.0)
	
	co_first = Decimal(0.0)
	co_second = Decimal(0.0)
	co_third = Decimal(0.0)
	co_fourth = Decimal(0.0)
	
	courses_first = YearlyCourseList.objects.get(option=program_stream, year=1).courses.all()
	courses_second = YearlyCourseList.objects.get(option=program_stream, year=2).courses.all()
	courses_third = YearlyCourseList.objects.get(option=program_stream, year=3).courses.all()
	courses_fourth = YearlyCourseList.objects.get(option=program_stream, year=4).courses.all()
	
	
	#courses_first = program_stream.courses.filter(year='FI')
	#courses_second = program_stream.courses.filter(year='SE')
	#courses_third = program_stream.courses.filter(year='TH')
	#courses_fourth = program_stream.courses.filter(year='FO')
	
	for course in courses_first:
		instances = CourseInstance.objects.filter(course=course, date=first)
		for instance in instances:
			contact_hours = ContactHours.objects.get(instance=instance)
			es_first += contact_hours.contact_es
			ed_first += contact_hours.contact_ed
			ma_first += contact_hours.contact_ma
			sc_first += contact_hours.contact_sc
			co_first += contact_hours.contact_co
			
	for course in courses_second:
		instances = CourseInstance.objects.filter(course=course, date=second)
		for instance in instances:
			contact_hours = ContactHours.objects.get(instance=instance)
			es_second += contact_hours.contact_es
			ed_second += contact_hours.contact_ed
			ma_second += contact_hours.contact_ma
			sc_second += contact_hours.contact_sc
			co_second += contact_hours.contact_co
			
	for course in courses_third:
		instances = CourseInstance.objects.filter(course=course, date=third)
		for instance in instances:
			contact_hours = ContactHours.objects.get(instance=instance)
			es_third += contact_hours.contact_es
			ed_third += contact_hours.contact_ed
			ma_third += contact_hours.contact_ma
			sc_third += contact_hours.contact_sc
			co_third += contact_hours.contact_co

	for course in courses_fourth:
		instances = CourseInstance.objects.filter(course=course, date=fourth)
		for instance in instances:
			contact_hours = ContactHours.objects.get(instance=instance)
			es_fourth += contact_hours.contact_es
			ed_fourth += contact_hours.contact_ed
			ma_fourth += contact_hours.contact_ma
			sc_fourth += contact_hours.contact_sc
			co_fourth += contact_hours.contact_co			
	
	total_first = es_first + ed_first + ma_first + sc_first + co_first
	total_second = es_second + ed_second + ma_second + sc_second + co_second
	total_third = es_third + ed_third + ma_third + sc_third + co_third
	total_fourth = es_fourth + ed_fourth + ma_fourth + sc_fourth + co_fourth
	
	es_total = es_first + es_second + es_third + es_fourth
	ed_total = ed_first + ed_second + ed_third + ed_fourth
	ma_total = ma_first + ma_second + ma_third + ma_fourth
	sc_total = sc_first + sc_second + sc_third + sc_fourth
	co_total = co_first + co_second + co_third + co_fourth
	
	context_dict['es_total'] = es_total
	context_dict['ed_total'] = ed_total
	context_dict['ma_total'] = ma_total
	context_dict['sc_total'] = sc_total
	context_dict['co_total'] = co_total
	
	total = total_first + total_second + total_third + total_fourth
	
	context_dict['contact_total'] = total
	
	context_dict['total_first'] = total_first
	context_dict['total_second'] = total_second
	context_dict['total_third'] = total_third
	context_dict['total_fourth'] = total_fourth
	
	context_dict['es_first'] = es_first
	context_dict['ed_first'] = ed_first
	context_dict['ma_first'] = ma_first
	context_dict['sc_first'] = sc_first
	context_dict['co_first'] = co_first
	
	context_dict['es_second'] = es_second
	context_dict['ed_second'] = ed_second
	context_dict['ma_second'] = ma_second
	context_dict['sc_second'] = sc_second
	context_dict['co_second'] = co_second
	
	context_dict['es_third'] = es_third
	context_dict['ed_third'] = ed_third
	context_dict['ma_third'] = ma_third
	context_dict['sc_third'] = sc_third
	context_dict['co_third'] = co_third
	
	context_dict['es_fourth'] = es_fourth
	context_dict['ed_fourth'] = ed_fourth
	context_dict['ma_fourth'] = ma_fourth
	context_dict['sc_fourth'] = sc_fourth
	context_dict['co_fourth'] = co_fourth
	
	return render_to_response('curriculum/contact_hours_cohort.html',context_dict, context)
	
# Allow user to edit the number of lectures taught per course
def edit_concept_relation(request, course_url, date_url, concept_url):
	context = RequestContext(request)
	success = False
	
	course_code = course_url.replace('_', '/')
	date = date_url.replace('_', '-')
	concept_name = concept_url.replace('_', ' ')
	
	try:
		course = Course.objects.get(course_code=course_code)
		try:
			instance = CourseInstance.objects.get(course=course, date=date)
		except CourseInstance.DoesNotExist:
			pass
	except Course.DoesNotExist:
		pass
		
	try:
		concept = Concept.objects.get(name=concept_name)
	except Concept.DoesNotExist:
		pass
	
	relation = ConceptRelation.objects.get(course_instance=instance, concept=concept)
	
	form = ConceptRelationForm(request.POST or None, instance=relation)
	
	context_dict = {'form' : form}
	context_dict['course_url'] = course_url
	context_dict['date_url'] = date_url
	context_dict['concept_url'] = concept_url
	
	if form.is_valid():
		relation = form.save()
		Success = True
		calculate_accreditation_units(course_url, date_url)
		return HttpResponseRedirect('/curriculum/instances/'+course_url+'/'+date_url+'/#au', context_dict, context)
	else:
		print(form.errors)
		
	return render_to_response('curriculum/edit_concept_relation_form.html', context_dict, context)
	
# Let's you create a concept and simultaneously add it to a course instance
# Prety neat		
def add_concept_to_instance(request, course_url, date_url):
	context = RequestContext(request)
	success = False
	
	context_dict = {'course_url' : course_url}
	context_dict['date_url'] = date_url
	
	course_code = course_url.replace('_', '/')
	date = date_url.replace('_', '-')
	height = 0
	
	try:
		course = Course.objects.get(course_code=course_code)
		context_dict['course'] = course		
		
		if course.year == 'FI':
			height = 1
		elif course.year == 'SE':
			height = 2
		elif course.year == 'TH':
			height = 3
		elif course.year == 'FO':
			height = 4
		
		try:
			instance = CourseInstance.objects.get(course=course, date=date)
			context_dict['instance'] = instance		
		except CourseInstance.DoesNotExist:
			pass		
	except Course.DoesNotExist:
			pass
			
	if request.method == 'POST':
		concept_form = ConceptFormDirect(data = request.POST)
		context_dict['concept_form'] = concept_form
		
		if concept_form.is_valid():
			concept = concept_form.save(commit=False)
			concept.height = height
			concept.save()			
						
			#instance.concepts.add(concept)
			membership = ConceptRelation(concept=concept, course_instance=instance, lectures=0)
			#instance.save()
			membership.save()
			success = True 	
			return HttpResponseRedirect('/curriculum/instances/'+course_url+'/'+date_url+'/', context)
		else:
			print(concept_form.errors)
			return render_to_response('curriculum/add_concept_form.html',context_dict,context)
	
	else:
		concept_form = ConceptFormDirect()
		context_dict['concept_form']=concept_form
	
	return render_to_response('curriculum/add_concept_form.html', context_dict, context)

def add_textbook(request, course_url, date_url):
	context = RequestContext(request)
	success=False

	# Add the date and course url to the context_dict, parse them to get the course_code and date
	context_dict = {'course_url':course_url}
	context_dict['date_url']=date_url
	course_code = course_url.replace('_','/')
	date = date_url.replace('_','-')

	try:
		course = Course.objects.get(course_code=course_code)
		context_dict['course']=course
		try:
			instance = CourseInstance.objects.get(course = course, date = date)
			context_dict['instance']=instance
		except CourseInstance.DoesNotExist:
			pass

	except Course.DoesNotExist:
		pass

	if request.method == 'POST':
		textbook_form = TextbookForm(data = request.POST)
		context_dict['textbook_form']=textbook_form
		if textbook_form.is_valid():
			textbook = textbook_form.save(commit=False)
			textbook.instance=instance
			textbook.save()
			success=True
			return HttpResponseRedirect('/curriculum/instances/'+course_url+'/'+date_url+'/',context)
		else:
			print(textbook_form.errors)
			return render_to_response('curriculum/add_deliverable_form.html',context_dict,context)
	else:
		textbook_form = TextbookForm()
		context_dict['textbook_form']=textbook_form
		return render_to_response('curriculum/add_textbook_form.html',context_dict,context)

def add_student_group(request, course_url, date_url):
	context = RequestContext(request)
	success=False
    
	# Add the date and course url to the context_dict, parse them to get the course_code and date
	context_dict = {'course_url':course_url}
	context_dict['date_url']=date_url
	course_code = course_url.replace('_','/')
	date = date_url.replace('_','-')
    
	try:
		course = Course.objects.get(course_code=course_code)
		context_dict['course']=course
		try:
			instance = CourseInstance.objects.get(course = course, date = date)
			context_dict['instance']=instance
		except CourseInstance.DoesNotExist:
			pass
    
	except Course.DoesNotExist:
		pass
    
	if request.method == 'POST':
		student_group_form = StudentGroupForm(data = request.POST)
		context_dict['student_group_form']=student_group_form
		if student_group_form.is_valid():
			student_group = student_group_form.save(commit=False)
			student_group.instance=instance
			student_group.save()
			success=True
			return HttpResponseRedirect('/curriculum/instances/'+course_url+'/'+date_url+'/',context)
		else:
			print(student_group_form.errors)
			return render_to_response('curriculum/add_student_group_form.html',context_dict,context)
	else:
		student_group_form = StudentGroupForm()
		context_dict['student_group_form']=student_group_form
		return render_to_response('curriculum/add_student_group_form.html',context_dict,context)

# This is to aid the functionality of searching for a course
def get_user_list(max_results=0, starts_with=''):
	user_list = []
	
	if starts_with:
		user_list = UserInfo.objects.filter(user__last_name__istartswith=starts_with)
	else:
		user_list = []

	if max_results > 0:
		if len(user_list) > max_results:
			user_list = user_list[:max_results]
			
	return user_list		
		
# Used the get_course_list function to get the top 5 matches
def suggest_user(request):
		context = RequestContext(request)
		user_list = []
		starts_with = ''
		context_dict = {}
		
		if request.method == 'GET':
			starts_with = request.GET['add_professor']
			course = request.GET['arg1']
			date = request.GET['arg2']
			
			type = request.GET['arg3']
			
			if type == "prof":
				context_dict['prof'] = type
			if type == "ass":
				context_dict['ass'] = type
			
			
			context_dict['course'] = course
			context_dict['date'] = date
			
		user_list = get_user_list(5, starts_with)
		
		context_dict['user_list'] = user_list
		
		return render_to_response('curriculum/user_list.html', context_dict, context)		

# Used the get_course_list function to get the top 5 matches
def suggest_user_assistant(request):
		context = RequestContext(request)
		user_list = []
		starts_with = ''
		context_dict = {}
		
		if request.method == 'GET':
			starts_with = request.GET['add_assistant']
			course = request.GET['arg1']
			date = request.GET['arg2']
			
			type = request.GET['arg3']
			
			if type == "prof":
				context_dict['prof'] = type
			if type == "ass":
				context_dict['ass'] = type
			
			
			context_dict['course'] = course
			context_dict['date'] = date
			
		user_list = get_user_list(5, starts_with)
		
		context_dict['user_list'] = user_list
		
		return render_to_response('curriculum/user_list.html', context_dict, context)			
		
# space to implement view to call/pass context to user search/link?
def add_professor(request, course_url, date_url, user_url):
	context = RequestContext(request)
	course_name = course_url.replace('_', '/')
	date = date_url.replace('_', '-')
	user_name = user_url.replace('_', ' ')
	
	try:
		course = Course.objects.get(course_code = course_name)
		
		try:
			instance = CourseInstance.objects.get(course=course, date=date)
			
			try:
				user = UserInfo.objects.get(user__username=user_name)
				
				instance.professors.add(user)
			
			except UserInfo.DoesNotExist:
				pass
			
		except CourseInstance.DoesNotExist:
			pass
		
	except Course.DoesNotExist:
		pass

	return HttpResponseRedirect('/curriculum/instances/'+course_url+'/'+date_url+'/', context)
	
# space to implement view to call/pass context to user search/link?
def add_assistant(request, course_url, date_url, user_url):
	context = RequestContext(request)
	course_name = course_url.replace('_', '/')
	date = date_url.replace('_', '-')
	user_name = user_url.replace('_', ' ')
	
	try:
		course = Course.objects.get(course_code = course_name)
		
		try:
			instance = CourseInstance.objects.get(course=course, date=date)
			
			try:
				user = UserInfo.objects.get(user__username=user_name)
				
				instance.assistants.add(user)
			
			except UserInfo.DoesNotExist:
				pass
			
		except CourseInstance.DoesNotExist:
			pass
		
	except Course.DoesNotExist:
		pass

	return HttpResponseRedirect('/curriculum/instances/'+course_url+'/'+date_url+'/', context)

# Add Deliverable - returns form, empty if GET, with data if POST
def add_deliverable(request, course_url, date_url):
	context = RequestContext(request)
	success = False
    
	context_dict = {'course_url':course_url}
	context_dict['date_url']=date_url
    
	course_code = course_url.replace('_','/')
	date = date_url.replace('_','-')

	try:
		course = Course.objects.get(course_code=course_code)
		context_dict['course']=course
		try:
			instance = CourseInstance.objects.get(course = course, date = date)
			context_dict['instance']=instance
		except CourseInstance.DoesNotExist:
			pass
            
	except Course.DoesNotExist:
		pass

	if request.method == 'POST':
		deliverable_form = DeliverableForm(data = request.POST)
		context_dict['deliverable_form']=deliverable_form

		if deliverable_form.is_valid():
			deliverable = deliverable_form.save(commit=False)
			deliverable.course_instance=instance
			deliverable.save()
			success = True
			return HttpResponseRedirect('/curriculum/instances/'+course_url+'/'+date_url+'/', context)
		else:
			print(deliverable_form.errors)
			return render_to_response('curriculum/add_deliverable_form.html',context_dict,context)


	else:
		deliverable_form = DeliverableForm()
		context_dict['deliverable_form']=deliverable_form

		return render_to_response('curriculum/add_deliverable_form.html',context_dict,context)

# Add learning objective - returns form, empty if GET, with data if POST
def add_learning_objective(request,course_url,date_url):
	context = RequestContext(request)
	success = False

	context_dict = {'course_url':course_url}
	context_dict['date_url']=date_url

	course_code = course_url.replace('_','/')
	date = date_url.replace('_','-')

	try:
		course = Course.objects.get(course_code=course_code)
		context_dict['course']=course
		try:
			instance = CourseInstance.objects.get(course = course, date = date)
			context_dict['instance']=instance
		except CourseInstance.DoesNotExist:
			pass

	except Course.DoesNotExist:
		pass


	if request.method == 'POST':
		learning_objective_form = LearningObjectiveForm(data = request.POST)
		context_dict['learning_objective_form']=learning_objective_form

		if learning_objective_form.is_valid():
			learning_objective = learning_objective_form.save(commit=False)
			learning_objective.course_instance = instance
			learning_objective.save()
			success = True
			return HttpResponseRedirect('/curriculum/instances/'+course_url+'/'+date_url+'/', context)
		else:
			print(learning_objective_form.errors)
    
		return render_to_response('curriculum/add_objective_form.html',context_dict,context)

	else:
		learning_objective_form = LearningObjectiveForm()
		context_dict['learning_objective_form']=learning_objective_form

		return render_to_response('curriculum/add_objective_form.html',context_dict,context)

# Add CEABgrad - returns form, empty if GET, with data if POST
def add_ceab_grad(request,course_url,date_url):
	context = RequestContext(request)
	success = False

	context_dict = {'course_url':course_url}
	context_dict['date_url']=date_url

	course_code = course_url.replace('_','/')
	date = date_url.replace('_','-')

	try:
		course = Course.objects.get(course_code=course_code)
		context_dict['course']=course
		try:
			instance = CourseInstance.objects.get(course = course, date = date)
			context_dict['instance']=instance
		except CourseInstance.DoesNotExist:
			pass

	except Course.DoesNotExist:
		pass

	if request.method == 'POST':
		ceab_grad_form = CEABGradForm(data = request.POST)
		context_dict['ceab_grad_form']=ceab_grad_form

		if ceab_grad_form.is_valid():
			ceab_grad = ceab_grad_form.save(commit=False)
			ceab_grad.course = instance
			# Get the picture if it was included
			if 'measurement_file' in request.FILES:
				ceab_grad.measurement_file = request.FILES['measurement_file']
			if 'rubrik' in request.FILES:
				ceab_grad.rubrik = request.FILES['rubrik']
			ceab_grad.save()
			success = True
			return HttpResponseRedirect('/curriculum/instances/'+course_url+'/'+date_url+'/', context)
		else:
			print(ceab_grad_form.errors)
        
			return render_to_response('curriculum/add_ceab_grad_form.html',context_dict,context)
    
	else:
		ceab_grad_form = CEABGradForm()
		context_dict['ceab_grad_form']=ceab_grad_form

		return render_to_response('curriculum/add_ceab_grad_form.html',context_dict,context)

def add_measurement(request, course_url, date_url, ceab_url):
	context = RequestContext(request)
	success=False
    
	# Add the date and course url to the context_dict, parse them to get the course_code and date
	context_dict = {'course_url':course_url}
	context_dict['date_url']=date_url
	context_dict['ceab_url']=ceab_url
	course_code = course_url.replace('_','/')
	date = date_url.replace('_','-')
	ceab = ceab_url.replace('_',' ')

	try:
		course = Course.objects.get(course_code=course_code)
		context_dict['course']=course
		try:
			instance = CourseInstance.objects.get(course = course, date = date)
			context_dict['instance']=instance
			try:
				ceab_grad = CEABGrad.objects.get(course=instance, id=ceab)
				context_dict['ceab_grad']=ceab_grad
			except CEABGrad.DoesNotExist:
				pass
		except CourseInstance.DoesNotExist:
			pass
	except Course.DoesNotExist:
		pass
    
	if request.method == 'POST':
		measurement_form = MeasurementForm(instance, data = request.POST)
		context_dict['measurement_form']=measurement_form
		if measurement_form.is_valid():
			measurement = measurement_form.save(commit=False)
			measurement.course=instance
			measurement.ceab_grad = ceab_grad
			measurement.save()
			success=True
			return HttpResponseRedirect('/curriculum/ceab_grad/'+course_url+'/'+date_url+'/'+str(ceab_grad.id),context)
		else:
			print(measurement_form.errors)
			return render_to_response('curriculum/add_measurement_form.html',context_dict,context)
	else:
		measurement_form = MeasurementForm(instance)
		context_dict['measurement_form']=measurement_form
		return render_to_response('curriculum/add_measurement_form.html',context_dict,context)

# This is to aid the functionality of searching for a course
def get_course_list(max_results=0, starts_with=''):
	course_list = []
	
	if starts_with:
		course_list = Course.objects.filter(course_code__istartswith=starts_with)
	else:
		course_list = []

	if max_results > 0:
		if len(course_list) > max_results:
			course_list = course_list[:max_results]
			
	return course_list
	
# Used the get_course_list function to get the top 5 matches
def suggest_course(request):
		context = RequestContext(request)
		course_list = []
		starts_with = ''
		
		if request.method == 'GET':
			starts_with = request.GET['course_suggestion']
			
		course_list = get_course_list(50, starts_with)
		
		return render_to_response('curriculum/search_list.html', {'course_list' : course_list}, context)
		
# Used the get_course_list function to get the top 5 matches
def suggest_course_add_one(request):
		context = RequestContext(request)
		course_list = []
		starts_with = ''
		
		if request.method == 'GET':
			starts_with = request.GET['add_courses_1']
			option_url = request.GET['arg1']
			year = request.GET['arg2']
			year_str = str(year)
			
		
		course_list = get_course_list(50, starts_with)
		context_dict = {'course_list' : course_list}
		context_dict['option_url'] = option_url
		context_dict['year'] = year_str
		
		return render_to_response('curriculum/search_list_add.html', context_dict, context)
		
# Used the get_course_list function to get the top 5 matches
def suggest_course_add_two(request):
		context = RequestContext(request)
		course_list = []
		starts_with = ''
		
		if request.method == 'GET':
			starts_with = request.GET['add_courses_2']
			option_url = request.GET['arg1']
			year = request.GET['arg2']
			year_str = str(year)
			
		
		course_list = get_course_list(50, starts_with)
		context_dict = {'course_list' : course_list}
		context_dict['option_url'] = option_url
		context_dict['year'] = year_str
		
		return render_to_response('curriculum/search_list_add.html', context_dict, context)
		
# Used the get_course_list function to get the top 5 matches
def suggest_course_add_three(request):
		context = RequestContext(request)
		course_list = []
		starts_with = ''
		
		if request.method == 'GET':
			starts_with = request.GET['add_courses_3']
			option_url = request.GET['arg1']
			year = request.GET['arg2']
			year_str = str(year)
			
		
		course_list = get_course_list(50, starts_with)
		context_dict = {'course_list' : course_list}
		context_dict['option_url'] = option_url
		context_dict['year'] = year_str
		
		return render_to_response('curriculum/search_list_add.html', context_dict, context)
		
# Used the get_course_list function to get the top 5 matches
def suggest_course_add_four(request):
		context = RequestContext(request)
		course_list = []
		starts_with = ''
		
		if request.method == 'GET':
			starts_with = request.GET['add_courses_4']
			option_url = request.GET['arg1']
			year = request.GET['arg2']
			year_str = str(year)
			
		
		course_list = get_course_list(50, starts_with)
		context_dict = {'course_list' : course_list}
		context_dict['option_url'] = option_url
		context_dict['year'] = year_str
		
		
		return render_to_response('curriculum/search_list_add.html', context_dict, context)
		
# Used the get_course_list function to get the top 5 matches
def suggest_pre_requisite(request):
		context = RequestContext(request)
		course_list = []
		starts_with = ''
		
		if request.method == 'GET':
			starts_with = request.GET['add_pre']
			course_url = request.GET['arg1']
			requisite = request.GET['arg2']
			
			course_code = course_url.replace('_', '/')
			course = Course.objects.get(course_code=course_code)
		
		course_list = get_course_list(50, starts_with)
		
		anti_list = course.anti_requisites.all()
		co_list = course.co_requisites.all()
		
		if anti_list:
			new_list = [course for course in course_list if course not in anti_list]
			course_list = new_list
			
		if co_list:	
			new_list = [course for course in course_list if course not in co_list]
			course_list = new_list
		
		context_dict = {'course_list' : course_list}
		context_dict['course_url'] = course_url
		context_dict['requisite'] = requisite
		
		
		return render_to_response('curriculum/search_list_add_requisite.html', context_dict, context)

def add_pre_requisite(request, course_url, requisite_url):
	context = RequestContext(request)
	course_code = course_url.replace('_', '/')
	requisite_code = requisite_url.replace('_', '/')
	
	try:
		course = Course.objects.get(course_code=course_code)
		
		try:
			requisite = Course.objects.get(course_code=requisite_code)
			course.pre_requisites.add(requisite)
			
		except Course.DoesNotExist:
			pass
	except Course.DoesNotExist:
		pass
		
	return HttpResponseRedirect('/curriculum/courses/'+course_url+'/', context)
	
# Used the get_course_list function to get the top 5 matches
def suggest_co_requisite(request):
		context = RequestContext(request)
		course_list = []
		starts_with = ''
		
		if request.method == 'GET':
			starts_with = request.GET['add_co']
			course_url = request.GET['arg1']
			requisite = request.GET['arg2']
			
			course_code = course_url.replace('_', '/')
			course = Course.objects.get(course_code=course_code)
		
		course_list = get_course_list(50, starts_with)
		
		anti_list = course.anti_requisites.all()
		pre_list = course.pre_requisites.all()
		
		
		if anti_list:
			new_list = [course for course in course_list if course not in anti_list]
			course_list = new_list
		
		if pre_list:	
			new_list = [course for course in course_list if course not in pre_list]
			course_list = new_list
		
		context_dict = {'course_list' : course_list}
		context_dict['course_url'] = course_url
		context_dict['requisite'] = requisite
		
		
		return render_to_response('curriculum/search_list_add_requisite.html', context_dict, context)
		
def add_co_requisite(request, course_url, requisite_url):
	context = RequestContext(request)
	course_code = course_url.replace('_', '/')
	requisite_code = requisite_url.replace('_', '/')
	
	try:
		course = Course.objects.get(course_code=course_code)
		
		try:
			requisite = Course.objects.get(course_code=requisite_code)
			course.co_requisites.add(requisite)
			
		except Course.DoesNotExist:
			pass
	except Course.DoesNotExist:
		pass
		
	return HttpResponseRedirect('/curriculum/courses/'+course_url+'/', context)		

# Used the get_course_list function to get the top 5 matches
def suggest_anti_requisite(request):
		context = RequestContext(request)
		course_list = []
		starts_with = ''
		
		if request.method == 'GET':
			starts_with = request.GET['add_anti']
			course_url = request.GET['arg1']
			requisite = request.GET['arg2']
			
			course_code = course_url.replace('_', '/')
			course = Course.objects.get(course_code=course_code)
		
		course_list = get_course_list(50, starts_with)
		
		co_list = course.co_requisites.all()
		pre_list = course.pre_requisites.all()
		
		if co_list:
			new_list = [course for course in course_list if course not in co_list]
			course_list = new_list
			
		if pre_list:	
			new_list = [course for course in course_list if course not in pre_list]
			course_list = new_list
		
		context_dict = {'course_list' : course_list}
		context_dict['course_url'] = course_url
		context_dict['requisite'] = requisite
		
		
		return render_to_response('curriculum/search_list_add_requisite.html', context_dict, context)
		
def add_anti_requisite(request, course_url, requisite_url):
	context = RequestContext(request)
	course_code = course_url.replace('_', '/')
	requisite_code = requisite_url.replace('_', '/')
	
	try:
		course = Course.objects.get(course_code=course_code)
		
		try:
			requisite = Course.objects.get(course_code=requisite_code)
			course.anti_requisites.add(requisite)
			
		except Course.DoesNotExist:
			pass
	except Course.DoesNotExist:
		pass
		
	return HttpResponseRedirect('/curriculum/courses/'+course_url+'/', context)	
		
def add_course_to_course_list(request, option_url, year_url, course_url):
	context = RequestContext(request)
	option_name = option_url.replace('_', ' ')
	year = int(year_url)
	course_code = course_url.replace('_', '/')
	
	try:
		option = Option.objects.get(name=option_name)
		
		try:
			course = Course.objects.get(course_code=course_code)
		except Course.DoesNotExist:
			pass	
	except Option.DoesNotExist:
		pass
			
	try:
		course_list = YearlyCourseList.objects.get(option=option, year=year)
		course_list.courses.add(course)
	except YearlyCourseList.DoesNotExist:
		pass
	
	return HttpResponseRedirect('/curriculum/options/'+option_url+'/', context)
	
# Used by the get_concept_list function to get the query results
def get_concept_list(max_results=0, starts_with=''):
	concept_list = []
	
	if starts_with:
		concept_list = Concept.objects.filter(name__istartswith=starts_with)
	else:
		concept_list = []
	
	if max_results > 0:
		if len(concept_list) > max_results:
			concept_list = concept_list[:max_results]
			
	return concept_list
	
# Used to get the top 5 results of the concept search
def suggest_concept(request):
	context = RequestContext(request)
	concept_list = []
	starts_with = ''
	
	if request.method == 'GET':
		starts_with = request.GET['concept_suggestion']
		
	concept_list = get_concept_list(5, starts_with)
	
	return render_to_response('curriculum/search_list.html', {'concept_list' : concept_list}, context)
	
# Get concept search results and send them to the template	
def suggest_concept_add(request):
	context = RequestContext(request)
	concept_list = []
	starts_with = ''
	
	if request.method == 'GET':
		starts_with = request.GET['link_concept']
		course_url = request.GET['arg1']
		date_url = request.GET['arg2']
		
	concept_list = get_concept_list(10, starts_with)
	context_dict = {'concept_list' : concept_list}
	context_dict['course_url'] = course_url
	context_dict['date_url'] = date_url
	
	return render_to_response('curriculum/concept_search_list.html', context_dict, context)
	
# implements the search functionality for adding concepts to a course instance	
def add_concept_search(request, course_url, date_url):
		context = RequestContext(request)

		context_dict = {'course_url' : course_url}
		context_dict['date_url'] = date_url
		
		course_code = course_url.replace('_', '/')
		date = date_url.replace('_', '-')
		
		context_dict['course_code'] = course_code
		context_dict['course_date'] = date
		
		try:
			course = Course.objects.get(course_code=course_code)
			try:
				instance = CourseInstance.objects.get(course=course, date=date)
				context_dict['instance'] = instance		
			except CourseInstance.DoesNotExist:
				pass		
		except Course.DoesNotExist:
			pass
			
		concepts = instance.concepts.all()
		context_dict['concepts'] = concepts
		
		return render_to_response('curriculum/add_concept_search.html', context_dict, context)
	
# Allows user to select an existing concept and add it to a course	
def link_concept(request, course_url, date_url, name_url):
		context = RequestContext(request)
		
		name = name_url.replace('_',' ')
		date = date_url.replace('_','-')
		course_code = course_url.replace('_','/')
		
		context_dict = {'name' : name}
		context_dict['date'] = date
		context_dict['course_code'] = course_code
		
		try:
			course = Course.objects.get(course_code=course_code)
			try:
				instance = CourseInstance.objects.get(course=course, date=date)
			except CourseInstance.DoesNotExist:
				pass
		except Course.DoesNotExist:
			pass
			
		try:
			concept = Concept.objects.get(name=name)
		except Concept.DoesNotExist:
			pass
			
		#instance.concepts.add(concept)
		membership = ConceptRelation(concept=concept, course_instance = instance, lectures=0.0)
		membership.save()
		
		return HttpResponseRedirect('/curriculum/add_concept_search/'+course_url+'/'+date_url+'/', context)
		
# implements the search functionality for adding concepts to a course instance	
def add_child_concept_search(request, concept_url):
		context = RequestContext(request)

		context_dict = {'concept_url' : concept_url}
		
		concept_name = concept_url.replace('_', ' ')
		
		context_dict['concept_name'] = concept_name
	
		try:
			concept = Concept.objects.get(name=concept_name)
			context_dict['concepts_html'] = meta_display_concepts(concept)
		except Concept.DoesNotExist:
			pass
				
		return render_to_response('curriculum/add_concept_to_concept_search.html', context_dict, context)		
		
# Used by the get_concept_list function to get the query results
def get_child_concept_list(max_results=0, starts_with='', parent_concept=''):
	concept_list = []
	
	parent = Concept.objects.get(name=parent_concept)
	height = parent.height
	height = height-1
	
	if starts_with:
		concept_list = Concept.objects.filter(name__istartswith=starts_with, height=height)
	else:
		concept_list = []
	
	if max_results > 0:
		if len(concept_list) > max_results:
			concept_list = concept_list[:max_results]
			
	return concept_list		
		
# Get concept search results and send them to the template	
def suggest_child_concept_add(request):
	context = RequestContext(request)
	concept_list = []
	starts_with = ''
	context_dict = {}
	
	if request.method == 'GET':
		starts_with = request.GET['link_child']
		parent_url = request.GET['arg1']
		context_dict['starts_with'] = starts_with
	
	parent_name = parent_url.replace('_', ' ')
	
	concept_list = get_child_concept_list(10, starts_with, parent_name)
	context_dict['concept_list'] = concept_list
	context_dict['parent_url'] = parent_url
	
	return render_to_response('curriculum/add_concept_to_concept_search_list.html', context_dict, context)		
		
def add_child_concept(request, concept_url, child_url):
	context = RequestContext(request)
	name_parent = concept_url.replace('_', ' ')
	name_child = child_url.replace('_', ' ')
	
	try:
		concept_child = Concept.objects.get(name=name_child)
		try:
			concept_parent = Concept.objects.get(name=name_parent)
			concept_parent.related_concepts.add(concept_child)
		except Concept.DoesNotExist:
			pass
	except Concept.DoesNotExist:
		pass

	
	return HttpResponseRedirect('/curriculum/add_child_concept_search/'+concept_url+'/', context)
	
# Calculate the % of each accreditation unit based on the number of lectures for each course
def calculate_accreditation_units(course_url, date_url):
	
	course_code = course_url.replace('_','/')
	date = date_url.replace('_','-')
	
	try:
		course = Course.objects.get(course_code=course_code)
		try:
			instance = CourseInstance.objects.get(course=course, date=date)
			try:
				relations = ConceptRelation.objects.filter(course_instance=instance)
			except ConceptRelation.DoesNotExist:
				pass
		except CourseInstance.DoesNotExist:
			pass
	except Course.DoesNotExist:
		pass

	total_lectures = 0.0
	unit_ma = 0.0
	unit_sc = 0.0
	unit_es = 0.0
	unit_ed = 0.0
	unit_co = 0.0
	
    # if there are any 'relations' i.e. concept-course relations, loop through them and track their hours
	if relations:
		for relation in relations:
			total_lectures += relation.lectures
			unit = relation.concept.ceab_unit
			
			if unit == 'MA':
				unit_ma += relation.lectures
			elif unit == 'SC':
				unit_sc += relation.lectures
			elif unit == 'ES':
				unit_es += relation.lectures
			elif unit == 'ED':
				unit_ed += relation.lectures
			elif unit == 'CO':
				unit_co += relation.lectures

	# calculate unit percentages
		unit_ma = (unit_ma/total_lectures)*100
		unit_sc = (unit_sc/total_lectures)*100
		unit_es = (unit_es/total_lectures)*100
		unit_ed = (unit_ed/total_lectures)*100
		unit_co = (unit_co/total_lectures)*100

	# set new unit percentages in instance, save
		instance.acc_math = unit_ma
		instance.acc_science = unit_sc
		instance.acc_eng_science = unit_es
		instance.acc_eng_design = unit_ed
		instance.acc_comp = unit_co
	
		instance.save()
	
	# Get contact hours object associated with instance, set new values, save.
		contact_hours = ContactHours.objects.get_or_create(instance=instance)[0]
		contact_hours.contact_es = unit_es
		contact_hours.contact_ed = unit_ed
		contact_hours.contact_ma = unit_ma
		contact_hours.contact_sc = unit_sc
		contact_hours.contact_co = unit_co
	
		contact_hours.save()

	# Redirect back to original instance page
#return HttpResponseRedirect('/curriculum/instances/'+course_url+'/'+date_url+'/', context)
	
def download_syllabus(request, course_url, date_url):
	# replace characters in url's
	course_code = course_url.replace('_','/')
	date = date_url
    
	# Obtain the course object to find the instance
	try:
		course = Course.objects.get(course_code=course_code)
		# Obtain the instance object to be used for syllabus generation
		try:
			instance = CourseInstance.objects.get(course=course,date=date)
			professors = instance.professors.all()
			assistants = instance.professors.all()
			textbooks = Textbook.objects.filter(instance=instance)
			concepts = instance.concepts.all()
			objectives = LearningObjective.objects.filter(course_instance=instance)
			deliverables = Deliverable.objects.filter(course_instance=instance)
			pre_reqs = instance.course.pre_requisites.all()
            
            # Create dynamic file name based on instane; create content disposition with filename for response
			file_name = course_url + "-" + date + "-syllabus"
			content_disposition = "attachment; filename='"+file_name+"'"
			# Create the HttpResponse object with the appropriate PDF headers.
			response = HttpResponse(content_type='application/pdf')
			response['Content-Disposition'] = content_disposition
            
			buffer = BytesIO()
            
			doc = SimpleDocTemplate(buffer, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72, pagesize=letter)
			elements=[]
                                    
			styles=getSampleStyleSheet()
			styles.add(ParagraphStyle(name='big_centerAlign',fontName='Helvetica',alignment=TA_CENTER,fontSize=16, spaceBefore=5, leading=20))
			styles.add(ParagraphStyle(name='small_centerAlign',fontName='Helvetica',alignment=TA_CENTER,fontSize=12, spaceBefore=5, leading=15))

			styles.add(ParagraphStyle(name='title_leftAlign',fontName='Helvetica',alignment=TA_LEFT,fontSize=14, spaceAfter=10, spaceBefore=10))
			styles.add(ParagraphStyle(name='body_leftAlign',fontName='Times-Roman',alignment=TA_LEFT, firstLineIndent=25, spaceAfter=5))
			styles.add(ParagraphStyle(name='body_justifyAlign',fontName='Times-Roman',alignment=TA_JUSTIFY, firstLineIndent=25, spaceAfter=5))

			# Print out the header information; course code and name, date of the isntance
			elements.append(Paragraph("<i>Western University ~ Faculty of Engineering</i>",styles['small_centerAlign']))
			elements.append(Paragraph(instance.course.course_code + " - " + instance.course.name,styles['big_centerAlign']))
			elements.append(Paragraph("Course Outline - "+str(instance.date)+"/"+str(int(instance.date)+1),styles['big_centerAlign']))

			# Print out the description if it exists
			elements.append(Paragraph("<b>Course Description:</b>",styles['title_leftAlign']))
			if course.description:
				elements.append(Paragraph(course.description,styles['body_justifyAlign']))
			else:
				elements.append(Paragraph("There was no description listed under this course object...",styles['body_leftAlign']))

			# If any pre-reqs were found under this course, print them
			elements.append(Paragraph("<b>Pre-Requisites:</b>",styles['title_leftAlign']))
			if pre_reqs:
				for idx,val in enumerate(pre_reqs):
					elements.append(Paragraph(str(idx+1)+". "+val.course_code+" - "+val.name,styles['body_leftAlign']))
				elements.append(Paragraph("<b>Please Note: </b>Unless you have either the prerequisites for this course or written special permission from your Dean to enroll in it, you will be removed from this course and it will be deleted from your record. This decision may not be appealed. You will receive no adjustment to your fees in the event that you are dropped from a course for failing to have the necessary prerequisites.",styles['body_justifyAlign']))
			else:
				elements.append(Paragraph("There were no pre-requisites listed under this course object...",styles['body_leftAlign']))

			# Display accreditation units
			elements.append(Paragraph("<b>Accreditation Units:</b>",styles['title_leftAlign']))
			if instance.acc_math != 0:
				elements.append(Paragraph("Math = "+str(instance.acc_math)+"%",styles['body_leftAlign']))
			if instance.acc_science != 0:
				elements.append(Paragraph("Science = "+str(instance.acc_science)+"%",styles['body_leftAlign']))
			if instance.acc_eng_science != 0:
				elements.append(Paragraph("Engineering Science = "+str(instance.acc_eng_science)+"%",styles['body_leftAlign']))
			if instance.acc_eng_design != 0:
				elements.append(Paragraph("Engineering Design = "+str(instance.acc_eng_design)+"%",styles['body_leftAlign']))
			if instance.acc_comp != 0:
				elements.append(Paragraph("Complementory = "+str(instance.acc_comp)+"%",styles['body_leftAlign']))

			# display detailed professor information
			elements.append(Paragraph("<b>Professors:</b>",styles['title_leftAlign']))
			if professors:
				for prof in professors:
					elements.append(Paragraph("<b>"+prof.user.first_name+" "+prof.user.last_name+"</b>",styles['body_leftAlign']))
					elements.append(Paragraph("Email: "+prof.user.email,styles['body_leftAlign']))
					elements.append(Paragraph("Office: "+prof.office,styles['body_leftAlign']))
			else:
				elements.append(Paragraph("There were no professors listed under this course instance...",styles['body_leftAlign']))

			# Print plain T.A. info (if they exist)
			elements.append(Paragraph("<b>Assistants:</b>",styles['title_leftAlign']))
			if assistants:
				for idx, val in enumerate(assistants):
					elements.append(Paragraph(str(idx+1)+". "+val.user.first_name+" "+val.user.last_name+" ("+val.user.email+")",styles['body_leftAlign']))
			else:
				elements.append(Paragraph("There were no assistants listed under this course instance...",styles['body_leftAlign']))

			# Print out contact hour info
			elements.append(Paragraph("<b>Contact Hours:</b>",styles['title_leftAlign']))
			elements.append(Paragraph("Lecture hours: "+str(instance.course.lecture_hours)+" - Lab hours: "+str(instance.course.lab_hours)+" - Tutorial hours: "+str(instance.course.tut_hours)+" - Credit: "+str(instance.course.credit), styles['body_leftAlign']))


			# Print out textbooks
			elements.append(Paragraph("<b>Textbooks:</b>",styles['title_leftAlign']))
			if textbooks:
				for textbook in textbooks:
					if textbook.required:
						elements.append(Paragraph(textbook.name+" (required)", styles['body_leftAlign']))
					else:
						elements.append(Paragraph(textbook.name,styles['body_leftAlign']))
			else:
				elements.append(Paragraph("There were no textbooks listed under this course instance...", styles['body_leftAlign']))

			# concepts
			elements.append(Paragraph("<b>Topics Covered:</b>",styles['title_leftAlign']))
			if concepts:
				for idx, val in enumerate(concepts):
					elements.append(Paragraph("<b>"+str(idx+1)+".</b> "+val.name,styles['body_leftAlign']))
			else:
				elements.append(Paragraph("There were no concepts listed under this course instance...",styles['body_leftAlign']))

			# Learning objectives
			elements.append(Paragraph("<b>Learning Objectives:</b>",styles['title_leftAlign']))
			if objectives:
				for idx, val in enumerate(objectives):
					elements.append(Paragraph("<b>"+str(idx+1)+".</b> "+val.description,styles['body_leftAlign']))
			else:
				elements.append(Paragraph("There were no learning objectives listed under this course instance...",styles['body_leftAlign']))

			elements.append(Paragraph("<b>CEAB Graduate Attributes:</b>",styles['title_leftAlign']))
			ceab_data = [['Knowledge Base',' ','Individual Work',' ','Ethics and Equity',' '],
                         ['Problem Analysis',' ','Team Work',' ','Economics and Project Management',' '],
                         ['Investigation',' ','Communication',' ','Life-long Learning',' '],
                         ['Design',' ','Professionalism',' ', ' ',' '],
                         ['Engineering Tools',' ','Impact on Soceity',' ',' ',' '],
                         ]
			ceab_table = Table(ceab_data)
			ceab_table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
			elements.append(ceab_table)

			# Deliverables
			elements.append(Paragraph("<b>Deliverables: </b>",styles['title_leftAlign']))
			if deliverables:
				table_data = [['Type', '%', 'Tentative Due Date'],]
				for idx, val in enumerate(deliverables):
					data=[val.get_type_display(),str(val.percent),val.due_date]
					table_data.append(data)
				t=Table(table_data)
				elements.append(t)
			else:
				elements.append(Paragraph("There were no deliverables listed under this course...",styles['body_leftAlign']))

			# Display and append random disclaimers
			elements.append(Paragraph("<b>English: </b>",styles['title_leftAlign']))
			elements.append(Paragraph("In accordance with Senate and Faculty Policy, students may be penalized up to 10% of the marks on all assignments, tests and examinations for the improper use of English. Additionally, poorly written work with the exception of final examinations may be returned without grading. If resubmission of the work is permitted, it may be graded with marks deducted for poor English and/or late submission.",styles['body_justifyAlign']))
			elements.append(Paragraph("<b>Attendance: </b>",styles['title_leftAlign']))
			elements.append(Paragraph("Any student who, in the opinion of the instructor, is absent too frequently from class or laboratory periods in any course, will be reported to the Dean (after due warning has been given). On the recommendation of the Department concerned, and with the permission of the Dean, the student will be debarred from taking the regular examination in the course.",styles['body_justifyAlign']))
			elements.append(Paragraph("<b>SSD: </b>",styles['title_leftAlign']))
			elements.append(Paragraph("<i>Please contact the course instructor if you require material in an alternate format or if any other arrangements can make this course more accessible to you. You may also wish to contact Services for Students with Disabilities (SSD) at 661-2111 x 82147 for any specific question regarding an accommodation.</i>",styles['body_justifyAlign']))
			elements.append(Paragraph("<b>Cheating: </b>",styles['title_leftAlign']))
			elements.append(Paragraph("University policy states that cheating, including plagiarism, is a scholastic offense. The commission of a scholastic offence is attended by academic penalties which might include expulsion from the program. If you are caught cheating, there will be no second warning.",styles['body_justifyAlign']))
			elements.append(Paragraph("<b>Note: </b>",styles['title_leftAlign']))
			elements.append(Paragraph("The above topics and outline are subject to adjustments and changes as needed. Students who have failed an Engineering course (ie.<50%) must repeat all components of the course. No special permissions will be granted enabling a student to retain laboratory, assignment or test marks from previous years. Previously completed assignments and laboratories cannot be resubmitted for grading by the student in subsequent years.",styles['body_justifyAlign']))


			doc.build(elements)

			# Get the value of the BytesIO buffer and write it to the response.
			pdf = buffer.getvalue()
			buffer.close()
			response.write(pdf)
			return response
        
		except CourseInstance.DoesNotExist:
			return HttpResponseRedirect()
    
	except Course.DoesNotExist:
		return HttpResponseRedirect()


def create_accreditation_report(request, option_url, date_url):
	context=RequestContext(request)
	option_name = option_url.replace('_',' ')
	try:
		option = Option.objects.get(name = option_name)
        
		try:
            # Get the yearly course lists associated with the appropriate option; get the number of years
			yearly_course_lists = YearlyCourseList.objects.filter(option=option)
			num_of_years = len(yearly_course_lists)
            
            
            # Loop through courses_lists;  get instances for appropriate year and add to master list
			all_course_instances=set()
            
			for course_list in yearly_course_lists:
				for course in course_list.courses.all():
					cohort_date = int(date_url)-num_of_years+(course_list.year - 1)
					try:
						all_course_instances.add(CourseInstance.objects.get(course=course, date=cohort_date))
					except:
						pass
            
			# categorize master list into math, science, eng_science, eng_design, and comp lists
            # loop through master, add to appropriate list if acc_percent is >0)
			math_instances = set()
			science_instances = set()
			eng_sc_ed_instances = set()
			comp_instances = set()
			empty_instances = set()
            
			for instance in all_course_instances:
				try:
					aunits = ContactHours.objects.get(instance=instance)
					if aunits.contact_ma > 0:
						math_instances.add(instance)
					if aunits.contact_sc > 0:
						science_instances.add(instance)
					if aunits.contact_es > 0 or aunits.contact_ed > 0:
						eng_sc_ed_instances.add(instance)
					if aunits.contact_co > 0:
						comp_instances.add(instance)
					if (aunits.contact_ma == 0) and (aunits.contact_sc == 0) and (aunits.contact_es == 0) and (aunits.contact_ed == 0) and (aunits.contact_co == 0):
						empty_instances.add(instance)
				except:
					empty_instances.add(instance)
            
    		# Create a dynamic file name, content disposition based on that name, and prepare the response object (for serving a pdf)
			file_name = option_url + "-Class_of_" + str(date_url) + "-au_report"
			content_disposition = "attachment; filename='"+file_name+"'"
			# Create the HttpResponse object with the appropriate PDF headers.
			response = HttpResponse(content_type='application/pdf')
			response['Content-Disposition'] = content_disposition
            
			# create a buffer to write to, and initialize a reportlab doc template to receive the buffer
			buffer = BytesIO()
			doc = SimpleDocTemplate(buffer, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72, pagesize=letter)
			elements=[]
            
			# Setup styles to be used throughout document creation
			styles=getSampleStyleSheet()
			styles.add(ParagraphStyle(name='big_centerAlign',fontName='Helvetica',alignment=TA_CENTER,fontSize=16, spaceBefore=5, leading=20))
			styles.add(ParagraphStyle(name='small_centerAlign',fontName='Helvetica',alignment=TA_CENTER,fontSize=12, spaceBefore=5, leading=15))
			styleN = styles['BodyText']
			styles.add(ParagraphStyle(name='title_leftAlign',fontName='Helvetica',alignment=TA_LEFT,fontSize=14, spaceAfter=10, spaceBefore=10))
			styles.add(ParagraphStyle(name='body_leftAlign',fontName='Times-Roman',alignment=TA_LEFT, firstLineIndent=25, spaceAfter=5))
			styles.add(ParagraphStyle(name='body_justifyAlign',fontName='Times-Roman',alignment=TA_JUSTIFY, firstLineIndent=25, spaceAfter=5))
            
			# HEADER/TITLE
			elements.append(Paragraph("<i>Western University ~ Faculty of Engineering</i>",styles['small_centerAlign']))
			elements.append(Paragraph("Accreditation Report on the "+option_name, styles['big_centerAlign']))
			elements.append(Paragraph("For the graduating class of "+date_url, styles['big_centerAlign']))
            
            # MATHEMATICS
			elements.append(Paragraph("Mathematics",styles['title_leftAlign']))
			math_data = [['Course Number','Course Title','Math AU','Course Contact','Relevant Content'],]
            
			total_math = 0
			for instance in math_instances:
				au = ContactHours.objects.get(instance=instance)
				instance_name = Paragraph(instance.course.name,styleN)
				if len(instance.professors.all())==0:
					data = [instance.course.course_code,instance_name,au.contact_ma,'n/a', '-']
				else:
					data =[instance.course.course_code,instance_name,au.contact_ma,instance.professors.all(), '-']
				total_math += au.contact_ma
				math_data.append(data)
            
			total_math_au = ['Total:','',total_math,'','']
			math_data.append(total_math_au)
			math_table = Table(math_data,colWidths=[3.0*cm,7.0*cm,2.5*cm,3.0*cm,4.0*cm])
			math_table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),('BOX', (0, 0), (-1, -1), 0.25, colors.black),('BACKGROUND',(0,0),(5,0),colors.grey)]))
			elements.append(math_table)
            
			# SCIENCES
			elements.append(Paragraph("Natural Sciences",styles['title_leftAlign']))
			science_data = [['Course Number','Course Title','Science AU','Course Contact','Relevant Content'],]
            
			total_science = 0
			for instance in science_instances:
				au = ContactHours.objects.get(instance=instance)
				instance_name = Paragraph(instance.course.name,styleN)
				if len(instance.professors.all())==0:
					data = [instance.course.course_code,instance_name,au.contact_sc,'n/a', '-']
				else:
					instance_professors = Paragraph(instance.professors.all()[0], styleN)
					data =[instance.course.course_code,instance_name,au.contact_sc,instance_professors, '-']
				total_science += au.contact_sc
				science_data.append(data)
            
			total_science_au = ['Total:','',total_science,'','']
			science_data.append(total_science_au)
			science_table = Table(science_data, colWidths=[3.0*cm,7.0*cm,2.5*cm,3.0*cm,4.0*cm])
			science_table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),('BOX', (0, 0), (-1, -1), 0.25, colors.black),('BACKGROUND',(0,0),(5,0),colors.grey)]))
			elements.append(science_table)
            
			# ENGINEERING SCIENCE AND DESIGN
			contact_para = Paragraph("Course Contact",styleN)
			content_para = Paragraph("Relevant Content",styleN)
			elements.append(Paragraph("Engineering Science and Design",styles['title_leftAlign']))
			eng_sc_ed_data = [['Course Number','Course Title','ES','ED','ES + ED',contact_para,content_para],]
            
			total_es = 0
			total_ed = 0
			for instance in eng_sc_ed_instances:
				au = ContactHours.objects.get(instance=instance)
				instance_name = Paragraph(instance.course.name,styleN)
				if len(instance.professors.all())==0:
					data = [instance.course.course_code,instance_name,au.contact_es, au.contact_ed, (au.contact_es + au.contact_ed),'n/a', '-']
				else:
					data =[instance.course.course_code,instance_name,au.contact_ma,instance.professors.all(), '-']
				total_es += au.contact_es
				total_ed += au.contact_ed
				eng_sc_ed_data.append(data)
            
			total_eng_au = ['Total:','',total_es,total_ed,(total_es+total_ed),'','']
			eng_sc_ed_data.append(total_eng_au)
			eng_table = Table(eng_sc_ed_data, colWidths=[3.0*cm,7.0*cm,1.5*cm,1.5*cm,2.0*cm,2.25*cm,2.25*cm])
			eng_table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),('BOX', (0, 0), (-1, -1), 0.25, colors.black),('BACKGROUND',(0,0),(6,0),colors.grey)]))
			elements.append(eng_table)
            
			# COMP STUDIES
			elements.append(Paragraph("Complementary Studies",styles['title_leftAlign']))
			comp_data = [['Course Number','Course Title','CS AU','Course Contact','Relevant Content'],]
            
			total_comp = 0
			for instance in comp_instances:
				au = ContactHours.objects.get(instance=instance)
				instance_name = Paragraph(instance.course.name,styleN)
				if len(instance.professors.all())==0:
					data = [instance.course.course_code,instance_name,au.contact_co,'n/a', '-']
				else:
					data =[instance.course.course_code,instance_name,au.contact_co,instance.professors.all(), '-']
				total_comp += au.contact_co
				comp_data.append(data)
            
			comp_total = ['Total:','',total_comp,'','']
			comp_data.append(comp_total)
			comp_table = Table(comp_data,colWidths=[3.0*cm,7.0*cm,2.5*cm,3.0*cm,4.0*cm])
			comp_table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),('BOX', (0, 0), (-1, -1), 0.25, colors.black),('BACKGROUND',(0,0),(5,0),colors.grey)]))
			elements.append(comp_table)
            
			# EMPTY
			elements.append(Paragraph("Empty Instances",styles['title_leftAlign']))
			elements.append(Paragraph("The following instances have no accreditation units available for analysis. Please make sure the instance is properly constructed/updated with all the appropriate information...",styles['body_leftAlign']))
			for instance in empty_instances:
				elements.append(Paragraph("<b>"+instance.course.course_code+" - "+instance.date+"</b>",styles['body_leftAlign']))
            
            
			doc.build(elements)
			# Get the value of the BytesIO buffer and write it to the response.
			pdf = buffer.getvalue()
			buffer.close()
			response.write(pdf)
			return response
		except YearlyCourseList.DoesNotExist:
			return HttpResponseRedirect()
    
	except Option.DoesNotExist:
		return HttpResponseRedirect()

	
def calculate_pre_requisite(request, course_url):
	context = RequestContext(request)
	context_dict = { 'course_url' : course_url }
	course_code = course_url.replace('_', '/')
	
	try:
		course = Course.objects.get(course_code=course_code)
		context_dict['course'] = course
		get_course_concepts(course_url)
		
		concepts_high = course.typical_concepts.all()
		
		concepts_children = set()
		
		for concept in concepts_high:
			concept_down = concept.related_concepts.all()
			for c in concept_down:
				concepts_children.add(c)
				
		size_high = 0
		
		for i in concepts_children:
			size_high = size_high + 1
				
		# Concepts children is the set of this courses lower level concepts
		
		all_courses = Course.objects.all()
		
		list_matches = []
		
		for course in all_courses:
			get_course_concepts(course.get_url)
		
		for course in all_courses:
			concepts_low = course.typical_concepts.all()
			difference = [concept for concept in concepts_low if concept in concepts_children]
			difference = set(difference)
			
			size_difference = 0
			
			for i in difference:
				size_difference = size_difference + 1
				
			percent_match = 0
			
			if not size_high == 0:
				if not size_difference == 0:
					percent_match = (size_difference / size_high) * 100

			if percent_match > 0:
				if not course.get_url == course_url:
					list_matches.append((course.get_url, course.course_code, percent_match, difference, course))
				
		if list_matches:
			context_dict['list_matches'] = list_matches 
		
	except Course.DoesNotExist:
		pass
	
	
	return render_to_response('curriculum/calculate_pre_requisite.html', context_dict, context)
	
def get_course_concepts(course_url):
	course_code = course_url.replace('_', '/')
	
	try:
		course = Course.objects.get(course_code=course_code)
		instances = CourseInstance.objects.filter(course=course)
		
		for instance in instances:
			concepts = instance.concepts.all()
			for concept in concepts:
				course.typical_concepts.add(concept)
		
	except Course.DoesNotExist:
		pass

# MAP VISUALIZATIONS
def concept_map(request):
	context = RequestContext(request)
	
	return render_to_response('curriculum/concept_map.html', context)

def concept_map(request, concept_url):
	context = RequestContext(request)
	
    
	
	concept_name = concept_url.replace('_',' ')
	concept = Concept.objects.get(name=concept_name)
	
	jsonFile = meta_display_concepts_json(concept)
	
	
	context_dict = {'Graph' : jsonFile}
	
	return render_to_response('curriculum/concept_map.html',context_dict, context)

# passes data to and calls display_concepts function
def meta_display_concepts_json(concept):
	html_list = ""
	height = concept.height
	my_children = concept.related_concepts.all()
	html_list = html_list + '{"id": "'+concept.name+'","name": "' + concept.name + '","data":[],"children":['
    
	if(height > 0):
		html_list = display_concepts_json(my_children, height, html_list)
    
    
	html_list = html_list + '],}'
	return html_list

# Recursive function to get child concepts of a concept
def display_concepts_json(concept_list, height, html_list):
	for c in concept_list:
		html_list = html_list + '{"id": "'+c.name+'","name": "' + c.name + '","data":[],"children":['
		one_down = height - 1
		if (one_down >= 0):
			children = c.related_concepts.all()
			html_list = display_concepts_json(children, one_down, html_list)
		html_list = html_list + ']},'
    
    
	return html_list

def course_map(request, program_stream_url):
	context = RequestContext(request)
    
	jsonFile ='['
	
	program_stream = program_stream_url.replace('_',' ')
	program = ProgramStream.objects.get(name=program_stream)
	
	for course in program.courses.all():
		jsonFile += '{"adjacencies": [';
		for pre in course.pre_requisites.all():
			jsonFile+= '{"nodeTo": "'+str(pre.course_code)+'","nodeFrom": "'+str(course.course_code)+'","data": {"$color": "#557EAA" } }, '
		jsonFile += '],"data": { "$color": "#83548B", "$type": "circle", "$dim": 10}, "id": "' +str(course.course_code)+'", "name": "'+str(course.course_code)+'"},'
	
	jsonFile += ']'
	context_dict = {'Graph' : jsonFile}
	
	return render_to_response('curriculum/course_map.html',context_dict,context)
	
def delete_course_from_list(request, option_url, course_url, year_url):
	context = RequestContext(request)
	option_name = option_url.replace('_', ' ')
	course_code = course_url.replace('_', '/')
	
	year = int(year_url)
	
	try:
		option = Option.objects.get(name = option_name)
		
		try:
			course = Course.objects.get(course_code = course_code)
			
			try:
				course_list = YearlyCourseList.objects.get(option=option, year=year)
				course_list.courses.remove(course)
				
			except YearlyCourseList.DoesNotExist:
				pass
			
		except Course.DoesNotExist:
			pass
		
	except Option.DoesNotExist:
		pass
	
	return HttpResponseRedirect('/curriculum/options/'+option_url+'/', context)
	
def delete_requisite_from_list(request, course_url, requisite_url, type_url):
	context = RequestContext(request)
	course_code = course_url.replace('_', '/')
	requisite_code = requisite_url.replace('_', '/')
	
	type = str(type_url)
	
	course = Course.objects.get(course_code=course_code)
	requisite = Course.objects.get(course_code=requisite_code)
	
	if type == "pre":
		course.pre_requisites.remove(requisite)
	elif type == "co":
		course.co_requisites.remove(requisite)
	elif type == "anti":
		course.anti_requisites.remove(requisite)

	return HttpResponseRedirect('/curriculum/courses/'+course_url+'/', context)

def delete_students(request, course_url, date_url, students_id):
	context = RequestContext(request)
	course_code = course_url.replace('_','/')
    
	try:
		students = StudentGroup.objects.get(pk=students_id)
		students.delete()
		return HttpResponseRedirect("/curriculum/instances/"+course_url+"/"+date_url+"/", context)
	except:
		return HttpResponseRedirect("/curriculum/instances/"+course_url+"/"+date_url+"/", context)

def delete_textbook(request, course_url, date_url, book_id):
	context = RequestContext(request)
	course_code = course_url.replace('_','/')

	try:
		text = Textbook.objects.get(pk=book_id)
		text.delete()
		return HttpResponseRedirect("/curriculum/instances/"+course_url+"/"+date_url+"/", context)
	except:
		return HttpResponseRedirect("/curriculum/instances/"+course_url+"/"+date_url+"/", context)
	
def delete_deliverable(request, course_url, date_url, deliverable_id):
	context = RequestContext(request)
	course_code = course_url.replace('_','/')
    
	try:
		deliverable = Deliverable.objects.get(pk=deliverable_id)
		deliverable.delete()
		return HttpResponseRedirect("/curriculum/instances/"+course_url+"/"+date_url+"/", context)
	except:
		return HttpResponseRedirect("/curriculum/instances/"+course_url+"/"+date_url+"/", context)

def delete_objective(request, course_url, date_url, objective_id):
	context = RequestContext(request)
	course_code = course_url.replace('_','/')
    
	try:
		objective = LearningObjective.objects.get(pk=objective_id)
		objective.delete()
		return HttpResponseRedirect("/curriculum/instances/"+course_url+"/"+date_url+"/", context)
	except:
		return HttpResponseRedirect("/curriculum/instances/"+course_url+"/"+date_url+"/", context)

def delete_ceab_grad(request, course_url, date_url, ceab_id):
	context = RequestContext(request)
	course_code = course_url.replace('_','/')
    
	try:
		ceab_grad = CEABGrad.objects.get(pk=ceab_id)
		ceab_grad.delete()
		return HttpResponseRedirect("/curriculum/instances/"+course_url+"/"+date_url+"/", context)
	except:
		return HttpResponseRedirect("/curriculum/instances/"+course_url+"/"+date_url+"/", context)
		
	
	
	
	
	
	



