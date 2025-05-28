from django.db import models
from django.contrib.auth.models import AbstractUser

# --------------------------
# Custom User with Roles
# --------------------------
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('worker', 'Booking Worker'),
        ('customer', 'Customer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    branch = models.CharField(max_length=100, blank=True, null=True)  # For workers

    def is_worker(self):
        return self.role == 'worker'

    def is_admin(self):
        return self.role == 'admin'

    def is_customer(self):
        return self.role == 'customer'


# --------------------------
# Booking Model
# --------------------------
class Booking(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings')
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    travel_date = models.DateField()
    travel_time = models.TimeField()
    seats = models.PositiveIntegerField(default=1)
    is_paid = models.BooleanField(default=False)
    branch = models.CharField(max_length=100)  # assigned branch for this booking
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} -> {self.destination} on {self.travel_date}"
