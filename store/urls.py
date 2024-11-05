from django.urls import path, include

from . import views

app_name = 'store'

urlpatterns = [
    # Leave as empty string for base url
    path('', views.index, name="index"),
    path('shop/', views.shop, name="shop"),
    path('contact/', views.contact, name="contact"),
    path('category_detail/<int:pk>/', views.category_detail, name="category_detail"),
    path('filter-products/', views.filter, name="filter"),
    path('product_detail/<int:pk>/', views.product_detail, name="product_detail"),
    path('ajax_add_review/<int:pk>/', views.ajax_add_review, name="ajax_add_review"),
    path('add-to-cart/', views.add_to_cart, name="add-to-cart"),
    path('delete_from_cart/', views.delete_from_cart, name="delete_from_cart"),
    path('cart_view/', views.cart_view, name="cart_view"),
    path('checkout_view/', views.checkout_view, name="checkout_view"),
    path('paypal', include('paypal.standard.ipn.urls')),
    path('payment_completed/', views.payment_completed, name="payment_completed"),
    path('payment_failed/', views.payment_failed, name="payment_failed"),
    path('get_email/', views.get_email, name="get_email"),
    path('shipping_address/', views.shipping_address, name="shipping_address"),
    path('get_contact/', views.get_contact, name="get_contact"),


]
