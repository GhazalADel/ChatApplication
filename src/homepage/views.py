from django.shortcuts import render,redirect

# Create your views here.
def home_page_view(request,*args,**kwargs):
    context={}
    if request.user.is_authenticated:
        return render(request,"homepage/home.html",context)
    return redirect('login')
