from django.contrib import admin
from django.urls import path
from bookings import views as booking_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', booking_views.home, name='home'),
    path('admin/', admin.site.urls),

    # Registration and Auth
    path('register/', booking_views.register_user, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Dashboard Routes
    path('dashboard/', booking_views.dashboard, name='dashboard'),
    path('dashboard/customer/', booking_views.customer_dashboard, name='customer_dashboard'),
    path('dashboard/worker/', booking_views.dashboard, name='worker_dashboard'),  # same view reused
    path('dashboard/admin/', booking_views.dashboard, name='admin_dashboard'),    # same view reused

    # Booking Routes
    path('book/', booking_views.create_booking, name='create_booking'),
    path('book-trip/', booking_views.book_trip, name='book_trip'),
    path('book/success/', booking_views.booking_success, name='booking_success'),
    path('receipt/<int:booking_id>/', booking_views.generate_receipt, name='generate_receipt'),

    # Customer Bookings
    path('my-bookings/', booking_views.my_bookings, name='my_bookings'),
]
