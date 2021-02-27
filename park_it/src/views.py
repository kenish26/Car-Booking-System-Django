
from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate,login,logout

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.

from .models import *
from .forms import CreateUserForm,CustomerForm,PartnerForm,BookingForm
from .filters import BookingFilter,PartnerAddFilter
from .decorators import *



#register_customer
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method =='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            Customer.objects.create(
                user=user,
                name=user.username,
                email=user.email,
            )

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'form':form}


    return render(request,'customer/register.html',context)

#register_partner
@unauthenticated_user
def registerPartner(request):
    forms = CreateUserForm()
    if request.method =='POST':
        forms = CreateUserForm(request.POST)
        if forms.is_valid():
            user = forms.save()
            username = forms.cleaned_data.get('username')

            group = Group.objects.get(name='parking_lot')
            user.groups.add(group)

            Partner.objects.create(
                user=user,
                name=user.username,
                email=user.email,
            )

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'forms':forms}


    return render(request,'parking_lot/register_partner.html',conext)

@unauthenticated_user
def loginPage(request):
    if request.method =='POST':
        username = request.POST.get('usernae')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username OR Password is incorrect')
            return render(request,'login.html')
    context = {}
    return render(request,'login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

#admin_
@login_required(login_url='login')
@admin_only
def home(request):
    booking = Booking.objects.all()
    customers = Customer.objects.all()
    partner = Partner.objects.all()
    total_customers = customers.count()
    total_partner = partner.count()
    total_booking = booking.count()
    accepted = booking.filter(status='Accepted').count()
    pending = booking.filter(status='Pending').count()
    context = {'booking':booking, 'customers':customers,'partner':partner,
	'total_booking':total_booking,'accepted':accepted,
	'pending':pending,'total_customers':total_customers , 'total_partner':total_partner }
    
    return render(request, 'dashboard.html', context)


#details_customer
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])   
def userPage(request):
    booking = request.user.customer.booking_set.all()

    total_booking = booking.count()
    accepted = booking.filter(status='Accepted').count()
    pending = booking.filter(status='Pending').count()

    print('booking:',booking)
    myFilter = BookingFilter(request.GET,queryset=booking)
    booking = myFilter.qs 
    context = {'booking':booking,'total_booking':total_booking,'accepted':accepted,
	'pending':pending,'myFilter':myFilter}
    return render(request,'customer/user.html', context) 

#details_partner
@login_required(login_url='login')
@allowed_users(allowed_roles=['parking_lot'])   
def userPartner(request):
    booking = request.user.partner.booking_set.all()

    total_booking = booking.count()
    accepted = booking.filter(status='Accepted').count()
    pending = booking.filter(status='Pending').count()

    print('booking:',booking)
    myFilter = BookingFilter(request.GET,queryset=booking)
    booking = myFilter.qs 
    context = {'booking':booking,'total_booking':total_booking,'accepted':accepted,
	'pending':pending,'myFilter':myFilter}
    return render(request,'parking_lot/user.html', context) 

#update_customer
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','parking_lot'])

def accountSettings(request):
    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
    if group == 'parking_lot':
        return redirect('account_partner')
    
    customer = request.user.customer
    form = CustomerForm(instance=customer) 
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES,instance=customer)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'customer/account_settings.html', context)

#update_parking_lots
@login_required(login_url='login')
@allowed_users(allowed_roles=['parking_lot'])  
def account_Partner(request):
	partner = request.user.partner
    
	forms = PartnerForm(instance=partner)
    
	if request.method == 'POST':
		forms = PartnerForm(request.POST, request.FILES,instance=partner)
		if forms.is_valid():
			forms.save()

    
	context = {'forms':forms}
	return render(request, 'parking_lot/account_partner.html', context)

#admin
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    booking = customer.booking_set.all()
    booking_count = booking.counts()

    myFilter = BookingFilter(request.GET,queryset=booking)
    booking = myFilter.qs 

    context = {'customer':customer, 'booking':booking, 'booking_count':booking_count,'myFilter':myFilter}
    return render(request, 'admin/customer.html',context)

#admin_partner
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def partners(request):
	partner = Partner.objects.all()
	return render(request, 'admin/partner.html', {'partner':partner})
