from urllib import request
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import BookingForm
from django.contrib import messages
from django.http import HttpResponse
from shop.models import Product


def home(request):
    products = Product.objects.all()

    # Grab the order success message from session and remove it
    order_msg = request.session.pop("order_success_message", None)

    # Booking form code...
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            send_mail(
                subject="New AC Service Booking",
                message=f"""
                New Booking Received:
                Name: {form.cleaned_data['name']}
                Phone: {form.cleaned_data['phone']}
                Service: {form.cleaned_data['service']}
                Note: {form.cleaned_data['note']}
                """,
                from_email="noreply@nepalaircon.com",
                recipient_list=["your-email@example.com"],
            )
            messages.success(request, "Your booking has been submitted successfully!")
            return redirect("/")
    else:
        form = BookingForm()

    return render(request, "index.html", {
        "products": products,
        "order_success_message": order_msg,  # ✅ pass to template
        "form": form
    })


def book_appointment(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()

            # Email content
            subject = "🔔 New AC Service Booking"
            message = f"""
New AC Booking Received

Name: {booking.name}
Phone: {booking.phone}
Service: {booking.get_service_display()}
Note : {booking.note or 'N/A'}
Address: {booking.address or 'N/A'}
"""

            send_mail(
                subject,
                message,
                None,
                ['nepalairconservice@gmail.com'],  # YOUR email
                fail_silently=False,
            )

            response = HttpResponse("""
                <div class="alert success">
                    Booking successful! ✅<br>
                    We will contact you shortly.
                </div>
            """)
            response["HX-Trigger"] = "bookingSuccess"
            return response

        # Errors
        errors = "<div class='alert error'><ul>"
        for field, msgs in form.errors.items():
            for msg in msgs:
                errors += f"<li>{msg}</li>"
        errors += "</ul></div>"

        return HttpResponse(errors)


