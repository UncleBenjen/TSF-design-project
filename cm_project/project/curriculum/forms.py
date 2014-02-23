from django import forms
from curriculum.models import UserInfo, Course
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
	password = forms.CharField(widget = forms.PasswordInput())
	username = forms.CharField()
	
	class Meta:
		model = User
		fields = ['username', 'email', 'password']
		
class UserProfileForm(forms.ModelForm):
	
	class Meta:
		model = UserInfo
		fields = ['website', 'picture', 'type']


class CourseForm(forms.ModelForm):
	class Meta:
		model = Course
		fields = ('course_code','name','lecture_hours','lab_hours','credit','description','website','year','pre_requisites','anti_requisites','co_requisites')