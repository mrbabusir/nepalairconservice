from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import BookingForm
from django.contrib import messages
from django.http import HttpResponse
from shop.models import Product
import os


def home(request):
    try:
        products = Product.objects.filter(is_available=True)
        order_msg = request.session.pop("order_success_message", None)

        if request.method == "POST":
            form = BookingForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your booking has been submitted successfully!")
                return redirect("/")
        else:
            form = BookingForm()

        return render(request, "index.html", {
            "products": products,
            "order_success_message": order_msg,
            "form": form
        })
    except Exception as e:
        import traceback
        print ("Home view error", traceback.format_exc())
        raise


def book_appointment(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()

            subject = "New AC Service Booking"
            message = f"""
New AC Booking Received

Name    : {booking.name}
Phone   : {booking.phone}
Service : {booking.get_service_display()}
Note    : {booking.note or 'N/A'}
Address : {booking.address or 'N/A'}
"""
            try:
                send_mail(
                    subject,
                    message,
                    None,
                    ['mrbabusir86@gmail.com'],  # ← fixed your email
                    fail_silently=False,
                )
            except Exception as e:
                print(f"[EMAIL ERROR] {e}")

            response = HttpResponse("""
                <div class="alert success">
                    Booking successful! ✅<br>
                    We will contact you shortly.
                </div>
            """)
            response["HX-Trigger"] = "bookingSuccess"
            return response

        errors = "<div class='alert error'><ul>"
        for field, msgs in form.errors.items():
            for msg in msgs:
                errors += f"<li>{msg}</li>"
        errors += "</ul></div>"
        return HttpResponse(errors)

