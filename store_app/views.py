from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Order, OrderDetail
from django.contrib.auth.decorators import login_required

from decimal import Decimal

import omise
omise.api_secret = 'skey_test_57keeul6umlho8uqitz'
omise.api_public = 'pkey_test_57keeul6mec3iw8g73s'

# Create your views here.
def home(request):
    products = Product.objects.filter(status=True)
    return render(request, 'index.html', {"products" : products})

def product_detail(request, id):
    product = Product.objects.get(id=id)
    tmp_quantity = 0
    if request.method == "POST" and not request.user.is_anonymous:
        try:
            order = Order.objects.get(customer = request.user.customer, status = Order.NEW)
        except Order.DoesNotExist:
            order = Order.objects.create(
                customer = request.user.customer,
                status = Order.NEW,
                total = 0
            )

        try:
            order_detail = OrderDetail.objects.get(order=order, product=product)
            tmp_quantity = order_detail.quantity
        except OrderDetail.DoesNotExist:
            order_detail = OrderDetail.objects.create(
                order=order,
                product=product,
                quantity=0,
                sub_total=0
            )
        
        order_detail.quantity = int(request.POST['quantity']) + tmp_quantity
        order_detail.sub_total = Decimal(product.price) * Decimal(int(request.POST['quantity']) + tmp_quantity)
        order_detail.save()

        tmp_total = 0
        for tmp_order_detail in order.order_details.all():
            tmp_total += tmp_order_detail.sub_total
        
        order.total = tmp_total
        order.save()

        return redirect('my_cart')
            
    return render(request, 'product_detail.html', {"product" : product })

def product_search(request):
    if 'product_search' in request.GET:
        products = Product.objects.filter(name__contains = request.GET['product_search'])
        return render(request, 'index.html', {"products" : products})
    else:
        return redirect('home')

@login_required(login_url="/")
def my_cart(request):
    try:
        order = Order.objects.get(customer = request.user.customer, status = Order.NEW)
        total_stang = int(order.total*100)
    except Order.DoesNotExist:
        return redirect('home')
        
    if request.method == "POST":
        omise_token = request.POST['omiseToken']
        checkout_description = request.POST['description']

        charge = omise.Charge.create(
            amount = total_stang,
            currency = "thb",
            description = checkout_description,
            card = omise_token
        )

        if charge.status == 'successful':
            order.status = Order.PAID
            order.delivery_address = request.POST['delivery_address']
            order.save()
            return redirect('my_order')
            
    return render(request, 'my_cart.html', {"order": order, "total_stang" : total_stang })

@login_required(login_url="/")
def my_order(request):
    try:
        orders = Order.objects.filter(customer = request.user.customer)
    except Order.DoesNotExist:
        return redirect('home')
        
    return render(request, 'my_order.html', {"orders": orders})

@login_required(login_url="/")
def delete_order_detail(request, id):
    try:
        order_detail = OrderDetail.objects.get(id=id)
    except OrderDetail.DoesNotExist:
        return redirect('my_cart')

    if request.method == "POST":
        order_detail.delete()

        order = Order.objects.get(customer=request.user.customer, status = Order.NEW)
        tmp_total = 0
        for tmp_order_detail in order.order_details.all():
            tmp_total += tmp_order_detail.sub_total
        
        order.total = tmp_total
        order.save()

        return redirect('my_cart')

    return render(request, 'delete_order_detail.html', {"order_detail" : order_detail})