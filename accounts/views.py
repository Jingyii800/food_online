from django.shortcuts import render, redirect
from accounts.utils import detectUser,send_verification_email
from orders.models import Order
from vendor.models import Vendor
from .models import User, UserProfile
from django.contrib import messages, auth
from .forms import UserForm
from vendor.forms import VendorForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.template.defaultfilters import slugify

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

            # send verification email
            mail_subject = 'Please Activate Your Account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)

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
            # generate the slug
            vendor_name = vendor_form.cleaned_data['vendor_name']
            vendor.vendor_slug = slugify(vendor_name)+'-'+ str(user.id) #make unique slug

            user_profile = UserProfile.objects.get(user=user) # retrieve profile from user
            vendor.user_profile = user_profile # get user profile
            vendor.save()

            # send verification email
            mail_subject = 'Please Activate Your Account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)

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

def activate(request, uidb64, token):
    # activate the account by is_active from false to true
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account is activated")
        return redirect('myAccount')
    else:
        messages.error(request, "Invalid Regisitration")
        return redirect('myAccount')

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
    orders = Order.objects.filter(user=request.user, is_ordered=True)
    recent_orders = orders[:5]
    context = {
        'orders': orders,
        'recent_orders': recent_orders,
        'count': orders.count()
    }
    return render(request, 'accounts/custDashboard.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email= email)
            # send reset password email
            mail_subject = 'Please Reset Your Password'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, "Password reset link is sent to your email")
            return redirect('login')
        else:
            messages.error(request, "Account does not exist.")
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')

def reset_password_validate (request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, OverflowError, ValueError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid # store uid in session
        messages.info(request, "Please rest your password.")
        return redirect('reset_password')
    else:
        messages.error(request, "This link is expired.")
        return redirect('myAccount')

def reset_password(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid') # retrieve from session (saved in reset_password_validate)
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, "Reset Successfully")
            return redirect('login')

        else:
            messages.error(request, "Passwords do not match")
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')

