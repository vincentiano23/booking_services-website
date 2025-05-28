from django.contrib import admin
from django.urls import path
from bookings import views as booking_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', booking_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('book/', booking_views.create_booking, name='create_booking'),
    path('book-trip/', booking_views.book_trip, name='book_trip'),
    path('book/success/', booking_views.booking_success, name='booking_success'),
    path('receipt/<int:booking_id>/', booking_views.generate_receipt, name='generate_receipt'),
    path('register/', booking_views.register_user, name='register'),
    path('dashboard/', booking_views.dashboard, name='dashboard'),
    path('dashboard/customer/', booking_views.customer_dashboard, name='customer_dashboard'),
    path('my-bookings/', booking_views.my_bookings, name='my_bookings'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
