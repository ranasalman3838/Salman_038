from django.contrib import admin
from .models import *
# Register your models here.

class websiteinfo_Data(admin.ModelAdmin):
    list_display = ['website_title','website_copyright','Email','Contact','Address','Facebook','Pintrest','Instagram','Twitter']
    
class Blog_Data(admin.ModelAdmin):
    list_display = ['title','description','posted_date','images']

class catagory_Data(admin.ModelAdmin):
    list_display = ['name']
    
class product_Data(admin.ModelAdmin):
    list_display = ['name','price','category','description','posted_date','image']

# class user_Data(admin.ModelAdmin):
#     list_display = ['fname','lname','email','phoneno','password']   
    
admin.site.register(Website_info, websiteinfo_Data)    
admin.site.register(Blog, Blog_Data)
admin.site.register(Category, catagory_Data)
admin.site.register(Product, product_Data)
# admin.site.register(User, user_Data)
admin.site.register(register_table)
admin.site.register(cart)
