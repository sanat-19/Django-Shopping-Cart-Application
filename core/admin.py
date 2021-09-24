from django.contrib import admin
from . models import Product, Category, CartItem
# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart_id', 'date_added',)
    list_display_links = ('id','cart_id',)
    search_fields = ['cart_id','date_added',]

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(CartItem,CartAdmin)
