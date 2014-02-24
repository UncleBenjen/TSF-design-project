from django import forms
from curriculum.models import UserInfo, Course, CourseInstance, Concept
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget

class UserForm(forms.ModelForm):
	password = forms.CharField(widget = forms.PasswordInput())
	username = forms.CharField()
	
	class Meta:
		model = User
		fields = ['username', 'email', 'password','first_name','last_name']
		
class UserProfileForm(forms.ModelForm):
	
	class Meta:
		model = UserInfo
		fields = ['website', 'picture', 'type']


class CourseForm(forms.ModelForm):
	class Meta:
		model = Course
		fields = ('course_code','name','lecture_hours','lab_hours','credit','description','website','year','pre_requisites','anti_requisites','co_requisites')

class InstanceForm(forms.ModelForm):
	date = forms.DateField(widget = SelectDateWidget())

	class Meta:
		model = CourseInstance
		fields = ['course','date','textbook','professors','assistants','acc_math','acc_science','acc_eng_science','acc_eng_design','acc_comp','semester','concepts']

class ConceptForm(forms.ModelForm):
	class Meta:
		model = Concept
		fields = ['name','description','ceab_unit','related_concepts']