#admin_partner_detail
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def partner_detail(request, pk):
    partner = Partner.objects.get(id=pk)
    booking = partner.booking_set.all()
    booking_count = booking.count()

    myFilter = BookingFilter(request.GET,queryset=booking)
    booking = myFilter.qs 

    context = {'partner':partner, 'booking':booking, 'booking_count':booking_count,'myFilter':myFilter}
    return render(request, 'admin/partner_detail.html',context)

#delete_booking_admin
@login_required(login_url='login')
def deleteBooking(request, pk):
	bookings = Booking.objects.get(id=pk)
	if request.method == "POST":
		bookings.delete()
		return redirect('home')
	context = {'item':bookings}
	return render(request, 'delete.html', context)

#create_booking_admin
@login_required(login_url='login')
def createBooking(request,pk):
    customer = Customer.objects.get(id=pk)
    form = BookingForm(initial={'customer':customer})
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {'form':form}
    return render(request, 'admin/booking_form.html', context)

#create_booking_admin
@login_required(login_url='login')
def createBookingP(request,pk):
    partner = Partner.objects.get(id=pk)
    form = BookingForm(initial={'partner':partner})
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {'form':form}
    return render(request, 'admin/booking_form.html', context)

#update
@login_required(login_url='login')
def updateBooking(request, pk):
    group = None
    if request.user.groups.exists():
        group = request.users.groups.all()[0].name
    if group == 'parking_lot':
        booking = Booking.objects.get(id=pk)
        form = BookingForm(instance=booking)
        if request.method == 'POST':
        	form = BookingForm(request.POST, instance=booking)
        	if form.is_valid():
        		form.save()
        		return redirect('/')
        context = {'form':form}
        return render(request, 'parking_lot/booking_form_partner.html', context)
    if group == 'admin':
        Booking = Booking.objects.get(id=pk)
        form = BookingForm(instance=booking)
        if request.method == 'POST':
        	form = BookingForm(request.POST, instance=booking)
        	if form.is_valid():
        		form.save()
        		return redirect('/')
        context = {'form':form}
        return render(request, 'admin/booking_form.html', context)
    return render(request, 'admin/booking_form.html')


#update_customer_admin
@login_required(login_url='login')
@admin_only
def accountSettings_admin(request,pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer) 
    if request.method == 'POST':
        form = CustomerForm(request.POST,instance=customer)
        if form.is_valid():
            form.save()
    context = {'form':form ,'customer':customer}
    return render(request, 'admin/account_settings.html', context)

#update_partner_admin
@login_required(login_url='login')
@admin_only
def accountSettings_admin(request,pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer) 
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES,instance=customer)
        if form.is_valid():
            form.save()
    context = {'form':form ,'customer':customer}
    return render(request, 'admin/account_settings.html', context)

#update_partner_admin
@login_required(login_url='login')
@admin_only
def account_Partner_admin(request,pk):
    partner = Partner.objects.get(id=pk)
    forms = PartnerForm(instance=partner)
    if request.method == 'POST':
        forms = PartnerForm(request.POST, request.FILES,instance=partner)
        if forms.is_valid():
            forms.save()
            return redirect('home')
    context = {'forms':forms,'partner':partner}
    return render(request, 'admin/account_partner.html', context)

#--------------------------------------------------partner---------------------------------------------------------
@login_required(login_url='login')
def createBookingPartner(request):
    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
    if group == 'parking_lot':
        partner = request.user.partner
        form = BookingForm(initial={'partner':partner})
        if request.method == 'POST':
            #print('Printing POST:', request.POST)
            form = BookingForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')
        
        context = {'form':form}
        return render(request, 'parking_lot/booking_form_partner.html', context)
    if group == 'customer':
        customer = request.user.customer
        
        form = BookingForm(initial={'customer':customer})
        if request.method == 'POST':
            #print('Printing POST:', request.POST)
            form = BookingForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')

        context = {'form':form}
        return render(request, 'customer/booking_form.html', context)
    return redirect('index')


def IndexPage(request):
    partner = Partner.objects.all()
    Partnerfilter = PartnerAddFilter(request.GET,queryset=partner)
    partner = Partnerfilter.qs 
    context = {'partner':partner , 'Partnerfilter':Partnerfilter}
    return render(request, 'index.html', context)

#create_booking_admin
@login_required(login_url='login')
def createBookingCustomer(request,pk):
    customer = request.user.customer
    partner = Partner.object.get(id=pk)
    form = BookingForm(initial={'customer':customer,'partner':partner})
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-page')
    context = {'form':form}
    return render(request, 'customer/booking_form.html', context)