from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Product)
class ShopOrders(admin.ModelAdmin):
    list_display = ('name', 'price', 'available', 'created_at')
    list_filter = ('available',)
    search_fields = ('name', 'description')

admin.site.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'item_names', 'total_items', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
