from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from paypal.standard.forms import PayPalPaymentsForm
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from .models import *


def index(request):
    products = Product.objects.all()
    recent_products = Product.objects.order_by('-date_created')[:4]
    categorys = Category.objects.all()
    context = {'products': products, 'recent_products': recent_products, 'categorys': categorys}
    return render(request, 'store/index.html', context)


def contact(request):
    return render(request, 'store/contact.html')


def shop(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/shop.html', context)


def category_detail(request, pk):
    category = Category.objects.get(id=pk)
    products = Product.objects.filter(category=category)
    context = {'products': products}
    return render(request, 'store/category_detail.html', context)


def filter(request):
    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")

    products = Product.objects.filter(products_status="Published").order_by("id").distinct()

    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()

    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct()
    data = render_to_string("store/filter_list.html", {'products': products})
    return JsonResponse({'data': data})


def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    products = Product.objects.all()
    reviews = ProductReview.objects.filter(product=product).order_by("date_created")
    make_review = True

    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()

        if user_review_count > 0:
            make_review = False

    context = {'product': product, 'products': products, 'reviews': reviews, 'make_review': make_review}
    return render(request, 'store/product_detail.html', context)


def ajax_add_review(request, pk):
    product = Product.objects.get(id=pk)
    user = request.user

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST.get('review'),

    )
    context = {
        'user': user.username,
        'review': request.POST.get('review'),

    }
    return JsonResponse(
        {
            'bool': True,
            'context': context,
        }
    )


def add_to_cart(request):
    cart_product = {}
    product_id = request.GET['id']
    print(product_id)
    print("what")

    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'id': request.GET['id'],
    }
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse(
        {"data": request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj']),
         'product_id': product_id})


def delete_from_cart(request):
    product_id = str(request.GET['id'])

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            total = cart_total_amount + 10
    context = render_to_string('store/cart_list.html', {"cart_data": request.session['cart_data_obj'],
                                                        "totalcartitems": len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount})
    return JsonResponse(
        {"data": context, "totalcartitems": len(request.session['cart_data_obj'])})


def cart_view(request):
    cart_total_amount = 0
    total = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            total = cart_total_amount + 10
        return render(request, 'store/cart.html', {"cart_data": request.session['cart_data_obj'],
                                                   "totalcartitems": len(request.session['cart_data_obj']),
                                                   'cart_total_amount': cart_total_amount, 'total': total,
                                                   })
    else:
        messages.warning(request, 'your cart is empty')
        return redirect("store:index")


def checkout_view(request):
    host = request.get_host()
    cart_total_amount = 0
    total_amount = 0

    if request.user.is_authenticated:
        user = request.user
    else:
        user = None


    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            total_amount += int(item['qty']) * float(item['price'])

        order = CartOrder.objects.create(
            user=user,
            price=total_amount,
        )

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

            cart_order_item = CartOrderItem.objects.create(
                order=order,
                invoice_no='INVOICE_NO' + str(order.id),
                item=item['title'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=int(item['qty']) * float(item['price']),

            )

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': cart_total_amount,
        'item_name': 'Order-Item-No-' + str(order.id),
        'invoice': 'INVOICE_NO-' + str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse("store:paypal-ipn")),
        'return_url': 'http://{}{}'.format(host, reverse("store:payment_completed")),
        'cancel_url': 'http://{}{}'.format(host, reverse("store:payment_failed")),
    }
    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            total = cart_total_amount + 10
    return render(request, 'store/checkout.html', {"cart_data": request.session['cart_data_obj'],
                                                   "totalcartitems": len(request.session['cart_data_obj']),
                                                   'cart_total_amount': cart_total_amount,
                                                   'paypal_payment_button': paypal_payment_button, 'total': total})


def payment_completed(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
            total = cart_total_amount + 10
    return render(request, 'store/payment_completed.html', {"cart_data": request.session['cart_data_obj'],
                                                            "totalcartitems": len(request.session['cart_data_obj']),
                                                            'cart_total_amount': cart_total_amount, 'total': total})


def payment_failed(request):
    return render(request, 'store/payment_failed.html')


def get_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        email = NewsletterSubscribers(
            email=email,
        )
        email.save()

    context = {
        'email': request.POST.get('email'),
    }
    return JsonResponse(
        {
            'context': context,
        }
    )


def shipping_address(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        country = request.POST.get('country')
        city = request.POST.get('city')
        state = request.POST.get('state')

        shippingaddress = ShippingAddress(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            mobile=request.POST.get('mobile'),
            address=request.POST.get('address'),
            country=request.POST.get('country'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
        )

        shippingaddress.save()

    context = {
        'first_name': request.POST.get('first_name'),
        'last_name': request.POST.get('last_name'),
        'email': request.POST.get('email'),
        'mobile': request.POST.get('mobile'),
        'address': request.POST.get('address'),
        'country': request.POST.get('country'),
        'city': request.POST.get('city'),
        'state': request.POST.get('state'),
    }
    return JsonResponse(
        {
            'context': context,
        }
    )


def get_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        email = request.POST.get('email')
        message = request.POST.get('message')

        contact = Contact(
            name=request.POST.get('name'),
            subject=request.POST.get('subject'),
            email=request.POST.get('email'),
            message=request.POST.get('message'),
        )

        contact.save()

    context = {
        'name': request.POST.get('name'),
        'subject': request.POST.get('subject'),
        'email': request.POST.get('email'),
        'message': request.POST.get('message'),
    }
    return JsonResponse(
        {
            'context': context,
        }
    )
