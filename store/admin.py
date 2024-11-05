from django.contrib import admin
from .models import *


# Register your models here.
class ProductImageAdmin(admin.TabularInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]
    list_display = ['user', 'name', 'image', 'price', 'feature', 'products_status']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'image']


class VendorAdmin(admin.ModelAdmin):
    list_display = ['name', 'image']


class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'price', 'paid_status', 'date_created', 'products_status']


class CartOrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'image', 'qty', 'price', 'total']


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date_created']


class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'status']



admin.site.register(Contact)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItem, CartOrderItemAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(WishList, WishlistAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(ShippingAddress)
