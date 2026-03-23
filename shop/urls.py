# accounts/urls.py
from django.urls import path

from booking import views
from .views import *

urlpatterns = [
    path("register/", auth_view, name="register"),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),
    path("auth/", auth_view, name="auth"),
    path("login/", auth_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("add-to-cart/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("cart/", cart_view, name="cart"),
    path("remove-cart/<int:product_id>/", remove_from_cart, name="remove_cart"),
    path("place-order/", place_order, name="place_order"),

]
