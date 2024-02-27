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
    path('cart/', views.show_cart, name='showCart'),

    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),

]