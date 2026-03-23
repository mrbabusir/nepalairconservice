from django.db import models

# Create your models here.
class Booking(models.Model):
    SERVICE_CHOICES = [
        ('REPAIR', 'AC Repair Service'),
        ('INSTALLATION', 'AC Installation'),
        ('GAS_REFILL', 'Gas Refill'),
        ('CLEANING', 'AC Cleaning Service'),
    ]
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    address = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.service}'