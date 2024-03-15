from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name="register"),
    path('verify/', views.verify, name="verify"),
    path('logout/', views.logoutuser, name="logout"),

    path('detail/<int:id>/', views.detail, name='detail'),
    path('category/<str:main_category>/', views.category, name='category'),

    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    # path('cart/', views.cart_view, name='showCart'),
    path('cart/', views.cart_view, name='cart'), 
    path('get_cart_count/', views.get_cart_count, name='get_cart_count'),


    path('plus_cart/', views.plus_cart, name='plus_cart'),
    path('minus_cart/', views.minus_cart, name='minus_cart'),
    path('remove_cart/', views.remove_cart, name='remove_cart'),

]