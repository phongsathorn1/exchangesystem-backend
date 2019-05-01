from django.contrib import admin
from exchange.models import Product

class ProductAdmin(admin.ModelAdmin):
    fields = ('name', 'detail', 'quantity', 'created_date', 'category', 'want_product', 'owner')

admin.site.register(Product, ProductAdmin)