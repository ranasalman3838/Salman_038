from django.db import models
from datetime import date
from django.contrib.auth.models import User
# Create your models here.

class Website_info(models.Model):
    website_title=models.CharField(max_length=50)
    website_copyright=models.CharField(max_length=50)
    Email = models.CharField(max_length=50)
    Contact = models.CharField(max_length=30)
    Address = models.CharField(max_length=50)
    Facebook = models.CharField(max_length=50)
    Pintrest = models.CharField(max_length=50)
    Instagram = models.CharField(max_length=50)
    Twitter = models.CharField(max_length=50)
    

class  Blog(models.Model):   
    title=models.CharField('Post Title',max_length=100)
    description=models.TextField('Post Description')
    posted_date=models.DateField(default=date.today)
    images = models.ImageField(upload_to="images/")

class Category(models.Model):
    name = models.CharField(max_length=50)
    def get_all_categories():
        return Category.objects.all()
    
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    posted_date = models.DateField(default=date.today)
    image=models.ImageField(upload_to='uploads/products/')
    #decorators
    @staticmethod
    def get_all_products():
        return Product.objects.all()
    
    @staticmethod
    def get_all_products_by_catagoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()
   
   
   
   
   
    def __str__(self):
        return self.name
    
# class User(models.Model):
#     fname = models.CharField(max_length=50)
#     lname=models.CharField(max_length=50)
#     email=models.EmailField(max_length=50)
#     phoneno=models.IntegerField()
#     password=models.CharField(max_length=50)
#     def __str__(self):
#         return self.fname   
    
    
class register_table(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    contact_number=models.IntegerField()
    profile_pic =models.ImageField(upload_to = "profiles/%Y/%m/%d",null=True,blank=True)
    age = models.CharField(max_length=250,null=True,blank=True)
    city = models.CharField(max_length=250,null=True,blank=True)
    postal_code=models.IntegerField(null=True)
    gender = models.CharField(max_length=250,default="Male")
    Address=models.TextField(null=True)
    added_on =models.DateTimeField(auto_now_add=True,null=True)
    update_on = models.DateTimeField(auto_now=True,null=True)

    
    def __str__(self):
        return self.user.username
    
class cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status=models.BooleanField(default=False)
    added_on = models.DateTimeField(auto_now=True,null=True)
    update_on = models.DateTimeField(auto_now=True,null=True)
    
    def __str__(self):
        return self.user.username
    
class Order(models.Model):
    cust_id=models.ForeignKey(User,on_delete=models.CASCADE)
    cart_ids=models.CharField(max_length=234)
    product_ids=models.CharField(max_length=250)
    invoice_id = models.CharField(max_length=250)
    status =models.BooleanField(default=False)
    processed_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.cust_id.username
    
class Contact(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    subject=models.CharField(max_length=100)
    message=models.TextField()
    