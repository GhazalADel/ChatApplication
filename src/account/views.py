from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login,authenticate,logout
from account.forms import RegistrationForm,AccountAuthenticationForm
from .models import Account
from django.conf import settings

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

def login_view(request, *args, **kwargs):
	context = {}
	user = request.user
	if user.is_authenticated: 
		return redirect("home")

	destination = get_redirect_if_exists(request)
	
	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			phone = request.POST['phone']
			password = request.POST['password']
			user = authenticate(phone=phone, password=password)

			if user:
				login(request, user)
				if destination:
					return redirect(destination)
				return redirect("home")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form

	return render(request, "account/login.html", context)


def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect

def logout_view(request):
	logout(request)
	return redirect("login")

def account_view(request,*arga,**kwargs):
	context={}
	user_id=kwargs.get("user_id")
	try:
		account=Account.objects.get(pk=user_id)
	except Account.DoesNotExist:
		return HttpResponse("account not found")
	if account:
		context['id']=account.id
		context['phone']=account.phone
		context['username']=account.username
		context['hide_phone']=account.hide_phone
		context['profile_image']=account.profile_image.url

		is_self=True
		is_friend=False
		user=request.user
		if user.is_authenticated and user!=account:
			is_self=False
		elif not user.is_authenticated:
			is_self=False
		
		context['is_self']=is_self
		context['is_friend']=is_friend
		context['BASE_URL']=settings.BASE_URL

		return render(request,"account/account.html",context)