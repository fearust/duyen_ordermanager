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
    list_display = ['name_kr', 'nickname_kr', 'selling', 'hide_product', 'add_date']
    inlines = [ProductImageInline,]


admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)
admin.site.register(Order, OrderAdmin)
admin.site.register(AccountSetting)