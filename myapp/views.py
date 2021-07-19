from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from .models import *
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail,EmailMessage
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, get_object_or_404,reverse
import datetime
from paypal.standard.forms import PayPalPaymentsForm
 
# Create your views here.

def index(request):
    info=Website_info.objects.all()
    latest_products=Product.objects.order_by('?')[:4]
    return render(request, 'index.html',{'webinfo':info, 'latest_products':latest_products})

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
 
def get_cart_data(request):
    items=cart.objects.filter(user__id=request.user.id,status=False)
    itemtotal,total,quantity =0,0,0
    
    for i in items:
        total +=float(i.product.price)*i.quantity
        quantity+=float(i.quantity)
        
    res={
        "total":total,"quan":quantity,"itotal":itemtotal,
    }
    return JsonResponse(res)



def change_quan(request):
    if "quantity" in request.GET:
        cid = request.GET["cid"]
        qty = request.GET["quantity"]
        cart_obj = get_object_or_404(cart,id=cid)
        cart_obj.quantity = qty
        cart_obj.save()
        return HttpResponse(cart_obj.quantity)

    if "delete_cart" in request.GET:
        id = request.GET["delete_cart"]
        cart_obj = get_object_or_404(cart,id=id)
        cart_obj.delete()
        return HttpResponse(1)
    
def process_payment(request):
   items = cart.objects.filter(user_id__id=request.user.id,status=False)
    
   products=""
   amt=0
   inv = "INV10001-"
   cart_ids = ""
   p_ids =""  
   for j in items:
        products += str(j.product.name)+"\n"
        p_ids += str(j.product.id)+","
        amt += float(j.product.price)
        inv +=  str(j.id)
        cart_ids += str(j.id)+","

   paypal_dict = {
        'business': settings.PAYPAL_RECIEVER_EMAIL,
        'amount': str(amt),
        'item_name': products,
        'invoice': inv,
        'notify_url': 'http://{}{}'.format("127.0.0.1:8000",
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format("127.0.0.1:8000",
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format("127.0.0.1:8000",
                                              reverse('payment_cancelled')),
   }
   usr = User.objects.get(username=request.user.username)
   ord = Order(cust_id=usr,cart_ids=cart_ids,product_ids=p_ids)
   ord.save()
   ord.invoice_id = str(ord.id)+inv
   ord.save()
   request.session["order_id"] = ord.id
    
   form = PayPalPaymentsForm(initial=paypal_dict)
   return render(request, 'process_payment.html', {'form': form})
def payment_done(request):
    if "order_id" in request.session:
        order_id = request.session["order_id"]
        ord_obj = get_object_or_404(Order,id=order_id)
        ord_obj.status=True
        ord_obj.save()
        
        for i in ord_obj.cart_ids.split(",")[:-1]:
            cart_object = cart.objects.get(id=i)
            cart_object.status=True
            cart_object.save()
    return render(request,"payment_success.html")

def payment_cancelled(request):
    return render(request,"payment_failed.html")

def order_history(request):
    context = {}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data

    all_orders = []
    orders = Order.objects.filter(cust_id__id=request.user.id).order_by("-id")
    for order in orders:
        products = []
        for id in order.product_ids.split(",")[:-1]:
            pro = get_object_or_404(Product, id=id)
            products.append(pro)
        ord = {
            "order_id":order.id,
            "products":products,
            "invoice":order.invoice_id,
            "status":order.status,
            "date":order.processed_on,
        }
        all_orders.append(ord)
    context["order_history"] = all_orders
    return render(request,"order_history.html",context)

def sendemail(request):
    context = {}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data

    if request.method=="POST":
    
        rec = request.POST["to"].split(",")
        print(rec)
        sub = request.POST["sub"]
        msz = request.POST["msz"]

        try:
            em = EmailMessage(sub,msz,to=rec)
            em.send()
            context["status"] = "Email Sent"
            context["cls"] = "alert-success"
        except:
            context["status"] = "Could not Send, Please check Internet Connection / Email Address"
            context["cls"] = "alert-danger"
def contact(request):
    a=Contact.objects.all()
    
    if request.method =="POST":
        n=request.POST["name"]
        e=request.POST["email"]
        s=request.POST["subject"]
        m=request.POST["message"]
        
        data=Contact(name=n,email=e,subject=s,message=m)
        data.save()
        
    return render(request,'contact.html')