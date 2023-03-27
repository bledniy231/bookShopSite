import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from Library.models import Profile, Books
from shopping_cart.models import OrderItem, Order
from shopping_cart.extras import generate_order_id
####


def get_user_pending_order(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        return order[0]
    return 0


@login_required()
def add_to_cart(request, **kwargs):
    user_profile = get_object_or_404(Profile, user=request.user)
    product = Books.objects.filter(id=kwargs.get('object_id', "")).first()
    #if product in request.user.profile.books.all():
    #    messages.info(request, 'У вас уже есть эта книга')
    #    return redirect('library:home')
    order_item, status = OrderItem.objects.get_or_create(product=product)
    user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)
    if status:
        user_order.ref_code = generate_order_id()
        user_order.save()

    messages.info(request, "Книга добавлена в корзину")
    return redirect('library:home')


@login_required()
def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Выбранная книга удалена из заказа")
    return redirect('shopping_cart:order_summary')


@login_required()
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {'order': existing_order}
    return render(request, 'shopping_cart/order_summary.html', context)


@login_required()
def checkout(request):
    existing_order = get_user_pending_order(request)
    context = {'order': existing_order}
    return render(request, 'shopping_cart/checkout.html', context)


#@login_required()
#def process_payment(request, order_id):
#    return redirect(reverse_lazy('shopping_cart:update_records', kwargs={'order_id': order_id, }))


@login_required()
def update_transaction_records(request, order_id):
    order_to_purchase = Order.objects.filter(pk=order_id).first()
    order_to_purchase.is_ordered = True
    order_to_purchase.date_ordered = datetime.datetime.now()
    order_to_purchase.save()
    order_items = order_to_purchase.items.all()
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())
    user_profile = get_object_or_404(Profile, user=request.user)
    order_products = [item.product for item in order_items]
    user_profile.books.add(*order_products)
    user_profile.save()

    messages.info(request, "Вы совершили покупку")
    return redirect('shopping_cart:purchase_success')


def success(request, **kwargs):
    return render(request, 'shopping_cart/purchase_success.html', {})

def get_user_all_orders(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    allOrdersQuerySet = Order.objects.filter(owner=user_profile, is_ordered=True)
    if allOrdersQuerySet.exists():
        return allOrdersQuerySet
    return 0

def all_orders(request):
    all_existing_orders = get_user_all_orders(request)
    context = {'all_orders': all_existing_orders}
    return render(request, 'shopping_cart/all_orders.html', context)
