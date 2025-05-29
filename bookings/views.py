from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from .forms import BookingForm, CustomUserCreationForm
from .models import Booking

def home(request):
    return render(request, 'bookings/home.html')

# Registration View
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect_user_dashboard(user)
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# Role-based Redirect
def redirect_user_dashboard(user):
    if user.is_admin():
        return redirect('admin_dashboard')
    elif user.is_worker():
        return redirect('worker_dashboard')
    else:
        return redirect('customer_dashboard')


@login_required
def customer_dashboard(request):
    return render(request, 'bookings/customer_dashboard.html')
# Unified Dashboard Routing
@login_required
def dashboard(request):
    if request.user.role == 'admin':
        return render(request, 'bookings/admin_dashboard.html')
    elif request.user.role == 'worker':
        return render(request, 'bookings/worker_dashboard.html')
    else:
        return redirect('book_trip')


# Customer Booking View
@login_required
def book_trip(request):
    if request.method == 'POST':
        travel_date = request.POST['travel_date']
        travel_time = request.POST['travel_time']
        origin = request.POST['origin']
        destination = request.POST['destination']

        # Prevent duplicate booking
        exists = Booking.objects.filter(
            customer=request.user,
            travel_date=travel_date,
            travel_time=travel_time,
            destination=destination
        ).exists()

        if exists:
            messages.error(request, "You already booked this trip.")
            return redirect('book_trip')

        Booking.objects.create(
            customer=request.user,
            destination=destination,
            travel_date=travel_date,
            travel_time=travel_time
        )
        return redirect('booking_success')

    return render(request, 'bookings/book_trip.html')


# Worker/Admin Create Booking
@login_required
def create_booking(request):
    if not request.user.is_worker() and not request.user.is_admin():
        return redirect('dashboard')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.save()
            return redirect('booking_success')
    else:
        form = BookingForm()
    return render(request, 'bookings/create_booking.html', {'form': form})


# Booking Success Page
@login_required
def booking_success(request):
    booking_id = request.session.get('booking_id')
    if not booking_id:
        return redirect('home')  # or show a message

    return render(request, 'bookings/booking_success.html', {
        'booking_id': booking_id
    })



# Show My Bookings (for customers)
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-travel_date', '-travel_time')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})


# Generate PDF Receipt
@login_required
def generate_receipt(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    template = get_template("bookings/receipt_template.html")
    html = template.render({'booking': booking})
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{booking.id}.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF receipt', status=500)
    return response
