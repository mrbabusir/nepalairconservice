from django.contrib import admin
from django.urls import path
from .views import home, book_appointment

urlpatterns = [
    path('', home, name='home'),
    path('book-appointment/', book_appointment, name='book_appointment'),
]