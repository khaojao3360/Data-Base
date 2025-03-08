from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("shop_grid/", views.shop_grid, name="shop_grid"),
    path("product/<str:prod_id>/", views.product_detail, name="product_detail"),
    path("shop_grid/<str:cat_id>/", views.product_categories, name="product_categories"),
    path("wishlist/", views.wishlist_page, name="wishlist"),
    path("wishlist_delete/", views.wishlist_delete, name="wishlist_delete"),
    path("add-to-wishlist/", views.wishlist_add, name="add_to_wishlist"),
]
