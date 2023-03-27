#from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'shopping_cart'

urlpatterns = [
    path('add-to-cart/<int:object_id>/', views.add_to_cart, name="add_to_cart"),
    path('order-summary/', views.order_details, name="order_summary"),
    path('success/', views.success, name='purchase_success'),
    path('item/delete/<int:item_id>/', views.delete_from_cart, name='delete_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('update-transaction/<order_id>/', views.update_transaction_records, name='update_records'),
    path('all-orders/', views.all_orders, name='all_orders')
]