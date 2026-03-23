from django import forms
from .models import Booking
import re

class BookingForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'placeholder': 'Phone Number',
            'pattern': r'^\+?\d{8,15}$',
            'required': True
        })
    )

    class Meta:
        model = Booking
        fields = ["name", "phone", "service", "address", "note"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your Name"}),
            "address": forms.Textarea(attrs={
                "placeholder": "Address",
                "rows": 2
            }),
            "note": forms.Textarea(attrs={
                "placeholder": "Additional Note (optional)",
                "rows": 2
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.fullmatch(r'\+?\d{8,15}', phone):
            raise forms.ValidationError("Enter a valid phone number")
        return phone

