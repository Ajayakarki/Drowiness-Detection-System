from django.shortcuts import render, redirect
from .models import Users
from django.contrib import messages



# Create your views here.

def welcome(req):
    return render(req, 'welcome.html')

def login(req):
	if req.method == 'POST':
		users = Users()
		if users.objects.filter(email=req.POST['email'], password=req.POST['password']).exists():
			users.get(email=request.POST['email'], password=request.POST['password'])
			return redirect('login/')

	return render(req, 'login.html')


    
def register(req):
	if req.method=="POST":
		users = Users()


		users.firstname = req.POST['firstname']
		users.lastname = req.POST['lastname']
		users.email = req.POST['email']
		users.password = req.POST['password']
		users.repassword = req.POST['repassword']
		if users.password != users.repassword:
			messages.info(req, 'Password didnnot match')
		elif users.firstname == "" or users.lastname == "" or users.email == "" or users.password == "" or users.repassword == "":
			messages.info(req, 'Some fields are empty')
			return redirect('register')
		else:
			users.save()



	return render(req, 'register.html')
		

    


