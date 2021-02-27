from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
#register_customer
    path('register/', registerPage ,name="register"),

#register_partner
    path('register_partner/', registerPartner ,name="register_partner"),
#Login_Logout
    path('login/', loginPage ,name="login"),
    path('logout/', logoutUser,name="logout"),

    path('', IndexPage,name="index"),
    path('home/', home,name="home"),
#details_user
    path('user/', userPage ,name="user-page"),
#details_partner
    path('partner/', userPartner ,name="user-partner"),

#admin_customer
path('customer/<str:pk>/', customer,name="customer"),
path('partners/', partners,name="partners"),
path('partner_detail/<str:pk>/', partner_detail,name="partner_detail"),

#update_customer
path('account/', accountSettings, name="account"),

#update_customer_admin
path('account_cust/<str:pk>/', accountSettings_admin, name="account_cust"),


path('account_ptr/<str:pk>/', account_Partner_admin, name="account_ptr"),

#update_partner
path('account_partner/', account_Partner, name="account_partner"),
##adminnnnnnnn-------------------------------------------------------------------------------------------------------------------------------------------

#delete
path('delete_booking/<str:pk>/', deleteBooking , name="delete_booking"),
#create
path('create_booking/<str:pk>/', createBooking , name="create_booking"),
path('create_booking_p/<str:pk>/', createBookingP , name="create_booking_p"),


#update
path('update_booking/<str:pk>/', updateBooking, name="update_booking"),


#----------------------------------------------parking_lot----------------------------------------------------------------------
path('create_booking_ptr/', createBookingPartner , name="create_booking_ptr"),

#------------------------------------------------------
path('create_booking/<str:pk>/', createBookingCustomer , name="create_booking_c"),

]

