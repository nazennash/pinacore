from django.contrib import admin
from .models import Product, Cart, User

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Cart)
