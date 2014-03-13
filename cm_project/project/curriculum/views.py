from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
#
from curriculum.forms import RegisterForm, UserForm, UserInfoForm, CourseForm, InstanceForm, ConceptForm, TextbookForm,StudentGroupForm, DeliverableForm, LearningObjectiveForm, CEABGradForm, MeasurementForm, ConceptRelationForm, ContactHoursCohortForm
from curriculum.models import UserInfo, Department, ProgramStream, Option, Course, CourseInstance, Concept, LearningObjective, Textbook, StudentGroup, Deliverable, CEABGrad, Measurement, ConceptRelation, ContactHours, ContactHoursCohort


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
		user_info = UserInfo.objects.get(user = u)
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

def option(request, option_name_url):
	context = RequestContext(request)

	option_name = option_name_url.replace('_',' ')
	context_dict={'option_name':option_name}
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

	except Option.DoesNotExist:
		pass

	return render_to_response('curriculum/option.html',context_dict,context)

# Simple view to display a course	
def course(request, course_name_url):
	context = RequestContext(request)

	# Get the name from the url that was passed with the request
	course_name = course_name_url.replace('_','/')
	context_dict={'course_name':course_name}
	
	course_instances = CourseInstance.objects.filter(course__course_code = course_name)
	context_dict['instances'] = course_instances
	
	try:
		# Get the course object from the database and add it to the context dict
		course = Course.objects.get(course_code = course_name)
		context_dict['course'] = course

    	# Add lists of pre/co/anti requisite courses to the context dict
		pre_courses = course.pre_requisites.all()
		context_dict['pre_requisites']=pre_courses

		co_courses = course.co_requisites.all()
		context_dict['co_requisites']=co_courses

		anti_courses = course.anti_requisites.all()
		context_dict['anti_requisites']=anti_courses
		
		concepts = set()
		for c in course_instances:
			concepts.add(c.concepts.all())
			
		context_dict['concepts'] = concepts

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
	
	
	context_dict = {'concept_name' : concept_name}
	context_dict['description'] = description
	context_dict['ceab_unit'] = ceab_unit
	context_dict['highschool'] = highschool
	context_dict['courses'] = courses
	
	return render_to_response('curriculum/concept.html', context_dict, context)
	
# Simple view to display an instance of a course	
def instance(request, course_name_url, instance_date_url):
	context = RequestContext(request)
	
	# Get the date from the url that was passed
	instance_date = instance_date_url.replace('_','-')
	context_dict={'instance_date':instance_date}
	
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

			concepts = instance.concepts.all
			context_dict['concepts']=concepts

			ceab_grads = CEABGrad.objects.filter(course = instance)
			context_dict['ceab_grads'] = ceab_grads

			measurements = set()
			for ceab_grad in ceab_grads:
				ceab_measurement=set()
				for student_group in students:
					try:
						ceab_measurement.add(Measurement.objects.get(ceab_grad=ceab_grad,students=student_group))
					except Measurement.DoesNotExist:
						 pass
				name = ceab_grad.get_url+"_measurements"
				context_dict[name]=ceab_measurement

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
		
		
def add_cohort(request, program_stream_url, user_name_url):
	context = RequestContext(request)
	context_dict = {'user_name_url' : user_name_url}
	context_dict['program_stream_url'] = program_stream_url
	program_name = program_stream_url.replace('_', ' ')
	user_name = user_name_url.replace('_', ' ')
	
	context_dict['program_name'] = program_name
	
	
	if request.method == 'POST':
		cohort_form = ContactHoursCohortForm(data = request.POST)
		context_dict['cohort_form'] = cohort_form
		
		if cohort_form.is_valid():
			contact_hours_cohort = cohort_form.save(commit = False)
			contact_hours_cohort.program = program_name
			program = ProgramStream.objects.get(name=program_name)
			user = UserInfo.objects.get(user__username = user_name)
			contact_hours_cohort.user = user
			program.cohorts = contact_hours_cohort
			program.save()
			contact_hours_cohort.save()		
			
			#return render_to_response('/curriculum/profile/', context)
			
		else:
			print(cohort_form.errors)
			
		return render_to_response('curriculum/contact_hours_cohort_template.html', context_dict, context)
	
	else:
		cohort_form = ContactHoursCohortForm()
		context_dict['cohort_form'] = cohort_form
				
		return render_to_response('curriculum/contact_hours_cohort_template.html', context_dict, context)
	
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
		
		return HttpResponseRedirect('/curriculum/instances/'+course_url+'/'+date_url+'/', context_dict, context)
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
	
	try:
		course = Course.objects.get(course_code=course_code)
		context_dict['course'] = course		
		try:
			instance = CourseInstance.objects.get(course=course, date=date)
			context_dict['instance'] = instance		
		except CourseInstance.DoesNotExist:
			pass		
	except Course.DoesNotExist:
			pass
			
	if request.method == 'POST':
		concept_form = ConceptForm(data = request.POST)
		context_dict['concept_form'] = concept_form
		
		if concept_form.is_valid():
			concept = concept_form.save()
						
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
		concept_form = ConceptForm()
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

# space to implement view to call/pass context to user search/link?
def add_professor(request, course_url, date_url):
    return
def add_assistant(request, course_url, date_url):
    return

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
				ceab_grad = CEABGrad.objects.get(course=instance, name=ceab)
				context_dict['ceab_grad']=ceab_grad
			except CEABGrad.DoesNotExist:
				pass
		except CourseInstance.DoesNotExist:
			pass
	except Course.DoesNotExist:
		pass
    
	if request.method == 'POST':
		measurement_form = MeasurementForm(ceab_grad, data = request.POST)
		context_dict['measurement_form']=measurement_form
		if measurement_form.is_valid():
			measurement = measurement_form.save(commit=False)
			measurement.course=instance
			measurement.ceab_grad = ceab_grad
			measurement.save()
			success=True
			return HttpResponseRedirect('/curriculum/instances/'+course_url+'/'+date_url+'/',context)
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
			
		course_list = get_course_list(5, starts_with)
		
		return render_to_response('curriculum/search_list.html', {'course_list' : course_list}, context)
	
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
	
# Calculate the % of each accreditation unit based on the number of lectures for each course
def calculate_accreditation_units(request, course_url, date_url):
	context = RequestContext(request)
	
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
		contact_hours = ContactHours.objects.get(instance=instance)
		contact_hours.contact_es = unit_es
		contact_hours.contact_ed = unit_ed
		contact_hours.contact_ma = unit_ma
		contact_hours.contact_sc = unit_sc
		contact_hours.contact_co = unit_co
	
		contact_hours.save()

	# Redirect back to original instance page
	return HttpResponseRedirect('/curriculum/instances/'+course_url+'/'+date_url+'/', context)
	

		
		

	
	
	
	
		
	
	
	
	
	
	



