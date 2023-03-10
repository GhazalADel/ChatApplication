from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login,authenticate
from account.forms import RegistrationForm

def register_view(request, *args, **kwargs):
	user = request.user
	if user.is_authenticated: 
		return redirect('home')

	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			phone = form.cleaned_data.get('phone')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(phone=phone, password=raw_password)
			login(request, account)
			destination = kwargs.get("next")
			if destination:
				return redirect(destination)
			return redirect('home')
		else:
			print(form)
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'account/register.html', context)
        