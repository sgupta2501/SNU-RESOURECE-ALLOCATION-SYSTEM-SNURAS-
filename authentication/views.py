from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from app import settings
from django.core.mail import EmailMessage,send_mail
#from django.core.mail.message import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
#from email.message import EmailMessage

# Create your views here.

def register_teacher(request):

	if request.method == "POST":
		username = request.POST['username']
		fname = request.POST['fname']
		lname = request.POST['lname']
		room = request.POST['room']
		email = request.POST['email']
		pass1 = request.POST['pass1']
		pass2 = request.POST['pass2']

		if User.objects.filter(username = username):
			messages.error(request, "Username already exists. Please try another username.")
			#context = {'message':"Username already exists. Please try another username."}
			#render(request, 'err.html', context)
			print("username same error")
			return redirect('home')

		if User.objects.filter(email = email):
			messages.error(request, "Email is already in use. Please give a differnet email.")
			print("email same error")
			return redirect('home')

		if pass1 != pass2:
			messages.error(request, "Passwords didn't match")
			print("password donot match error")
			return redirect('home')

		if not username.isalnum():
			messages.error(request, "Username must be alpha-Numeric")
			print("username has special chars error")
			return redirect('home')
		
		myuser = User.objects.create_user(username,email, pass1)
		myuser.first_name=fname
		myuser.last_name=lname
		myuser.room=room
		myuser.is_staff = 1
		myuser.is_staff = 1	
		myuser.groups.add(1)
		myuser.save()

		messages.success(request, "Your account has been successfully created!. We have sent you a confirmation email, please confirm your email in order to activate your account")
		
		#welcome Email

		subject = "Welcome to SNU Resource Allocation System (SNURAS)"
		message = "Dear "+myuser.first_name +":)\n Welcome to SNURAS.\n We have also sent you a confirmation email, please confirm your email address in order to activate Your account. \n\n Thank You"
		from_email = settings.EMAIL_HOST_USER
		to_list = [myuser.email]
		send_mail(subject, message, from_email, to_list,fail_silently = True)

		# email address confirmation email
		current_site = get_current_site(request)
		email_subject = "Confirm your email @ SNU Resource Allocation System (SNURAS) Login!"
		message2 = render_to_string('email_confirmation.html',{
			'name':myuser.first_name,
			'domain':current_site.domain,
			'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
			'token': generate_token.make_token(myuser)
		})
		email=EmailMessage(
			email_subject,
			message2,
			settings.EMAIL_HOST_USER,
			[myuser.email],
		)
		email.fail_silently = True
		email.send()
				
	return render(request, 'register_teacher.html')

def register_student(request):

	if request.method == "POST":
		username = request.POST['username']
		fname = request.POST['fname']
		lname = request.POST['lname']
		roll = request.POST['roll']
		email = request.POST['email']
		pass1 = request.POST['pass1']
		pass2 = request.POST['pass2']

		if User.objects.filter(username = username):
			messages.error(request, "Username already exists. Please try another username.")
			#context = {'message':"Username already exists. Please try another username."}
			#render(request, 'err.html', context)
			print("username same error")
			return redirect('home')

		if User.objects.filter(email = email):
			messages.error(request, "Email is already in use. Please give a differnet email.")
			print("email same error")
			return redirect('home')

		if pass1 != pass2:
			messages.error(request, "Passwords didn't match")
			print("password donot match error")
			return redirect('home')

		if not username.isalnum():
			messages.error(request, "Username must be alpha-Numeric")
			print("username has special chars error")
			return redirect('home')
		
		myuser = User.objects.create_user(username,email, pass1)
		myuser.first_name=fname
		myuser.last_name=lname
		myuser.roll=roll
		myuser.is_staff = 0
		myuser.groups.add(2) 
		myuser.is_active = False
		myuser.save()

		messages.success(request, "Your account has been successfully created!. We have sent you a confirmation email, please confirm your email in order to activate your account")
		
		#welcome Email

		subject = "Welcome to SNU Resource Allocation System (SNURAS)"
		message = "Dear "+myuser.first_name +":)\n Welcome to SNURAS.\n We have also sent you a confirmation email, please confirm your email address in order to activate Your account. \n\n Thank You"
		from_email = settings.EMAIL_HOST_USER
		to_list = [myuser.email]
		send_mail(subject, message, from_email, to_list,fail_silently = True)

		# email address confirmation email
		current_site = get_current_site(request)
		email_subject = "Confirm your email @ SNU Resource Allocation System (SNURAS) Login!"
		message2 = render_to_string('email_confirmation.html',{
			'name':myuser.first_name,
			'domain':current_site.domain,
			'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
			'token': generate_token.make_token(myuser)
		})
		email=EmailMessage(
			email_subject,
			message2,
			settings.EMAIL_HOST_USER,
			[myuser.email],
		)
		email.fail_silently = True
		email.send()

	return render(request, 'register_student.html')

def activate(request, uidb64, token):


	context = {'uidb64':uidb64, 'token':token}

	
	try:
		#print('here')
		uid = force_str(urlsafe_base64_decode(uidb64))
		myuser = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError,User.DoesNotExist):
		myuser = None

	if myuser is not None and generate_token.check_token(myuser, token):
		myuser.is_active = True
		myuser.save()
		login(request, myuser)
		return redirect('home')
	else:
		return render(request, 'activation_failed.html',context)

