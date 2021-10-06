from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'ordermanager'
urlpatterns = [
    path('', views.manage_index, name='order_index'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('vn/<int:order_id>/', views.order_detail_vn, name='order_detail_vn'),
    path('order/create/', views.order_create, name='order_create'),
    path('vn/order/create/', views.order_create_vn, name='order_create_vn'),
    path('order/modify/<int:order_id>/', views.order_modify, name='order_modify'),
    path('vn/order/modify/<int:order_id>/', views.order_modify_vn, name='order_modify_vn'),
    path('order/delete/<int:order_id>/', views.order_delete, name='order_delete'),
    path('vn/order/delete/<int:order_id>/', views.order_delete_vn, name='order_delete_vn'),
    path('actor/create/<int:order_id>/', views.actor_create, name='actor_create'),
    path('vn/actor/create/<int:order_id>/', views.actor_create_vn, name='actor_create_vn'),
    path('actor/modify/<int:actor_id>/', views.actor_modify, name='actor_modify'),
    path('vn/actor/modify/<int:actor_id>/', views.actor_modify_vn, name='actor_modify_vn'),
    path('actor/delete/<int:actor_id>/', views.actor_delete, name='actor_delete'),
    path('vn/actor/delete/<int:actor_id>/', views.actor_delete_vn, name='actor_delete_vn'),
    path('order/price_update/<int:order_id>', views.price_update, name='price_update'),
    path('opp/<str:user_id>', views.opp, name='opp'),
    path('order_list_bulkedit/', views.order_list_bulkedit, name='order_list_bulkedit'),
    path('order/order_confirm_modify/<int:order_id>', views.order_confirm_modify, name='order_confirm_modify'),
    path('bill/', views.bill_detail, name='bill_detail'),
    path('bill_csv', views.bill_csv, name='bill_csv'),
    path('receptionist/', views.receptionist, name='receptionist'),
]