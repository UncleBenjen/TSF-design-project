from django import forms
from curriculum.models import UserInfo, Course, CourseInstance, Concept, Deliverable, LearningObjective
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget

class RegisterForm(forms.ModelForm):
	username = forms.CharField(max_length=25)
	password = forms.CharField(widget = forms.PasswordInput())
	confirm_password = forms.CharField(widget = forms.PasswordInput())
	
	
	class Meta:
		model = User
		fields = ['username', 'password', 'confirm_password']

	def clean(self):
		cleaned_data = self.cleaned_data
		# individual field's clean methods have already been called
		password = cleaned_data.get("password")
		confirm_password = cleaned_data.get("confirm_password")
		if password != confirm_password:
			raise forms.ValidationError("Passwords must be identical.")
	
		return cleaned_data

class UserForm(forms.ModelForm):
	first_name = forms.TextInput()
	last_name = forms.TextInput()
	email=forms.EmailInput()
	class Meta:
		model = User
		fields=['first_name','last_name','email']

class UserInfoForm(forms.ModelForm):
	website=forms.URLInput()
	class Meta:
		model = UserInfo
		fields = ['website', 'picture', 'type']
    
	#override clean to put
	def clean(self):
		#make variable to use cleaned data
		cleaned_data=self.cleaned_data
		return cleaned_data


class CourseForm(forms.ModelForm):
	description=forms.CharField(widget=forms.widgets.Textarea())
	website=forms.URLInput()

	class Meta:
		model = Course
		fields = ('course_code','name','lecture_hours','lab_hours','credit','description','website','year','pre_requisites','anti_requisites','co_requisites')

class InstanceForm(forms.ModelForm):
	date = forms.DateField(widget = SelectDateWidget())

	class Meta:
		model = CourseInstance
		fields = ['course','date','textbook','professors','assistants','acc_math','acc_science','acc_eng_science','acc_eng_design','acc_comp','semester','concepts']

class ConceptForm(forms.ModelForm):
	description=forms.CharField(widget=forms.widgets.Textarea())
	class Meta:
		model = Concept
		fields = ['name','description','ceab_unit','related_concepts']

class DeliverableForm(forms.ModelForm):
	due_date = forms.DateField(widget=SelectDateWidget())

	class Meta:
		model = Deliverable
		fields=['type','percent','due_date','course_instance']

class LearningObjectiveForm(forms.ModelForm):
	description=forms.CharField(widget=forms.widgets.Textarea())
	class Meta:
		model = LearningObjective
		fields=['name', 'description','related_concepts','course_instance']