from django.contrib import admin
from .models import (
    seller, seller_address, product_category, product, users, user_address, 
    user_payment, status, shipping_company, order_details, reviews, cart, wishlist
)

# Seller Admin
class SellerAdmin(admin.ModelAdmin):
    list_display = ['seller_id', 'store_name', 'username', 'email', 'created_at']
    search_fields = ['store_name', 'username', 'email']
    list_filter = ['created_at']

class SellerAddressAdmin(admin.ModelAdmin):
    list_display = ['seller_id', 'address_line_1', 'city', 'country']
    search_fields = ['seller_id__store_name', 'address_line_1']
    list_filter = ['country']

# Product Category Admin
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['cat_id', 'name', 'desc', 'created_at', 'modified_at']
    search_fields = ['name']
    list_filter = ['created_at', 'modified_at']

# Product Admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ['prod_id', 'name', 'price', 'sales', 'quantity', 'created_at']
    search_fields = ['name', 'prod_id']
    list_filter = ['created_at', 'cat_id']

# Users Admin
class UsersAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'first_name', 'last_name', 'username', 'email', 'created_at']
    search_fields = ['first_name', 'last_name', 'username', 'email']
    list_filter = ['created_at']

# User Address Admin
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'title', 'address_line_1', 'city', 'country']
    search_fields = ['user_id__username', 'title', 'address_line_1']
    list_filter = ['country']

# User Payment Admin
class UserPaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'user_id', 'payment_method', 'provider', 'account_no']
    search_fields = ['user_id__username', 'account_no']
    list_filter = ['payment_method']

# Order Details Admin
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user_id', 'prod_id', 'quantity', 'total', 'created_at']
    search_fields = ['order_id', 'prod_id__name']
    list_filter = ['created_at', 'status_id']

# Reviews Admin
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['prod_id', 'rating', 'comment', 'created_at']
    search_fields = ['prod_id__name', 'comment']
    list_filter = ['rating']

# Cart Admin
class CartAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'prod_id']
    search_fields = ['user_id__username', 'prod_id__name']

# Wishlist Admin
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'prod_id']
    search_fields = ['user_id__username', 'prod_id__name']

# Register models with admin
admin.site.register(seller, SellerAdmin)
admin.site.register(seller_address, SellerAddressAdmin)
admin.site.register(product_category, ProductCategoryAdmin)
admin.site.register(product, ProductAdmin)
admin.site.register(users, UsersAdmin)
admin.site.register(user_address, UserAddressAdmin)
admin.site.register(user_payment, UserPaymentAdmin)
admin.site.register(order_details, OrderDetailsAdmin)
admin.site.register(reviews, ReviewsAdmin)
admin.site.register(cart, CartAdmin)
admin.site.register(wishlist, WishlistAdmin)
admin.site.register(status)
admin.site.register(shipping_company)
