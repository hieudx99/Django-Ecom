from django.http import HttpResponse
from django.shortcuts import render, redirect

from carts.models import CartItem
from orders.forms import OrderForm
from orders.models import Order, Payment, OrderProduct
import datetime
import json

def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered = False, order_number = body['orderID'])

    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status']
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart item to the Order Product table
    cart_items = CartItem.objects.filter(user=request.user)

    for product in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.item_id = product.item_id
        orderproduct.quantity = product.quantity
        orderproduct.product_price = product.product_price
        orderproduct.ordered = True
        orderproduct.save()

        cart_items = CartItem.objects.get(id=product.id)
        item_variation = cart_items.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(item_variation)
        orderproduct.save()
    # Reduce the quantity of the sold products

    # Clear the cart

    # Send order email to the customer

    # Send order number and transaction id back to sendData method via JsonResponse
    return render(request, 'orders/payments.html')

def place_order(request, total=0, quantity=0):
    current_user = request.user

    # If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    ship_pay = 0
    for cart_item in cart_items:
        total += (cart_item.item.public_price * cart_item.quantity)
        quantity += cart_item.quantity
    ship_pay = (2 * total)/100
    grand_total = total + ship_pay

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.ship_pay = ship_pay
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'ship_pay': ship_pay,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)
        else:
            return redirect('checkout')
