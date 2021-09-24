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
    list_display_links = ['name_kr', 'nickname_kr']
    list_filter = ['selling', 'hide_product']
    inlines = [ProductImageInline,]

    def make_published(self, request, queryset):
        updated_count = queryset.update(selling=True)  # queryset.update
        self.message_user(request, '{}건의 상품을 판매중 상태로 변경'.format(updated_count))  # django message framework 활용
    make_published.short_description = '지정 상품을 판매중 상태로 변경'

    def make_draft(self, request, queryset):
        updated_count = queryset.update(selling=False)  # queryset.update
        self.message_user(request, '{}건의 상품을 판매중단 상태로 변경'.format(updated_count))  # django message framework 활용
    make_draft.short_description = '지정 상품을 판매중단 상태로 변경'


admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)
admin.site.register(Order, OrderAdmin)
admin.site.register(AccountSetting)