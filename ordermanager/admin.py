from django.contrib import admin
from ordermanager.models import Product, ProductImage, Customer, Order, OrderImage, Actor, AccountSetting


class OrderImageInline(admin.StackedInline):
    model = OrderImage


class ActorInline(admin.StackedInline):
    model = Actor


class ProductImageInline(admin.StackedInline):
    model = ProductImage


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_info']
    inlines = [OrderImageInline, ActorInline]

    def customer_info(self, post):
        if post.customer.name:
            name = post.customer.name
        else:
            name = 'none'
        if post.customer.phone:
            phone = post.customer.phone
        else:
            phone = 'none'
        return '{} - {}'.format(name, phone)
    customer_info.short_description = '고객'


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name_kr', 'nickname_kr', 'selling', 'hide_product', 'add_date']
    list_display_links = ['name_kr', 'nickname_kr']
    list_filter = ['selling', 'hide_product']
    actions = ['make_selling', 'make_unselling', 'make_hide', 'make_unhide']
    inlines = [ProductImageInline,]

    def make_selling(self, request, queryset):
        updated_count = queryset.update(selling=True)  # queryset.update
        self.message_user(request, '{}건의 상품을 판매중 상태로 변경'.format(updated_count))  # django message framework 활용
    make_selling.short_description = '지정 상품을 판매중 상태로 변경'

    def make_unselling(self, request, queryset):
        updated_count = queryset.update(selling=False)  # queryset.update
        self.message_user(request, '{}건의 상품을 판매중단 상태로 변경'.format(updated_count))  # django message framework 활용
    make_unselling.short_description = '지정 상품을 판매중단 상태로 변경'

    def make_hide(self, request, queryset):
        updated_count = queryset.update(hide_product=True)  # queryset.update
        self.message_user(request, '{}건의 상품을 시스템에서 숨김 상태로 변경'.format(updated_count))  # django message framework 활용
    make_hide.short_description = '지정 상품을 시스템에서 숨김 상태로 변경'

    def make_unhide(self, request, queryset):
        updated_count = queryset.update(hide_product=False)  # queryset.update
        self.message_user(request, '{}건의 상품을 시스템에서 숨김해제 상태로 변경'.format(updated_count))  # django message framework 활용
    make_unhide.short_description = '지정 상품을 시스템에서 숨김해제 상태로 변경'


admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)
admin.site.register(Order, OrderAdmin)
admin.site.register(AccountSetting)