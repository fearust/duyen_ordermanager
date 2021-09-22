from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'ordermanager'
urlpatterns = [
    path('', views.manage_index, name='order_index'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/create/', views.order_create, name='order_create'),
    path('order/modify/<int:order_id>/', views.order_modify, name='order_modify'),
    path('order/delete/<int:order_id>/', views.order_delete, name='order_delete'),
    path('actor/create/<int:order_id>/', views.actor_create, name='actor_create'),
    path('actor/modify/<int:actor_id>/', views.actor_modify, name='actor_modify'),
    path('actor/delete/<int:actor_id>/', views.actor_delete, name='actor_delete'),
    path('order/price_update/<int:order_id>', views.price_update, name='price_update'),
    # path('phonefind/', views.phone_find, name='phone_find'),
    path('productfind/', views.product_find, name='product_find'),
    path('opp/<str:user_id>', views.opp, name='opp'),
    path('order_list_bulkedit/', views.order_list_bulkedit, name='order_list_bulkedit'),
    path('order/order_confirm_modify/<int:order_id>', views.order_confirm_modify, name='order_confirm_modify'),
    path('bill/', views.bill_detail, name='bill_detail'),
    path('bill_csv', views.bill_csv, name='bill_csv'),
    path('receptionist/', views.receptionist, name='receptionist'),
]