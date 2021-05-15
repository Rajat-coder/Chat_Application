from django.shortcuts import render
from django.contrib.auth import login, logout
from authentication.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate

# Create your views here.


def HomeView(request):
    return render(request,"homepage.html")

def IndexView(request):
    user = request.user
    if user.is_authenticated:
        return HttpResponseRedirect(reverse("homepage"))
    else:
        return render (request, 'registerpage.html' ) 


def SignUpView(request):
    if request.method == "POST":
        username=request.POST.get("username")
        if username:
            obj=User.objects.filter(username=username)
            if obj:
                message="Username already taken . Please try another"
                context={"message":message}
                return render (request, 'registerpage.html',context)
        email=request.POST.get("email")
        password=request.POST.get("password") 
        password2=request.POST.get("password2")
        if password == password2:
            message="User created successfully "
            context={"message":message}
            user=User.objects.create_user(username = username, password = password,email=email)
            return render (request, 'registerpage.html',context )
        else:
            message="Password doesnt match . Please try again"
            context={"message":message}
            return render (request, 'registerpage.html',context )

def LoginView(request):
    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        if username and password :
            user=authenticate(username=username,password=password)
            if user:
                login(request,user)
                return HttpResponseRedirect(reverse("homepage"))    
        return HttpResponseRedirect(reverse("login"))


    