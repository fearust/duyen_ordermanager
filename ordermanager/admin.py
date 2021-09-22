from django.contrib import admin
from ordermanager.models import Product, ProductImage, Customer, Order, OrderImage, Actor, AccountSetting


class OrderImageInline(admin.StackedInline):
    model = OrderImage


class ActorInline(admin.StackedInline):
    model = Actor


class ProductImageInline(admin.StackedInline):
    model = ProductImage


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderImageInline,
               ActorInline]


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline,]


admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)
admin.site.register(Order, OrderAdmin)
admin.site.register(AccountSetting)