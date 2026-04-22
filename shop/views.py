from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import UserRegistrationForm
from .models import *
from django.core.mail import send_mail
from django.http import HttpResponse

# ===== AUTH VIEW (LOGIN + REGISTER) =====
def auth_view(request):
    login_form = AuthenticationForm()
    register_form = UserRegistrationForm()

    if request.method == "POST":

        # LOGIN
        if "login" in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get("username")
                password = login_form.cleaned_data.get("password")
                user = authenticate(username=username, password=password)

                if user is not None:
                    if user.is_active:
                        login(request, user)
                        messages.success(request, f"Welcome, {username}!")
                        return redirect("home")
                    else:
                        messages.error(request, "Your account is not activated yet. Please check your email.")
                else:
                    messages.error(request, "Invalid username or password.")

        # REGISTER

        elif "register" in request.POST:
            register_form = UserRegistrationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save(commit=False)
                user.is_active = False
                user.save()

                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                activation_link = f"{request.scheme}://{request.get_host()}/accounts/activate/{uid}/{token}/"

                subject = "Activate your Nepal Aircon Service account"
                message = (
                    f"Hi {user.username},\n\n"
                    f"Click the link below to activate your account:\n\n"
                    f"{activation_link}\n\n"
                    f"If you did not register, ignore this email."
                )
                try:
                    send_mail(
                        subject,
                        message,
                        "Nepal Aircon Service <mrbabusir86@gmail.com>",
                        [user.email],
                        fail_silently=False,
                    )
                    messages.success(request, "✅ Registration successful! Check your email to activate your account.")
                except Exception as e:
                    print(f"[EMAIL ERROR] {e}")
                    messages.error(request, f"Account created but email failed: {e}")

                # ✅ Use redirect to 'auth', NOT '/accounts/login/?form=login'
                return redirect("auth")
            else:
                # Form invalid — show register panel again with errors
                messages.error(request, "Please fix the errors below.")
    return render(request, "auth.html", {
        "login_form": login_form,
        "register_form": register_form
    })

# ===== LOGOUT =====
def logout_view(request):
    logout(request)
    return redirect("home")

# ===== ACCOUNT ACTIVATION =====
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, TypeError, ValueError, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Your account has been activated!")
        return redirect("home")
    else:
        messages.error(request, "Activation link is invalid!")
        return redirect("auth")
def csrf_failure(request, reason=""):
    return render(request, "403_csrf.html", status=403)
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get("cart", {})

    pid = str(product.id)

    if pid in cart:
        cart[pid]["qty"] += 1
    else:
        cart[pid] = {
            "name": product.name,
            "price": float(product.price),
            "qty": 1,
            "image": product.image.url if product.image else ""
        }

    request.session["cart"] = cart
    request.session.modified = True
   # 🔥 TOTAL ITEMS & PRICE
    total_items = sum(item["qty"] for item in cart.values())
    total_price = sum(
        Decimal(item["price"]) * item["qty"]
        for item in cart.values()
    )

    return JsonResponse({
        "total_items": total_items,
        "total_price": float(total_price),
    })
@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})

    pid = str(product_id)

    if pid in cart:
        del cart[pid]
        request.session["cart"] = cart
        request.session.modified = True

    return redirect("cart")
@login_required
def cart_view(request):
    cart = request.session.get("cart", {})

    total = sum(
        item["price"] * item["qty"]
        for item in cart.values()
    )

    return render(request, "cart.html", {
        "cart": cart,
        "total": total
    })

@login_required
def place_order(request):
    if request.method == "POST":
        cart = request.session.get("cart", {})

        if not cart:
            return redirect("cart")

        total_items = sum(item["qty"] for item in cart.values())
        total_price = sum(
            Decimal(str(item["price"])) * item["qty"]
            for item in cart.values()
        )

        order = Order.objects.create(
            user=request.user,
            item=cart,
            total_price=total_price
        )

        # Clear cart
        request.session["cart"] = {}
        request.session.modified = True

        # Build admin panel URL dynamically
        domain = request.get_host()
        scheme = request.scheme
        admin_url = f"{scheme}://{domain}/admin/shop/order/{order.id}/change/"

        # ===== EMAIL TO CUSTOMER =====
        customer_message = f"""
Hi {request.user.username},

Your order #{order.id} has been placed successfully!

Order Summary:
Total Items : {total_items}
Total Price : Rs {total_price:.2f}

We will contact you shortly to confirm your order.

Thank you for shopping with Nepal Aircon Service!
        """
        send_mail(
            f"Order #{order.id} Confirmed — Nepal Aircon Service",
            customer_message,
            "Nepal Aircon Service <mrbabusir86@gmail.com>",
            [request.user.email],
            fail_silently=False,
        )

        # ===== EMAIL TO OWNER =====
        # Build cart items list for email
        items_list = "\n".join([
            f"  - {item['name']} x{item['qty']} @ Rs {item['price']} each"
            for item in cart.values()
        ])

        owner_message = f"""
Hello,

A new order has been placed on Nepal Aircon Service!

Order ID  : #{order.id}
Customer  : {request.user.username}
Email     : {request.user.email}
Total Items: {total_items}
Total Price: Rs {total_price:.2f}

Items Ordered:
{items_list}

View in admin panel:
{admin_url}
        """
        send_mail(
            f"🛒 New Order #{order.id} from {request.user.username}",
            owner_message,
            "Nepal Aircon Service <mrbabusir86@gmail.com>",
            ["mrbabusir86@gmail.com"],
            fail_silently=False,
        )

        request.session["order_success_message"] = f"🎉 Order #{order.id} placed successfully!"
        request.session.modified = True

        return redirect("home")


def product_list(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all()
    
    if category_id:
        products = Product.objects.filter(is_available=True, category_id=category_id)
    else:
        products = Product.objects.filter(is_available=True)
    
    return render(request, 'products.html', {
        'products': products,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_available=True)
    return render(request, 'product_detail.html', {
        'product': product
    })

def reset_admin(request):
    from django.contrib.auth.models import User
    try:
        user = User.objects.get(username='mrbabusir')
        user.set_password('NewPassword456!')
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        return HttpResponse(f"Done! is_staff={user.is_staff}, is_superuser={user.is_superuser}")
    except User.DoesNotExist:
        return HttpResponse("User not found!")