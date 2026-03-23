from django.contrib import admin
from .models import Booking

admin.site.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'phone', 'status', 'created_at')
    list_filter = ('status', 'service')
    list_editable = ('status',)
    search_fields = ('name', 'phone')
