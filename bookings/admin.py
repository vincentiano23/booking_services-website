from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'destination', 'travel_date', 'travel_time', 'is_paid')
    search_fields = ('customer__username', 'destination')
    list_filter = ('is_paid', 'travel_date')
