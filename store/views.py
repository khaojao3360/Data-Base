from django.shortcuts import render,redirect, get_object_or_404
from .models import (
    seller, seller_address, product_category, product, users, user_address, 
    user_payment, status, shipping_company, order_details, reviews, cart, wishlist
)
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .form import SignUpForm
from django import forms
import uuid
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import json
import logging
from django.http import JsonResponse
import random

logger = logging.getLogger(__name__)
def home(request):
    products_list = list(product.objects.all())
    # Randomly 8 products 
    featured_products = random.sample(products_list, min(len(products_list), 8))
    categories = product_category.objects.all()
    
    return render(request, "home.html", {
        'products': featured_products, 
        'categories': categories
    })

def login_user(request):
    if request.method == "POST":
        if request.POST.get('action') == "Login":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have been logged in!")
                return redirect('home')  # Make sure 'home' URL pattern exists
            else:
                messages.error(request, "Invalid username or password")
                return redirect('login')
                
        elif request.POST.get('action') == "Sign Up":
            form = SignUpForm(request.POST)
            if form.is_valid():
                try:
                    # Save the Django auth user first
                    django_user = form.save(commit=True)
                    last_user = users.objects.order_by('-user_id').first()
                    if last_user:
                        last_number = int(last_user.user_id[1:])
                        new_number = last_number + 1
                    else:
                        new_number = 1
                    new_user_id = f'U{new_number:04d}'
                    new_user = users.objects.create(
                        user_id=new_user_id,
                        username=form.cleaned_data['username'],
                        first_name=form.cleaned_data['firstname'],
                        last_name=form.cleaned_data['lastname'],
                        email=form.cleaned_data['email'],
                        password=django_user.password,
                        date_of_birth=form.cleaned_data['dob'],
                        phone_number=form.cleaned_data['phonenum']
                    )
                    
                    # Log the user in automatically
                    login(request, django_user)
                    messages.success(request, "Registration successful!")
                    return redirect('home')  # Make sure 'home' URL pattern exists
                    
                except Exception as e:
                    # If something goes wrong, delete the auth user if it was created
                    if 'django_user' in locals():
                        django_user.delete()
                    messages.error(request, f"Registration failed: {str(e)}")
                    return redirect('login')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{error}")
                return redirect('login')
    
    return render(request, "login.html", {'form': SignUpForm()})

def logout_user(request):
    logout(request)
    messages.success(request, "logged out")
    return redirect('home')

def shop_grid(request):
    product_list = product.objects.all()
    
    # Get price filter parameters
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    # Apply price filter if parameters exist
    if min_price and max_price:
        # Remove currency symbol and convert to float
        min_price = float(min_price.replace('THB', '').strip())
        max_price = float(max_price.replace('THB', '').strip())
        product_list = product_list.filter(price__gte=min_price, price__lte=max_price)
    
    # Pagination
    paginator = Paginator(product_list, 12)
    page = request.GET.get('page', 1)
    products = paginator.page(page)
    
    context = {
        'products': products,
        'categories': product_category.objects.all(),
    }
    return render(request, 'shop_grid.html', context)

def product_categories(request, cat_id):
    # Get the category or return 404 if not found
    category = get_object_or_404(product_category, cat_id=cat_id)
    product_items = product.objects.filter(cat_id=cat_id)
    categories = product_category.objects.all()
    
    context = {
        'products': product_items,
        'categories': categories,
        'current_category': category
    }
    return render(request, 'cat_grid.html', context)


def product_detail(request, prod_id):
    product_item = product.objects.get(prod_id=prod_id)
    product_reviews = reviews.objects.filter(prod_id=prod_id)
    return render(request, 'product_detail.html', {'product': product_item, 'reviews': product_reviews})

def wishlist_page(request):
    wishlist_items = wishlist.objects.select_related('prod_id').filter(user_id__username=request.user.username)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def wishlist_delete(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prod_id = data.get('prod_id')
            
            # Get the user
            user_obj = get_object_or_404(users, username=request.user.username)
            # Get the product
            product_obj = get_object_or_404(product, prod_id=prod_id)
            
            # Get and delete the wishlist item
            wishlist_item = wishlist.objects.filter(
                user_id=user_obj,
                prod_id=product_obj
            ).first()
            
            if wishlist_item:
                wishlist_item.delete()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Item deleted from wishlist successfully'
                })
            
            return JsonResponse({
                'status': 'error',
                'message': 'Item not found in wishlist'
            })
            
        except Exception as e:
            logger.error(f"Error deleting item from wishlist: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': 'Failed to delete item from wishlist'
            }, status=400)
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

@login_required
def wishlist_add(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prod_id = data.get('prod_id')
            
            # Get the product
            product_obj = get_object_or_404(product, prod_id=prod_id)
            
            # Get the user
            user_obj = get_object_or_404(users, username=request.user.username)
            
            # Check if item already exists in wishlist
            wishlist_item = wishlist.objects.filter(user_id=user_obj, prod_id=product_obj).first()
            
            if wishlist_item:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Item already in wishlist'
                })
            else:
                # Create new wishlist item
                wishlist.objects.create(
                    user_id=user_obj,
                    prod_id=product_obj
                )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Item added to wishlist successfully'
            })
            
        except Exception as e:
            logger.error(f"Error adding item to wishlist: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': 'Failed to add item to wishlist'
            }, status=400)
            
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

