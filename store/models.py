from django.db import models
from userauths.models import User

# Create your models here.

STATUS_CHOICE = (
    ('Process', 'Processing'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
)

STATUS = (
    ('Draft', 'Draft'),
    ('Disabled', 'Disabled'),
    ('Rejected', 'Rejected'),
    ('In_review', 'In_review'),
    ('Published', 'Published'),
)

RATING = (
    ('1', '⭐☆☆☆☆'),
    ('2', '⭐⭐☆☆☆'),
    ('3', '⭐⭐⭐☆☆'),
    ('4', '⭐⭐⭐⭐☆'),
    ('5', '⭐⭐⭐⭐⭐'),
)



class Category(models.Model):
    name = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to='category/')

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


class Vendor(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to='vendor/')
    descriptions = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=20, null=True, default='123 main street')
    contact = models.CharField(max_length=20, null=True, default='+234 (345) 787')
    chat_rep_time = models.CharField(max_length=20, null=True, default='10')
    shipping_on_time = models.CharField(max_length=20, null=True, default='10')
    authentic_rating = models.CharField(max_length=20, null=True, default='10')
    days_return = models.CharField(max_length=20, null=True, default='10')
    warranty_period = models.CharField(max_length=20, null=True, default='10')

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Vendors"


class Tags(models.Model):
    pass


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to='products/')
    descriptions = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=1)
    old_price = models.DecimalField(max_digits=20, decimal_places=2)
    specifications = models.TextField(null=True, blank=True)
    tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True, blank=True)
    products_status = models.CharField(choices=STATUS, max_length=20, null=True)
    status = models.BooleanField(default=True, null=True, blank=True)
    in_stock = models.BooleanField(default=True, null=True, blank=True)
    feature = models.BooleanField(default=False, null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(null=True, blank=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "products"

    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    class Meta:
        verbose_name_plural = "product images"


class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=1)
    paid_status = models.BooleanField(default=False, null=True, blank=True)
    products_status = models.CharField(choices=STATUS_CHOICE, max_length=20, null=True, default='processing')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "cart order"


class CartOrderItem(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE, null=True)
    product_status = models.CharField(max_length=20, null=True)
    invoice_no = models.CharField(max_length=20, null=True)
    item = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to='products/')
    qty = models.IntegerField(default='0')
    price = models.DecimalField(max_digits=20, decimal_places=2)
    total = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        verbose_name_plural = "cart order items"


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "product review"


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "wishlist"


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=20, null=True)
    status = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Address"


class NewsletterSubscribers(models.Model):
    email = models.CharField(max_length=70, null=True)

    def __str__(self):
        return self.email


class ShippingAddress(models.Model):
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Contact(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=20, null=True, blank=True)
    subject = models.CharField(max_length=20, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
