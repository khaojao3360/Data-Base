from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from store.models import cart, product, users, order_details, user_address, user_payment, status, shipping_company
from django.http import JsonResponse
import json
import logging
from django.views.decorators.http import require_http_methods
from django.utils import timezone
import random

logger = logging.getLogger(__name__)

def cart_summary(request):
    cart_items = cart.objects.select_related('prod_id').filter(user_id__username=request.user.username)
    product_items = product.objects.all()
    
    # Calculate totals for each item and cart total
    cart_total = 0
    for item in cart_items:
        # Default quantity to 1 if not set
        quantity = getattr(item, 'quantity', 1)
        # Calculate total for this item
        item.total = float(item.prod_id.price) * quantity
        cart_total += item.total

    return render(request, 'shoping_cart.html', {
        'cart_items': cart_items, 
        'product_items': product_items,
        'cart_total': cart_total
    })

@login_required
def cart_add(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prod_id = data.get('prod_id')
            
            # Get the product
            product_obj = get_object_or_404(product, prod_id=prod_id)
            
            # Get the user from store's users table based on authenticated user
            user_obj = get_object_or_404(users, username=request.user.username)
            # Check if item already exists in cart
            cart_item = cart.objects.filter(user_id=user_obj, prod_id=product_obj).first()
            if cart_item:
                cart_item.save()
            else:
                cart.objects.create(
                    user_id=user_obj,
                    prod_id=product_obj,
                )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Item added to cart successfully'
            })
            
        except Exception as e:
            logger.error(f"Error adding item to cart: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f'Failed to add item to cart {request.user.username} {get_object_or_404(users, username=request.user.username)}'
            }, status=400)
            
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

@login_required
def cart_delete(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prod_id = data.get('prod_id')
            
            # Get the user
            user_obj = get_object_or_404(users, username=request.user.username)
            # Get the product
            product_obj = get_object_or_404(product, prod_id=prod_id)
            
            # Get and delete the cart item
            cart_item = cart.objects.filter(
                user_id=user_obj,
                prod_id=product_obj
            ).first()
            
            if cart_item:
                cart_item.delete()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Item deleted from cart successfully'
                })
            
            return JsonResponse({
                'status': 'error',
                'message': 'Item not found in cart'
            })
            
        except Exception as e:
            logger.error(f"Error deleting item from cart: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': 'Failed to delete item from cart'
            }, status=400)
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

def cart_update(request):
    return render(request, 'cart/update.html')

def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.prod_id.price * item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'cart_total': total,
    }
    return render(request, 'cart/shoping_cart.html', context)

@login_required
def checkout(request):
    if request.method == 'POST':
        try:
            # Get all necessary objects
            user_obj = get_object_or_404(users, username=request.user.username)
            address_obj = get_object_or_404(user_address, address_id='UAD0001')
            payment_obj = get_object_or_404(user_payment, payment_id='P002')
            status_obj = get_object_or_404(status, status_id='STID01')
            
            # Get cart items
            cart_items = cart.objects.select_related('prod_id').filter(user_id__username=request.user.username)
            
            if not cart_items:
                return JsonResponse({'status': 'error', 'message': 'Cart is empty'})

            # Get the last order ID or start with 20001
            last_order = order_details.objects.order_by('-order_id').first()
            if last_order:
                new_order_id = last_order.order_id + 1
            else:
                new_order_id = 20001

            # Get random shipping company
            shipping_companies = shipping_company.objects.filter(
                shipping_company_ID__in=[f'SP00{i}' for i in range(1, 6)]
            )
            random_shipping = random.choice(shipping_companies)
            
            current_time = timezone.now()

            # Create order for each cart item
            for item in cart_items:
                quantity = getattr(item, 'quantity', 1)  # Default to 1 if quantity not set
                total = float(item.prod_id.price) * quantity

                order_details.objects.create(
                    order_id=new_order_id,
                    user_id=user_obj,
                    address_id=address_obj,
                    payment_id=payment_obj,
                    prod_id=item.prod_id,
                    quantity=quantity,
                    total=total,
                    status_id=status_obj,
                    shipping_company_ID=random_shipping,
                    created_at=current_time,
                    updated_at=current_time
                )

                # Delete item from cart after adding to order
                item.delete()

            return JsonResponse({
                'status': 'success',
                'message': 'Order created successfully',
                'order_id': new_order_id
            })

        except Exception as e:
            logger.error(f"Error creating order: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f'Failed to create order: {str(e)}'
            }, status=400)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

