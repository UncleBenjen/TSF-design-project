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
from curriculum.models import UserInfo, Department

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