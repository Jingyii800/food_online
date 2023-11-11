from django.shortcuts import get_object_or_404, render, redirect
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from accounts.views import check_role_vendor
from menu.forms import CategoryForm, FoodItemForm
from menu.models import Category, FoodItem
from vendor.forms import VendorForm
from vendor.models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import slugify

def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def v_profile(request):
    profile = get_object_or_404(UserProfile, user = request.user)
    vendor = get_object_or_404(Vendor, user = request.user)

    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "Profile Updated Successfully.")
            return redirect('v_profile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)

    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor) # form will load existing contents

    context ={
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        "profile" : profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/v_profile.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor = vendor).order_by('created_at')
    context = {
        'vendor': vendor,
        'categories': categories
    }
    return render(request, 'vendor/menu_builder.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(category = category, vendor=vendor)
    context = {
        'fooditems': fooditems,
        'category': category

    }
    return render(request, 'vendor/fooditems_by_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    vendor = get_vendor(request)
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category= form.save(commit=False)
            category.vendor = vendor
            category.slug = slugify(category_name)
            category.save()
            messages.success(request, "Category Created Successfully")
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        category_form = CategoryForm()
    context = {
        'form': category_form
    }
    return render(request, 'vendor/add_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Updated Successfully")
            return redirect('menu_builder')
        else:
            print(form.error)
    else:
        form = CategoryForm(instance=category)
        form['category'].queryset = Category.objects.filter(vendor = get_vendor(request))
    context= {
        'category' : category,
        'form': form,
    }

    return render(request, 'vendor/edit_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, "Category Deleted Successfully")
    return redirect('menu_builder')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_fooditem(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food_form = form.save(commit=False)
            food_form.vendor = get_vendor(request)
            food_form.slug = slugify(food_title)
            food_form.save()
            messages.success(request, "Food Item Created Successfully!")
            return redirect('fooditems_by_category', food_form.category.id)
        else:
            print(form.errors)
    else:
        form = FoodItemForm()
        # modify the form
        form['category'].queryset = Category.objects.filter(vendor = get_vendor(request))
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_fooditem.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_fooditem(request, pk=None):
    food= get_object_or_404(FoodItem, pk=pk)
    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES, instance=food)
        if form.is_valid():
            foodtitle = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.slug = slugify(foodtitle)
            food.save()
            messages.success(request, "Food Item Updated Successfully!")
            return redirect('fooditems_by_category', food.category.id)
    else:
        form = FoodItemForm(instance=food)
        form['category'].queryset = Category.objects.filter(vendor = get_vendor(request))
    context = {
        'form': form,
        'food': food,
    }
    return render(request, 'vendor/edit_fooditem.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_fooditem(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    food.delete()
    messages.success(request, "Food Item Deleted")
    return redirect('fooditems_by_category', food.category.id)