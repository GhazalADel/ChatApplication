from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account

class RegistrationForm(UserCreationForm):
	phone = forms.CharField(max_length=11, help_text='Required. Add a valid phone number.')

	class Meta:
		model = Account
		fields = ('phone', 'username', 'password1', 'password2', )

	def clean_phone(self):
		phone = self.cleaned_data['phone']
		if len(str(phone))!=11 or not str(phone).startswith("09"):
			raise forms.ValidationError('Invalid Phone Number Format')
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(phone=phone)
		except Account.DoesNotExist:
			return phone
		raise forms.ValidationError('Input phone is already in use.')

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
		except Account.DoesNotExist:
			return username
		raise forms.ValidationError('Username "%s" is already in use.' % username)    
    
class AccountAuthenticationForm(forms.ModelForm):

    #widget for making password hidden when writing
	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('phone', 'password')

	def clean(self):
		if self.is_valid():
			phone = self.cleaned_data['phone']
			password = self.cleaned_data['password']
			if not authenticate(phone=phone, password=password):
				raise forms.ValidationError("Invalid login")    

