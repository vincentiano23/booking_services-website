from django import forms
from .models import Booking
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['destination', 'travel_date', 'travel_time', 'seats']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'branch')

    def clean_branch(self):
        role = self.cleaned_data.get('role')
        branch = self.cleaned_data.get('branch')

        if role == 'worker' and not branch:
            raise forms.ValidationError("Workers must be assigned a branch.")
        return branch
