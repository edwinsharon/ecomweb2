from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from verify_email.email_handler import send_verification_email
from django.conf import settings
from django.core.mail import send_mail
import random

# Create your views here.

def index(request):
    categories = Categories.objects.all()
    
    if request.method == 'POST':
        category_id = request.POST.get('category')
        if category_id == "all":
            products = product.objects.all()
        else:
            products = product.objects.filter(category_id=category_id)
            return render(request, 'index.html', {'products': products, 'categories': categories})
    else:
        products =product.objects.all()
        
    return render(request, 'index.html', {'products': products, 'categories': categories})

def createseller(request):
    if request.POST:
        email=request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password')
        confirmpassword=request.POST.get('confirmpassword')
        
        if not username or not email or not password or not confirmpassword:
            messages.error(request,'all fields are required.')

        elif confirmpassword != password:
            messages.error(request,"password doesnot match")
           
        elif User.objects.filter(email=email).exists():
            messages.error(request,"email already exist")
           
        elif User.objects.filter(username=username).exists():
            messages.error(request,"username already exist")

        else:
           
            user = User.objects.create_user(username=username, email=email, password=password)    
            user.is_staff=True
            user.save()
            messages.success(request,"account created successfully")
            return render(request, "createseller.html")
    return render(request,"createseller.html")    


def sellerlogin(request):
    if 'username' in request.session:
        return redirect('sellerindex')
    if request.POST:
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            request.session['username']=username
            return redirect("sellerindex")
    return render(request,"sellerlogin.html") 

def sellerindex(request):
    user = request.user
    products = product.objects.filter(seller=user)
    categories = Categories.objects.all() 
    context = {
        'products': products,
        'categories':categories
    }
    return render(request, "sellerindex.html", context)

def logoutseller(request):
    logout(request)
    request.session.flush()
    return redirect('sellerlogin')
def logoutuser(request):
    logout(request)
    request.session.flush()
    return redirect('index')

def usersignup(request):
    if request.POST:
        email=request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password')
        confirmpassword=request.POST.get('confirmpassword')
        
        if not username or not email or not password or not confirmpassword:
            messages.error(request,'all fields are required.')

        elif confirmpassword != password:
            messages.error(request,"password doesnot match")
           
        elif User.objects.filter(email=email).exists():
            messages.error(request,"email already exist")
           
        elif User.objects.filter(username=username).exists():
            messages.error(request,"username already exist")

        else:
           
            user = User.objects.create_user(username=username, email=email, password=password)    
            user.save()
            messages.success(request,"account created successfully")
            return render(request, "createuser.html")
    return render(request,"createuser.html") 


def userlogin(request):
    if 'username' in request.session:
        return redirect('index', user=request.user.username)  
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            request.session['username'] = username
            return redirect('index')  
        
    return render(request, 'userlogin.html') 

def verification(request):
    if request.method == 'POST':
        otp_from_form = request.POST.get('otp1')
        otp_from_session = request.session.get('otp')
        if otp_from_form == otp_from_session:
            del request.session['otp']  
            return redirect('changepassword')  
        else:
            messages.error(request, 'Invalid OTP. Please try again.')


    otp = generate_otp()
    request.session['otp'] = otp 
    message = f'Your email verification code is: {otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [request.session.get('email')]
    send_mail('Email Verification', message, email_from, recipient_list)

    return render(request, "getemail.html")   



def generate_otp():
    otp = ''.join(random.choices('123456789', k=6))
    return otp    

def getotp(request):
    if request.method=='POST':
        otp1=request.POST.get('otp1')
        return (otp1)
    return render(request,'getemail.html')
    

def changepassword(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        cfpassword = request.POST.get('cfpassword')
        if password == cfpassword:
            email=request.session.get('email')
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password changed successfully!')
            if user.is_staff:
                return redirect('sellerlogin')
            else:
                return redirect('userlogin')
        else:
            messages.error(request, 'Passwords do not match. Please try again.')
    return render(request, 'changepassword.html')



def getemail(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if user:
                request.session['email'] = email
                return redirect('verification')
        except User.DoesNotExist:
            messages.error(request, "Email not found in the database.")
    return render(request, "verificationmail.html")


def addproduct(request):
    if request.method == 'POST':
        productname = request.POST.get("productname")
        prize = request.POST.get("prize")
        offer = request.POST.get("offer")
        speed = request.POST.get("speed")
        color = request.POST.get("color")
        description = request.POST.get("description")
        category_id = request.POST.get("category")  
        image = request.FILES.get("image")
        seller = request.user

        try:
            category_instance = Categories.objects.get(id=category_id)
        except Categories.DoesNotExist:
            pass
        if not productname or not prize or not offer or not speed or not color or not description or not category_id or not image:
            messages.error(request, "All fields are required")
        else:
            probj = product(productname=productname, prize=prize, offer=offer, speed=speed, color=color, description=description, category=category_instance, seller=seller, image=image)
            probj.save()
            messages.success(request, "Product added successfully")
            return redirect('addproduct')
    
    categories = Categories.objects.all()  
    return render(request, "addpro.html", {"categories": categories})



def delete_g(request,pk):
    prodobj=product.objects.get(pk=pk)
    prodobj.delete()
    return redirect("sellerindex")


def edit_g(request,pk):
     if request.method =="POST":
        productname = request.POST.get("productname")
        prize = request.POST.get("prize")
        offer = request.POST.get("offer")
        speed = request.POST.get("speed")
        color = request.POST.get("color")
        description = request.POST.get("description")
        category = request.POST.get("category")  
        image = request.FILES.get("image")
        seller = request.user
        category_instance = get_object_or_404(Categories, pk=category)
        probj.category = category_instance
        probj = product(productname=productname, prize=prize, offer=offer, speed=speed, color=color, description=description, seller=seller, image=image) 
        probj.objects.filter(pk=pk).update()
        return redirect('sellerindex')
     else:            
          data=product.objects.get(pk=pk)
          return render(request,'editpro.html',{'data':data})
      
      
def productsdisplay(request,pk):
    products = product.objects.get(pk=pk)
    return render(request,'product.html',{'data': products})

def addcategory(request):
    if request.method == 'POST':
        category_name = request.POST.get("category")
        seller = request.user 
        new_category = Categories(category=category_name, seller=seller)
        new_category.save()
        
        messages.success(request, 'Category added successfully!')
        return redirect('addproduct') 
    return render(request, 'addpro.html')
def filtercategory(request):
    categories = Categories.objects.all()
    if request.method == 'POST':
        category_id = request.POST.get('category')
        if category_id == "all":
            products = product.objects.all()
        else:
            products = product.objects.filter(category_id=category_id)
    else:
        products =product.objects.all()
        
    return render(request, 'sellerindex.html', {'products': products, 'categories': categories})


def deletecat(request,pk):
    catobj=Categories.objects.get(pk=pk)
    catobj.delete()
    return redirect("addproduct")

def searchpro(request):
    categories = Categories.objects.all()
    products =product.objects.all()
    if request.POST:
        searchitem=request.POST.get("searchitem")
        if searchitem=="":
            return redirect('index')
        else:
            products = product.objects.filter(productname=searchitem)
            return render(request,'index.html',{"products":products,'categories': categories})
    return redirect(request, 'index')







