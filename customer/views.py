from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.forms import UserInfoForm, UserProfileForm
from accounts.models import User, UserProfile
from accounts.views import check_role_customer
from django.contrib import messages

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def c_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method=='POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        userinfo_form = UserInfoForm(request.POST, instance=request.user)
        if profile_form.is_valid() and userinfo_form.is_valid():
            userinfo_form.save()
            profile_form.save()
            messages.success(request, "Your profile updated successfully!")
            return redirect('c_profile')
        else:
            print(profile_form.errors)
            print(userinfo_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        userinfo_form = UserInfoForm(instance=request.user)

    context = {
        'profile_form': profile_form,
        'userinfo': userinfo_form,
        'profile': profile,

    }
    return render(request, 'customer/c_profile.html', context)
