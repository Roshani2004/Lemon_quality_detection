from django.shortcuts import render,HttpResponse 
import pickle 
import numpy as np 

from PIL import Image 
from io import BytesIO 
import tensorflow as tf 
import os 
model=tf.keras.models.load_model("./lemon.h5") 
class_name=['bad_quality','empty_background','good_quality'] 

def read_file_as_image(data): 
    image=np.array(Image.open(BytesIO(data))) 
    return image # Create your views here. 
def home(request): 
    return render(request,'index.html') 
def about(request): 
    return render(request,'about.html') 
def contact(request): 
    return render(request,'contact.html') 

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# ---------------- REGISTER ----------------
def registration(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check empty fields
        if not username or not password:
            return render(request, "registration.html", {
                "error": "All fields are required"
            })

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, "registration.html", {
                "error": "Username already exists"
            })

        # Create new user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()

        return redirect("login")

    return render(request, "registration.html")


# ---------------- LOGIN ----------------
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("prediction")
        else:
            return render(request, "login.html", {
                "error": "Invalid Username or Password"
            })

    return render(request, "login.html")
@login_required
def prediction(request): 
    context = { "status":False } 
    if request.method == 'POST':
         f=request.FILES['lemon'] 
         data=f.read() 
         image=read_file_as_image(data) 
         img_batch=np.expand_dims(image,0) 
         predictions=model.predict(img_batch) 
         predicted_class=class_name[np.argmax(predictions[0])] 
         confidence=np.max(predictions[0]) 
         context={ "actual_image":str(f), "confidence":str(confidence*100), "prediction":str(predicted_class), "status":True } 
         return render(request,"prediction.html",context) 
    else: 
        return render(request,"prediction.html",context)