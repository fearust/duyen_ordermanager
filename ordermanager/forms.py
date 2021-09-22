from django import forms
from ordermanager.models import Customer, Order, Actor, AccountSetting

# 주문 관련 폼


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone', 'name', 'facebook_url',
                  'bank_depositor', 'bank_refund',
                  'postcode', 'addr', 'detail_addr', 'extra_addr',
                  'description']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'quantity', 'size',
                  'confirm_transit', 'confirm_cancel', 'confirm_watch',
                  'receptionist_memo', 'order_addr',
                  'buying_url', 'buying_price', 'selling_price']
        # order_date, modify_date, receptionist, 'product' 는 view에서 별도 지정

class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = ['actor_memo']

class OppForm(forms.ModelForm):
    class Meta:
        model = AccountSetting
        fields = ['order_per_page']