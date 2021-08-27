from .models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
#from .import models
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


import os
import cv2
import winsound
import numpy as np
import random as rd
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
from tensorflow.keras import layers 

#print(os.path.dirname(os.path.abspath(__file__))+'\keras_model\drowsiness_model.h5')
#new_model = tf.keras.models.load_model(os.path.dirname(os.path.abspath(__file__))+'\keras_model\drowsiness_model.h5')
new_model = tf.keras.models.load_model('F:/PROJECTS/Semester6/FYP/Django/Authentication/accounts/keras_model/drowsiness_model.h5')






# Create your views here.

@login_required(login_url = "login_attempt") 
def home(request):
    return render(request , 'home.html')
    


def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/')
        
        
        
        profile_obj = Profile.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('/')
        

        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/')
            
            
            
        
        login(request , user)
        return redirect('/home') 

    return render(request, 'login.html')


def register_attempt(request):

    if request.method == 'POST':
        username = request.POST.get('username') 
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)
        try:
            if len(password) < 5:
                messages.success(request, 'Password is too short. Include at least 5 character')
                return redirect('/register') 


        
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is taken.')
                return redirect('/register')

            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is taken.')
                return redirect('/register')
            
            user_obj = User(username = username , email = email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
            profile_obj.save()
            send_mail_after_registration(email , auth_token)
            return redirect('/token')

        except Exception as e:
            print(e)


    return render(request , 'register.html')


def log_out(request):
    logout(request)
    return render(request,'login.html')


def success(request):
    return render(request, 'success.html')

def token_send(request):
    return render(request, 'token_send.html')


def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')



def error_page(request):
    return  render(request , 'error.html')



def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )  

## () 

def predict(request):  
    if request.method == 'POST': 
        frequency = 1500
        duration = 2000
        #face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + os.path.dirname(os.path.abspath(__file__))+'keras_model\haarcascade_frontalface_default.xml')
        #eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + os.path.dirname(os.path.abspath(__file__))+'keras_model\haarcascade_eye.xml')
        
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

        
        capture = cv2.VideoCapture(0)
        #### Will Check wjether the webcam will open or not
        if not capture.isOpened():
            capture = cv2.VideoCapture(1)
        if not capture.isOpened():
            raise IOError("Unable to open webcam") 
        counter = 10
        msg = "Counter:"
        while True:
            ret,frame = capture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face = face_cascade.detectMultiScale(gray, 1.1, 4)
            for(x, y, w, h) in face:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray)
                for(ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex,ey),(ex+ew,ey+eh),(0, 255, 0), 2)
                    if len(eyes) == 0:
                        print("Eyes not detected")
                    else:
                        for (ex,ey,ew,eh) in eyes:
                            eyes_roi = roi_color[ey: ey+eh, ex: ex+ew]
            final_image = cv2.resize(eyes_roi, (224,224))
            final_image = np.expand_dims(final_image,axis = 0) ## Here needed 4th dimension
            final_image = final_image/255.0

            predictions = new_model.predict(final_image)
            if (predictions >= 0.5):
                if counter > 0:
                    counter = 10 
                status = "Open Eyes"
                x1,y1,w1,h1 = 0,0,175,75
        
                ## Draw Black rectangle
                cv2.rectangle(frame, (x1, x1), (x1 + w1, y1 +h1), (0,0,0), -1)
                ### Adding Text
                cv2.putText(frame, status, (x1 + int(w1/10),y1 + int(h1/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
            else:
                counter = counter - 1
                cv2.putText(frame, msg + "" + str(counter), (280, 470), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_8)
        
                status = "Close Eyes"
        
                ## Draw a background rectangle
                cv2.rectangle(frame, (x1, x1), (x1 + w1, y1 + h1), (0,0,0), -1)
                ## Adding Text
                cv2.putText(frame, status, (x1 + int(w1/10), y1 + int(h1/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                if counter == 0:
                    x1,y1,w1,h1 = 0,0,175,75
                    ##Adding Text
                    cv2.putText(frame, 'Alert Alert!!', (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 2, cv2.LINE_8)
            
                    winsound.Beep(frequency, duration)
                    counter = 10
            cv2.imshow('Drowsiness Detection', frame)

             ### For exitting the windows
            if cv2.waitKey(2) & 0xFF == ord('q'):
                break
        capture.release()
        cv2.destroyAllWindows() 
    return render(request, 'home.html')



    
        
        




