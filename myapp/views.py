from django.shortcuts import redirect
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from .models import *
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, get_object_or_404
import datetime
# Create your views here.

def index(request):
    info=Website_info.objects.all()
    return render(request, 'index.html',{'webinfo':info})

def about(request):
    return render(request, 'about.html' )



def checkout(request):
    return render(request, 'checkout.html' )

def confirmation(request):
    return render(request, 'confirmation.html' )

def contact(request):
    
    return render(request, 'contact.html' )
def blog(request):
    b=Blog.objects.all()
    return render(request,'blog.html',{'blog':b})

def elements(request):
    
    return render(request, 'elements.html' )



def main(request):
    return render(request, 'main.html' )

def product_details(request):
    return render(request, 'product_details.html' )

def shop(request):
    products=None
    categories=Category.get_all_categories()
    categoryID=request.GET.get('category')
    if categoryID:
        products=Product.get_all_products_by_categoryId(categoryID)
    else:
        products=Product.get_all_products()
    data={}
    data['products']=products
    data['categories']=categories
    
    return render(request, 'shop.html',data)  



def register(request):
    if request.method=="POST":
        fname = request.POST['fname']
        lname=request.POST['lname']
        uname=request.POST['username']
        email = request.POST['email']
        phoneno=request.POST['phoneno']
        password = request.POST['password']
        usertype=request.POST['utype']
        usr=User.objects.create_user(uname,email,password)
        
        usr.first_name=fname
        usr.last_name=lname
        
        
        if usertype=="sell":
            usr.is_staff=True
        usr.save()
         
        reg=register_table(user=usr,contact_number=phoneno)
        reg.save()
        return render(request, 'signup.html',{"status":" Congratulatons {} your account registered successfully".format(fname)})
         
    return render(request, 'signup.html')

def check_user(request):
    if request.method=="GET":
        un = request.GET["usern"]
        check = User.objects.filter(username=un)
        if len(check) == 1:
            return HttpResponse("Exists")
        else:
            return  HttpResponse("Not Exists")  

def user_login(request):
      
    if request.method=="POST":
        un = request.POST["username"]
        pwd = request.POST["password"]
        print(un)

        user=authenticate(username=un,password=pwd)
        if user:
            login(request,user)
            if user.is_superuser:
                return HttpResponseRedirect ("/admin")
            if user.is_staff:
                return HttpResponseRedirect ("/seller_dashboard")
            if user.is_active:
                return HttpResponseRedirect ("/cust_dashboard")
        else:
            return render(request,"elements.html",{"status":"Invalid Username or Password"})

    return HttpResponse("Called")
    
@login_required
def cust_dashboard(request):
    context = {}
    check = register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
    return render(request,"cust_dashboard.html",context)

@login_required
def seller_dashboard(request):
    return render(request,"seller_dashboard.html")

def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

def edit_profile(request):
    context={}
    data=register_table.objects.get(user__id=request.user.id)
    context["data"]=data
    if request.method=="POST":
        fn=request.POST["fname"]
        ln=request.POST["lname"]
        em=request.POST["email"]
        
        cn=request.POST["contact"]
        age=request.POST["age"]
        c=request.POST["city"]
        pc=request.POST["pcode"]
        g=request.POST["gender"]
        a=request.POST["address"]
        usr=User.objects.get(id=request.user.id)
        usr.first_name=fn
        usr.last_name=ln
        usr.email=em
        usr.save()
        
        data.contact_number=cn
        data.age=age
        data.city=c 
        data.postal_code=pc 
        data.gender=g 
        data.address=a 
        data.save()
        
        if "image" in request.FILES:
            img=request.FILES['image']
            data.profile_pic=img
            data.save()        
        context["status"]="Changes done successfully"
                
    return render(request,"edit_profile.html",context)

def change_password(request):
    context={}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
    if request.method=="POST":
        current = request.POST["cpwd"]
        new_pas = request.POST["npwd"]
        
        user = User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)
        if check==True:
            user.set_password(new_pas)
            user.save()
            context["msz"] = "Password Changed Successfully!!!"
            context["col"] = "alert-success"
            user = User.objects.get(username=un)
            login(request,user)
        else:
            context["msz"] = "Incorrect Current Password"
            context["col"] = "alert-danger"

    return render(request,"change_password.html",context)

def add_to_cart(request):
     context={}
     items = cart.objects.filter(user__id=request.user.id,status=False)
     context["items"] = items

     if request.user.is_authenticated:
         
         if request.method=="POST":
             pid = request.POST["pid"]
             qty = request.POST["qty"]
             is_exist = cart.objects.filter(product__id=pid,user__id=request.user.id,status=False)
             if len(is_exist)>0:
                 context["msz"] = "Item Already Exists in Your Cart"
                 context["cls"] = "alert alert-warning"
             else:    
                 product =get_object_or_404(Product,id=pid)
                 usr = get_object_or_404(User,id=request.user.id)
                 c = cart(user=usr,product=product,quantity=qty)
                 c.save()
                 context["msz"] = "{} Added in Your Cart".format(product.name)
                 context["cls"] = "alert alert-success"
     else:
         context["status"] = "Please Login First to View Your Cart"
     return render(request,"cart.html",context)
          