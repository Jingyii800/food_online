from django.shortcuts import render, redirect
from accounts.utils import detectUser
from .models import User, UserProfile
from django.contrib import messages, auth
from .forms import UserForm
from vendor.forms import VendorForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

# Restrict the users from accessing the wrong role page 
# (cust !-> vendor)
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
# (vendor !->cust)
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
    
def userRegister(request):
    # handle request
    if request.user.is_authenticated:
        messages.warning(request, "You are alreay login!")
        return redirect('myAccount')
    elif request.method == 'POST':
        form = UserForm(request.POST) # get data from frontend 
        if form.is_valid():
            # # Create the user using form
            # password = form.cleaned_data['password'] # like a dic to get password value
            # # assign role to user
            # user = form.save(commit=False) # not yet to be saved, will assign other fields in form
            # user.set_password(password) # hash the password here
            # user.role = User.CUSTOMER # assign CUTOMER ROLE to user
            # form.save() # save it

            # Create user by create_user method
            first_name = form.cleaned_data['first_name']
            last_name  = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, 
                                            username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, "Register Successfully") # message
            return redirect('userRegister') 
        else:
            print(form.errors) # handle error
    
    else:
        form = UserForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/userRegister.html', context)

def vendorRegister(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are alreay login!")
        return redirect('myAccount')
    elif request.method == 'POST': # check if it's post request
        form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES) # FILES because we include files from post
        if form.is_valid() and vendor_form.is_valid():
            # create user
            first_name = form.cleaned_data['first_name']
            last_name  = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, 
                                            username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            # create vendor for this user
            vendor = vendor_form.save(commit=False) # need more fields
            vendor.user = user # get user for vendor model
            user_profile = UserProfile.objects.get(user=user) # retrieve profile from user
            vendor.user_profile = user_profile # get user profile
            vendor.save()

            messages.success(request, "Register successfully! Please wait for approval")
            return redirect('vendorRegister')

        else:
            print(form.errors)
    else:
        form = UserForm()
        vendor_form = VendorForm()
    context = {
        'form': form,
        'vendor_form': vendor_form
    }
    return render(request, 'accounts/vendorRegister.html', context)

def login(request):
    # prevent login user to see login page
    if request.user.is_authenticated:
        messages.warning(request, "You are already login")
        return redirect('myAccount')
    
    elif request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        # authenticate inbuilt function to check
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user) # login also the inbuilt function of auth
            messages.success(request, "Login Successfully")
            return redirect('myAccount')
        else:
            messages.error(request, "Invalid Login Credentidals")
            return redirect('login')
        
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request) # built-in function in auth
    messages.info(request, "Logging out")
    return redirect('login')

@login_required(login_url='login') # if user is not login, send it to login page
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')