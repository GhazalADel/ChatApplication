from django.shortcuts import render

# Create your views here.
def home_page_view(request,*args,**kwargs):
    context={}
    return render(request,"homepage/home.html",context)