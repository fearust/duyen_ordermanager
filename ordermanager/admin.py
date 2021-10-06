from django.contrib import admin
from ordermanager.models import Order, OrderImage, Actor, AccountSetting, PhoneTag, ProductTag
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter


class OrderImageInline(admin.StackedInline):
    model = OrderImage
    extra = 1


class ActorInline(admin.StackedInline):
    model = Actor
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_info', 'order_info', 'selling_info',
                    'confirm_transit', 'confirm_watch', 'confirm_cancel',
                    'order_date']
    list_display_links = ['id', 'customer_info', 'order_info', 'selling_info',]
    list_filter = [('order_date', DateRangeFilter), 'confirm_transit', 'confirm_watch', 'confirm_cancel']
    actions = ['make_transit', 'make_untransit', 'make_watch', 'make_unwatch', 'make_cancel', 'make_uncancel']
    inlines = [OrderImageInline, ActorInline]
    list_per_page = 100

    def customer_info(self, post):
        if post.customer:
            name = post.customer
        else:
            name = '없음'
        if post.phone.all().count() > 0:
            phone = ', '.join(phone.name for phone in post.phone.all())
        else:
            phone = '없음'
        return '{} - {}'.format(name, phone)
    customer_info.short_description = '고객'

    def order_info(self, post):
        if post.product.all().count() > 0:
            name = ', '.join(product.name for product in post.product.all())
        else:
            name = '없음'
        if post.quantity:
            quantity = post.quantity
        else:
            quantity = '?'
        if post.size:
            size = post.size
        else:
            size = '?'
        return '{}/개수:{}/사이즈:{}'.format(name, quantity, size)
    order_info.short_description = '주문정보'

    def selling_info(self, post):
        if post.buying_price:
            buying_price = post.buying_price
        else:
            buying_price = 'X'
        if post.selling_price:
            selling_price = post.selling_price
        else:
            selling_price = 'X'
        return '{} / {}'.format(buying_price, selling_price)
    selling_info.short_description = '구매가,판매가'

    def make_transit(self, request, queryset):
        updated_count = queryset.update(confirm_transit=True)  # queryset.update
        self.message_user(request, '{}건의 주문을 입금확인 상태로 변경'.format(updated_count))  # django message framework 활용
    make_transit.short_description = '지정 주문을 입금확인 상태로 변경'

    def make_untransit(self, request, queryset):
        updated_count = queryset.update(confirm_transit=False)  # queryset.update
        self.message_user(request, '{}건의 주문을 입금미확인 상태로 변경'.format(updated_count))  # django message framework 활용
    make_untransit.short_description = '지정 주문을 입금미확인 상태로 변경'

    def make_watch(self, request, queryset):
        updated_count = queryset.update(confirm_watch=True)  # queryset.update
        self.message_user(request, '{}건의 주문을 유의사항으로 추가'.format(updated_count))  # django message framework 활용
    make_watch.short_description = '지정 주문을 유의사항으로 추가'

    def make_unwatch(self, request, queryset):
        updated_count = queryset.update(confirm_watch=False)  # queryset.update
        self.message_user(request, '{}건의 주문을 유의사항에서 제외'.format(updated_count))  # django message framework 활용
    make_unwatch.short_description = '지정 주문을 유의사항에서 제외'

    def make_cancel(self, request, queryset):
        updated_count = queryset.update(confirm_cancel=True)  # queryset.update
        self.message_user(request, '{}건의 주문을 주문취소 상태로 변경'.format(updated_count))  # django message framework 활용
    make_cancel.short_description = '지정 주문을 주문취소 상태로 변경'

    def make_uncancel(self, request, queryset):
        updated_count = queryset.update(confirm_cancel=False)  # queryset.update
        self.message_user(request, '{}건의 주문을 주문취소 상태 해제'.format(updated_count))  # django message framework 활용
    make_uncancel.short_description = '지정 주문을 주문취소 상태 해제'


class AccountSettingAdmin(admin.ModelAdmin):
    list_display = ['user', 'order_per_page']
    list_per_page = 100


admin.site.register(Order, OrderAdmin)
admin.site.register(AccountSetting, AccountSettingAdmin)
admin.site.register(PhoneTag)
admin.site.register(ProductTag)