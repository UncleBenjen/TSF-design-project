from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
#
from curriculum.forms import UserForm, UserProfileForm
from curriculum.models import UserInfo, Department, ProgramStream, Course, CourseInstance

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
	except:
		up = u

	context_dict = {'userprofile' : up}	
	
	return render_to_response('curriculum/profile.html',context_dict, context) 

def register(request):
	context = RequestContext(request)
	
	# Boolean to see if registration was successful
	registered = False
	
	# If HTTP = POST, we are inserting / processing a record
	if request.method == 'POST':
		# Get information from form
		user_form = UserForm(data = request.POST)
		profile_form = UserProfileForm(data = request.POST)
		
		# If forms are valid
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			
			# Hash the users password
			user.set_password(user.password)
			user.save()
			
			# Sort out user profile instance
			# Do not commit since we need to save the user attribute ourselves
			profile = profile_form.save(commit = False)
			profile.user = user
			profile.save()
			
			# Get the picture if it was included
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			
			# Registration was successful
			registered = True
			
		# Something went wrong....dude....shiiiiieetttt
		else:
			print(user_form.errors)
			print(profile_form.errors)
	
	# Not an HTTP POST
	# Render blank forms
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
		
	return render_to_response(
			'curriculum/register.html',
			{'user_form' : user_form, 'profile_form' : profile_form, 'registered' : registered},
			context)
			
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
			print("Login Details were Invalid: {0}, {1}.".format(username, password))
			return HttpResponse("FOOL! IT WAS ALL WRONG!")
			
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
	
	try:
		program = ProgramStream.objects.get(name = program_name)
		context_dict['program'] = program
		
		department = program.department.name
		context_dict['department'] = department
		
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

def course(request, course_name_url):
	context = RequestContext(request)

	# Get the name from the url that was passed with the request
	course_name = course_name_url.replace('_','/')
	context_dict={'course_name':course_name}
	
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

	except Course.DoesNotExist:
		pass

	return render_to_response('curriculum/course.html', context_dict, context)

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
			#instance = CourseInstance.objects.filter(course=parent_course).filter(date=instance_date)
			instance = CourseInstance.objects.get(course=parent_course,date=instance_date)
			context_dict['instance']=instance
			#context_dict['professors']=instance.professors
		except CourseInstance.DoesNotExist:
			pass

	except Course.DoesNotExist:
		pass

	return render_to_response('curriculum/instance.html', context_dict, context)