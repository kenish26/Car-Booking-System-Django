import django_filters

from django_filters import DateFilter,CharFilter
from django import forms
from .models import *

class BookingFilter(django_filters.FilterSet):
    # start_date = DateFilter(field_name = "date_created", lookup_expr='gte')
    # end_date = DateFilter(field_name = "date_created", lookup_expr='lte')
    vehicle_number = CharFilter(field_name="vehicle_number",lookup_expr = 'icontains')
    class Meta:
        model = Booking
        fields = '__all__'
        exclude = ['customer' , 'date_created','date1','entry_time1']

class PartnerAddFilter(django_filters.FilterSet):
    # start_date = DateFilter(field_name = "date_created", lookup_expr='gte')
    # end_date = DateFilter(field_name = "date_created", lookup_expr='lte')
    address = CharFilter(field_name="address",lookup_expr = 'icontains' ,widget=forms.TextInput(attrs={'class': 'search_input','placeholder': "Enter a city",'autocomplete':'on'}))
    class Meta:
        model = Partner
        fields = []
