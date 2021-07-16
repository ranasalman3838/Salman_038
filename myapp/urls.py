from django.urls import path
from .import views 

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('cart/',views.add_to_cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('confirmation/',views.confirmation,name='confirmation'),
    path('contact/',views.contact,name='contact'),
    path('elements/',views.elements,name='elements'),
    # path('login/',views.login,name='login'),
    
    path('product_details/',views.product_details,name='product_details'),
    path('shop/',views.shop,name='shop'),
    path('blog/',views.blog,name='blog'),
    # path('signup/',views.signup,name='signup'),
    path('register/',views.register,name='register'),
    path("check_user/",views.check_user,name="check_user"),
    path('user_login',views.user_login,name='user_login'),
    path("cust_dashboard/",views.cust_dashboard,name="cust_dashboard"),
    path("seller_dashboard/",views.seller_dashboard,name="seller_dashboard"),
    path('user_logout',views.user_logout,name="user_logout"),
    path('edit_profile',views.edit_profile,name="edit_profile"),
    path('change_password',views.change_password,name="change_password"),
    path('get_cart_data',views.get_cart_data,name="get_cart_data"),
    path("change_quan",views.change_quan,name="change_quan"),
   
    path('process_payment',views.process_payment,name="process_payment"),
    path('payment_done',views.payment_done,name="payment_done"),
    path('payment_cancelled',views.payment_cancelled,name="payment_cancelled"),
    path('order_history',views.order_history,name="order_history"),
    path("sendemail",views.sendemail, name="sendemail"),
    ]