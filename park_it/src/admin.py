from django.contrib import admin

from .models import Customer,Partner,Booking

# Register your models here.
admin.site.register(Customer)
admin.site.register(Partner)
admin.site.register(Booking)