from . import views
from django.urls import path
urlpatterns = [

path('cart_session_id/',views.cart_session_id,name="cart_session_id"),
path('cart/<int:id>/', views.cart, name="cart"),
path('addtocart/<int:course>/', views.add_cart, name="add_cart"),
]