from django import forms
from curriculum.models import UserInfo
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
	