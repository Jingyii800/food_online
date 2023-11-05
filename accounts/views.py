from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from .forms import UserForm

# Create your views here.
def userRegister(request):
    # handle request
    if request.method == 'POST':
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