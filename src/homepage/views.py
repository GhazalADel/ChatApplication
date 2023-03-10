from django.shortcuts import render

# Create your views here.
def home_page_view(request,*args,**kwargs):
    context={}
    if request.user.is_authenticated:
        return render(request,"homepage/home.html",context)
    return render(request,"homepage/tmp.html",context)
