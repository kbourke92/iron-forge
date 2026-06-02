import json
import dj_database_url
import Stripe
from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Product, Category, Order, OrderItem

Stripe.api_key = settings.STRIPE_SECRET_KEY

# Cart helpers

def get_cart(request):
    return request.session.get('cart', {})


def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def cart_total(cart, products_qs):
    total = Decimal('0.00')
    product_map = {str(p.id): p for p in products_qs}
    for pid, qty in cart.items():
        if pid in product_map:
            total += product_map[pid].price * qty
    return total


# Public views

def home(request):
    featured = Product.objects.filter(is_active=True)[:6]
    categories = Category.objects.all()
    return render(request, 'store/home.html', {'featured': featured, 'categories': categories})


def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    q = request.GET.get('q', '')
    cat_slug = request.GET.get('category', '')

    if q:
        products = products.filter(name__icontains=q) | products.filter(description__icontains=q)
    if cat_slug:
        products = products.filter(category__slug=cat_slug)

    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'q': q,
        'active_cat': cat_slug,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'store/product_detail.html', {'product': product})


# Cart views

def cart_view(request):
    cart = get_cart(request)
    product_ids = list(cart.keys())
    products = Product.objects.filter(id__in=product_ids)
    product_map = {str(p.id): p for p in products}

    items = []
    for pid, qty in cart.items():
        if pid in product_map:
            p = product_map[pid]
            items.append({'product': p, 'quantity': qty, 'subtotal': p.price * qty})

    total = sum(i['subtotal'] for i in items)
    return render(request, 'store/cart.html', {'items': items, 'total': total})


def add_to_cart(request, product_id):
    cart = get_cart(request)
    pid = str(product_id)
    cart[pid] = cart.get(pid, 0) + 1
    save_cart(request, cart)
    messages.success(request, 'Item added to cart!')
    return redirect(request.META.get('HTTP_REFERER', 'store:cart'))


def remove_from_cart(request, product_id):
    cart = get_cart(request)
    pid = str(product_id)
    if pid in cart:
        del cart[pid]
        save_cart(request, cart)
    return redirect('store:cart')


def update_cart(request, product_id):
    cart = get_cart(request)
    pid = str(product_id)
    qty = int(request.POST.get('quantity', 1))
    if qty > 0:
        cart[pid] = qty
    else:
        cart.pop(pid, None)
    save_cart(request, cart)
    return redirect('store:cart')


# Checkout & Stripe

def checkout(request):
    cart = get_cart(request)
    if not cart:
        return redirect('store:cart')

    products = Product.objects.filter(id__in=cart.keys())
    total = cart_total(cart, products)

    if request.method == 'POST':
        # Create order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            email=request.POST['email'],
            full_name=request.POST['full_name'],
            address=request.POST['address'],
            city=request.POST['city'],
            country=request.POST['country'],
            postal_code=request.POST['postal_code'],
            total_price=total,
        )
        product_map = {str(p.id): p for p in products}
        for pid, qty in cart.items():
            if pid in product_map:
                p = product_map[pid]
                OrderItem.objects.create(
                    order=order,
                    product=p,
                    product_name=p.name,
                    price=p.price,
                    quantity=qty,
                )

        # Create Stripe PaymentIntent
        try:
            intent = Stripe.PaymentIntent.create(
                amount=int(total * 100),
                currency='eur',
                metadata={'order_id': order.id},
            )
            order.stripe_payment_intent = intent.id
            order.save()
            return render(request, 'store/payment.html', {
                'order': order,
                'client_secret': intent.client_secret,
                'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
                'total': total,
            })
        except Stripe.error.StripeError as e:
            messages.error(request, f'Payment error: {str(e)}')
            order.delete()

    return render(request, 'store/checkout.html', {
        'total': total,
        'user': request.user,
    })


def payment_success(request):
    cart = get_cart(request)
    request.session['cart'] = {}
    request.session.modified = True
    return render(request, 'store/payment_success.html')


def payment_cancel(request):
    return render(request, 'store/payment_cancel.html')


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        if webhook_secret:
            event = Stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        else:
            event = json.loads(payload)
    except Exception:
        return HttpResponse(status=400)

    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        order_id = intent.get('metadata', {}).get('order_id')
        if order_id:
            Stripe.Order.objects.filter(id=order_id).update(status='paid')

    return HttpResponse(status=200)


# Simple admin dashboard

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('store:home')
    orders = Order.objects.all()[:20]
    products = Product.objects.all()
    total_revenue = sum(o.total_price for o in Order.objects.filter(status='paid'))
    return render(request, 'store/admin_dashboard.html', {
        'orders': orders,
        'products': products,
        'total_revenue': total_revenue,
        'order_count': Order.objects.count(),
        'product_count': Product.objects.count(),
    })
