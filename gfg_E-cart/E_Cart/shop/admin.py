from django.contrib import admin

from .models import Product, Cart, Customer, Orderedplaced, Coupon
# Register your models here.

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Orderedplaced)
admin.site.register(Coupon)

