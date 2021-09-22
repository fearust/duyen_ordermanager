from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q, Sum, Count
from django.http import HttpResponse
import json
import csv
import mimetypes
from urllib import parse
from django.core.serializers.json import DjangoJSONEncoder
from ordermanager.models import Product, Order, OrderImage, Actor, AccountSetting, Customer
from .forms import OrderForm, CustomerForm, ActorForm, OppForm


@login_required(login_url='common:login')
def manage_index(request):
    userdb = User.objects.all()
    productdb = Product.objects.exclude(hide_product=True)
    # customerdb = Customer.objects.exclude(name=None)
    # customerphonedb = Customer.objects.exclude(phone=None).distinct()
    current_user = request.user


    page = request.GET.get('page', '1')
    customer_phone = request.GET.get('customer_phone', '')
    customer_name = request.GET.get('customer_name', '')
    product_nickname_kr = request.GET.get('product_nickname_kr', '')
    order_receptionist = request.GET.get('order_receptionist', '')
    order_actor = request.GET.get('order_actor', '')
    qstart = request.GET.get('Qstart', '')
    qend = request.GET.get('Qend', '')
    pkstart = request.GET.get('pkstart', '')
    pkend = request.GET.get('pkend', '')
    check_confirm_transit = request.GET.get('check_confirm_transit', '')
    check_confirm_transit_cancel = request.GET.get('check_confirm_transit_cancel', '')
    check_confirm_cancel = request.GET.get('check_confirm_cancel', '')
    check_confirm_watch = request.GET.get('check_confirm_watch', '')
    check_blacklist = request.GET.get('check_blacklist', '')

    order_list = Order.objects.all().order_by('-confirm_watch', '-order_date', '-id')

    if customer_phone:
        order_list = order_list.filter(Q(customer__phone__icontains=customer_phone)).distinct()
    if customer_name:
        order_list = order_list.filter(Q(customer__name__icontains=customer_name)).distinct()
    if product_nickname_kr:
        order_list = order_list.filter(Q(product__nickname_kr__icontains=product_nickname_kr)).distinct()
    if order_receptionist:
        order_list = order_list.filter(Q(receptionist__username__icontains=order_receptionist)).distinct()
    if order_actor:
        order_list = order_list.filter(Q(buying_actor__username__icontains=order_actor)).distinct()
    if qstart:
        order_list = order_list.filter(Q(order_date__gte=qstart)).distinct()
    if qend:
        order_list = order_list.filter(Q(order_date__lte=qend)).distinct()
    if pkstart:
        order_list = order_list.filter(Q(id__gte=pkstart)).distinct()
    if pkend:
        order_list = order_list.filter(Q(id__lte=pkend)).distinct()
    if check_confirm_transit == '1':
        order_list = order_list.filter(Q(confirm_transit=True)).distinct()
        if check_confirm_transit_cancel == '1':
            order_list = order_list.exclude(confirm_cancel=True).distinct()
    elif check_confirm_transit == '0':
        order_list = order_list.filter(Q(confirm_transit=False)).distinct()
        if check_confirm_transit_cancel == '1':
            order_list = order_list.exclude(confirm_cancel=True).distinct()
    if check_confirm_cancel == '1':
        order_list = order_list.filter(Q(confirm_cancel=True)).distinct()
    if check_confirm_watch == '1':
        order_list = order_list.filter(Q(confirm_watch=True)).distinct()
    if check_blacklist == '1':
        order_list = order_list.filter(Q(customer__blacklist=True)).distinct()

    # 페이지당 오브젝트 갯수 설정

    object_per_page = 10
    oppsetting = 10
    if request.user.is_authenticated and AccountSetting.objects.filter(user=request.user).exists():
        object_per_page = AccountSetting.objects.get(user=request.user).order_per_page
        oppsetting = object_per_page
    elif request.user.is_authenticated:
        account_setting_create = AccountSetting(user=request.user, order_per_page=10)
        account_setting_create.save()
    else:
        object_per_page = 10
        oppsetting = 10

    # 페이지 나누기
    paginator = Paginator(order_list, object_per_page)
    page_obj = paginator.get_page(page)

    context = {
        'order_list': page_obj,
        'page': page,
        'object_per_page': object_per_page,
        'userdb': userdb,
        'productdb': productdb,
        'customer_phone': customer_phone, 'customer_name': customer_name,
        'product_nickname_kr': product_nickname_kr,
        'order_receptionist': order_receptionist, 'order_actor': order_actor,
        'Qstart': qstart, 'Qend': qend, 'pkstart': pkstart, 'pkend': pkend,
        'check_confirm_transit': check_confirm_transit,
        'check_confirm_transit_cancel': check_confirm_transit_cancel,
        'check_confirm_cancel': check_confirm_cancel,
        'check_confirm_watch': check_confirm_watch,
        'check_blacklist': check_blacklist,
        'current_user': current_user,
        'oppsetting': oppsetting,
    }
    ## 'customerdb': customerdb,
    ## 'customerphonedb': customerphonedb,

    return render(request, 'ordermanager/order_list.html', context)


@login_required(login_url='common:login')
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    buying_price = order.buying_price
    selling_price = order.selling_price
    buying_actor = order.buying_actor
    context = {'order': order, 'buying_price': buying_price, 'selling_price': selling_price, 'buying_actor': buying_actor}
    return render(request, 'ordermanager/order_detail.html', context)


@login_required(login_url='common:login')
def order_create(request):
    # customerdb = Customer.objects.exclude(phone=None).distinct()
    productdb = Product.objects.filter(Q(selling=True) & Q(hide_product=False))
    if request.method == 'POST':
        customerform = CustomerForm(request.POST)
        orderform = OrderForm(request.POST)
        product_name = request.POST.get('product', '')
        product_id = Product.objects.get(name_kr=product_name)

        if customerform.is_valid() and orderform.is_valid():
            customerquestion = customerform.save(commit=False)
            customerquestion.save()
            orderquestion = orderform.save(commit=False)
            orderquestion.product = product_id
            orderquestion.customer = customerquestion
            orderquestion.order_date = timezone.now()
            orderquestion.receptionist = request.user
            orderquestion.save()

            for img in request.FILES.getlist('imgs'):
                photo = OrderImage()
                photo.order = orderquestion
                photo.image = img
                photo.save()

            return redirect('ordermanager:order_index')
    else:
        customerform = CustomerForm()
        orderform = OrderForm()
    context = {'customerform': customerform, 'orderform': orderform, 'productdb': productdb}  # 'customerdb': customerdb, 제외
    return render(request, 'ordermanager/order_form.html', context)


@login_required(login_url='common:login')
def order_modify(request, order_id):
    # customerdb = Customer.objects.exclude(phone=None).distinct()
    productdb = Product.objects.filter(selling=True)
    order = get_object_or_404(Order, pk=order_id)
    if not request.user.is_staff:
        messages.error(request, '수정권한이 없습니다')
        return redirect('ordermanager:order_detail', order_id=order.id)
    if request.method == 'POST':
        customerform = CustomerForm(request.POST, instance=order.customer)
        orderform = OrderForm(request.POST, instance=order)
        if customerform.is_valid() and orderform.is_valid():
            customerquestion = customerform.save(commit=False)
            customerquestion.save()
            orderquestion = orderform.save(commit=False)
            orderquestion.customer = customerquestion
            orderquestion.modify_date = timezone.now()
            orderquestion.receptionist = request.user
            orderquestion.save()
            for img in request.FILES.getlist('imgs'):
                photo = OrderImage()
                photo.order = orderquestion
                photo.image = img
                photo.save()
            return redirect('ordermanager:order_detail', order_id=order.id)
    else:
        customerform = CustomerForm(instance=order.customer)
        orderform = OrderForm(instance=order)
    context = {'order': order, 'customerform': customerform, 'orderform': orderform, 'productdb': productdb}  # 'customerdb': customerdb, 제외
    return render(request, 'ordermanager/order_form.html', context)


@login_required(login_url='common:login')
def order_delete(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.user == order.receptionist or request.user.is_superuser:
        order.delete()
    else:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('ordermanager:order_detail', order_id=order.id)
    return redirect('ordermanager:order_index')

@login_required(login_url='common:login')
def actor_create(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == "POST":
        form = ActorForm(request.POST)
        if form.is_valid():
            actor = form.save(commit=False)
            actor.actor_date = timezone.now()
            actor.actor = request.user
            actor.order = order
            actor.save()
            return redirect('ordermanager:order_detail', order_id=order.id)
    else:
        form = ActorForm()
    context = {'order': order, 'form': form, }
    return redirect('ordermanager:order_detail', context)


@login_required(login_url='common:login')
def actor_modify(request, actor_id):
    actor = get_object_or_404(Actor, pk=actor_id)
    if request.user == actor.actor or request.user.is_superuser:
        pass
    else:
        messages.error(request, '수정권한이 없습니다')
        return redirect('ordermanager:order_detail', order_id=actor.order.id)

    if request.method == "POST":
        form = ActorForm(request.POST, instance=actor)
        if form.is_valid():
            actor = form.save(commit=False)
            actor.modify_date = timezone.now()
            actor.save()
            return redirect('ordermanager:order_detail', order_id=actor.order.id)
    else:
        form = ActorForm(instance=actor)
    context = {'actor': actor, 'form': form}
    return render(request, 'ordermanager/actor_form.html', context)


@login_required(login_url='common:login')
def actor_delete(request, actor_id):
    actor = get_object_or_404(Actor, pk=actor_id)
    if request.user == actor.actor or request.user.is_superuser:
        actor.delete()
    else:
        messages.error(request, '삭제권한이 없습니다')
    return redirect('ordermanager:order_detail', order_id=actor.order.id)


def phone_find(request):
    if request.method == 'GET' and request.is_ajax():
        phone_id = request.GET.get('phone', None)
        req2 = Customer.objects.filter(phone=phone_id).values()
        data = json.dumps(list(req2))
        return HttpResponse(data)
    else:
        return HttpResponse(json.dumps({'error': 'HTTP Method error'}))


def product_find(request):
    if request.method == 'GET' and request.is_ajax():
        product_id = request.GET.get('product', None)
        req2 = Product.objects.filter(pk=product_id).values()
        data = json.dumps(list(req2), cls=DjangoJSONEncoder)
        return HttpResponse(data)
    else:
        return HttpResponse(json.dumps({'error': 'HTTP Method error'}))


@login_required(login_url='common:login')
def opp(request, user_id):
    userpk = User.objects.get(username=user_id)
    user = get_object_or_404(AccountSetting, user=userpk)

    if request.method == "POST":
        form = OppForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('ordermanager:order_index')

    return render(request, 'ordermanager/order_list.html')

@login_required(login_url='common:login')
def order_list_bulkedit(request):
    if request.method == "POST":
        selected_values = request.POST.getlist('order_list_check')
        for_change = Order.objects.filter(id__in=selected_values)
        if for_change.exists():
            if 'do_transit' in request.POST:
                for_change.update(confirm_transit=True)
            elif 'do_untransit' in request.POST:
                for_change.update(confirm_transit=False)
            elif 'do_watch' in request.POST:
                for_change.update(confirm_watch=True)
            elif 'do_unwatch' in request.POST:
                for_change.update(confirm_watch=False)
            elif 'do_cancel' in request.POST:
                for_change.update(confirm_cancel=True)
            elif 'do_uncancel' in request.POST:
                for_change.update(confirm_cancel=False)
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='common:login')
def price_update(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.user != order.receptionist and not request.user.is_staff:
        messages.error(request, '수정권한이 없습니다')
        return redirect('ordermanager:order_detail', order_id=order.id)
    if request.method == "POST":
        buying_price = request.POST.get('buying_price', '')
        selling_price = request.POST.get('selling_price', '')
        order.buying_price = buying_price
        order.selling_price = selling_price
        order.buying_actor = request.user
        order.save()
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='common:login')
def order_confirm_modify(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.user != order.receptionist and not request.user.is_staff:
        messages.error(request, '수정권한이 없습니다')
        return redirect('ordermanager:order_detail', order_id=order.id)
    if request.method == "POST":
        if 'do_transit' in request.POST:
            if order.confirm_transit:
                order.confirm_transit = False
            else:
                order.confirm_transit = True
            order.save()
        elif 'do_watch' in request.POST:
            if order.confirm_watch:
                order.confirm_watch = False
            else:
                order.confirm_watch = True
            order.save()
        elif 'do_cancel' in request.POST:
            if order.confirm_cancel:
                order.confirm_cancel = False
            else:
                order.confirm_cancel = True
            order.save()
    return redirect(request.META['HTTP_REFERER'])



@user_passes_test(lambda u: u.is_superuser)
def bill_detail(request):
    userdb = User.objects.all()
    productdb = Product.objects.all()
    # customerdb = Customer.objects.exclude(name=None)
    # customerphonedb = Customer.objects.exclude(phone=None).distinct()
    current_user = request.user
    oppsetting = AccountSetting.objects.get(user=request.user).order_per_page

    page = request.GET.get('page', '1')
    customer_phone = request.GET.get('customer_phone', '')
    customer_name = request.GET.get('customer_name', '')
    product_nickname_kr = request.GET.get('product_nickname_kr', '')
    order_receptionist = request.GET.get('order_receptionist', '')
    order_actor = request.GET.get('order_actor', '')
    qstart = request.GET.get('Qstart', '')
    qend = request.GET.get('Qend', '')
    pkstart = request.GET.get('pkstart', '')
    pkend = request.GET.get('pkend', '')
    check_confirm_transit = request.GET.get('check_confirm_transit', '')
    check_confirm_watch = request.GET.get('check_confirm_watch', '')
    check_blacklist = request.GET.get('check_blacklist', '')

    order_list = Order.objects.all().order_by('-order_date', '-id')
    order_list = order_list.exclude(confirm_cancel=True).distinct()

    if customer_phone:
        order_list = order_list.filter(Q(customer__phone__icontains=customer_phone)).distinct()
    if customer_name:
        order_list = order_list.filter(Q(customer__name__icontains=customer_name)).distinct()
    if product_nickname_kr:
        order_list = order_list.filter(Q(product__nickname_kr__icontains=product_nickname_kr)).distinct()
    if order_receptionist:
        order_list = order_list.filter(Q(receptionist__username__icontains=order_receptionist)).distinct()
    if order_actor:
        order_list = order_list.filter(Q(buying_actor__username__icontains=order_actor)).distinct()
    if qstart:
        order_list = order_list.filter(Q(order_date__gte=qstart)).distinct()
    if qend:
        order_list = order_list.filter(Q(order_date__lte=qend)).distinct()
    if pkstart:
        order_list = order_list.filter(Q(id__gte=pkstart)).distinct()
    if pkend:
        order_list = order_list.filter(Q(id__lte=pkend)).distinct()
    if check_confirm_transit == '1':
        order_list = order_list.filter(Q(confirm_transit=True)).distinct()
    elif check_confirm_transit == '0':
        order_list = order_list.filter(Q(confirm_transit=False)).distinct()
    if check_confirm_watch == '1':
        order_list = order_list.filter(Q(confirm_watch=True)).distinct()
    if check_blacklist == '1':
        order_list = order_list.filter(Q(customer__blacklist=True)).distinct()

    benefit_byproduct_list = {}
    benefit_bydays_list = {}
    order_list_firstday = datetime.now()
    order_list_lastday = datetime.now()
    benefit_all_list = []

    if order_list.exists():

        for product in Product.objects.all():
            try:
                byproduct = order_list.filter(product__name_kr__icontains=product.name_kr)
                byproduct_count = list(byproduct.aggregate(Count('pk')).values())[0]
                byproduct_buying_sum = list(byproduct.aggregate(Sum('buying_price')).values())[0]
                byproduct_selling_sum = list(byproduct.aggregate(Sum('selling_price')).values())[0]
                byproduct_benefit_sum = byproduct_selling_sum - byproduct_buying_sum
                if byproduct_count and byproduct_benefit_sum > 0:
                    benefit_byproduct_list[product.name_kr] = (byproduct_count, byproduct_buying_sum, byproduct_selling_sum, byproduct_benefit_sum)
            except:
                pass

        if order_list.exists():
            order_list_firstday = order_list.last().order_date
            order_list_lastday = order_list.first().order_date
            order_list_diffday = order_list_lastday - order_list_firstday
            start_day = order_list_firstday.date()
            for i in range(order_list_diffday.days):
                end_day = start_day + timedelta(days=1)
                bydays = order_list.filter(Q(order_date__gte=start_day) & Q(order_date__lte=end_day))
                try:
                    bydays_count = list(bydays.aggregate(Count('pk')).values())[0]
                    bydays_buying_sum = list(bydays.aggregate(Sum('buying_price')).values())[0]
                    bydays_selling_sum = list(bydays.aggregate(Sum('selling_price')).values())[0]
                    bydays_benefit_sum = bydays_selling_sum - bydays_buying_sum
                    if bydays_count and bydays_benefit_sum > 0:
                        benefit_bydays_list[start_day] = (bydays_count, bydays_buying_sum, bydays_selling_sum, bydays_benefit_sum)
                except:
                    pass
                start_day = end_day

        all_order_count = list(order_list.aggregate(Count('pk')).values())[0]
        buying_sum = list(order_list.aggregate(Sum('buying_price')).values())[0]
        selling_sum = list(order_list.aggregate(Sum('selling_price')).values())[0]
        benefit_sum = selling_sum - buying_sum
        if selling_sum > 0:
            benefit_all_list = [all_order_count, buying_sum, selling_sum, benefit_sum]

    # 페이지당 오브젝트 갯수 설정
    object_per_page = 50

    # 페이지 나누기
    paginator = Paginator(order_list, object_per_page)
    page_obj = paginator.get_page(page)



    context = {
        'order_list': page_obj,
        'page': page,
        'object_per_page': object_per_page,
        'userdb': userdb,
        'productdb': productdb,
        'customer_phone': customer_phone, 'customer_name': customer_name,
        'product_nickname_kr': product_nickname_kr,
        'order_receptionist': order_receptionist, 'order_actor': order_actor,
        'Qstart': qstart, 'Qend': qend, 'pkstart': pkstart, 'pkend': pkend,
        'check_confirm_transit': check_confirm_transit,
        'check_confirm_watch': check_confirm_watch,
        'check_blacklist': check_blacklist,
        'current_user': current_user,
        'oppsetting': oppsetting,
        'benefit_byproduct_list': benefit_byproduct_list, 'benefit_bydays_list': benefit_bydays_list,
        'benefit_all_list': benefit_all_list,
        'order_list_firstday': order_list_firstday, 'order_list_lastday': order_list_lastday
    }
    # 'customerdb': customerdb,
    # 'customerphonedb': customerphonedb,

    return render(request, 'ordermanager/bill_detail.html', context)

@user_passes_test(lambda u: u.is_superuser)
def bill_csv(request):
    userdb = User.objects.all()
    productdb = Product.objects.all()
    current_user = request.user

    customer_phone = request.POST.get('customer_phone', '')
    customer_name = request.POST.get('customer_name', '')
    product_nickname_kr = request.POST.get('product_nickname_kr', '')
    order_receptionist = request.POST.get('order_receptionist', '')
    order_actor = request.POST.get('order_actor', '')
    qstart = request.POST.get('Qstart', '')
    qend = request.POST.get('Qend', '')
    pkstart = request.POST.get('pkstart', '')
    pkend = request.POST.get('pkend', '')
    check_confirm_transit = request.POST.get('check_confirm_transit', '')
    check_confirm_watch = request.POST.get('check_confirm_watch', '')
    check_blacklist = request.POST.get('check_blacklist', '')

    order_list = Order.objects.all().order_by('order_date', 'id')
    order_list = order_list.exclude(confirm_cancel=True).distinct()

    filename_txt = ''
    if customer_phone:
        order_list = order_list.filter(Q(customer__phone__icontains=customer_phone)).distinct()
        filename_txt += ''.join(['전화(', customer_phone, ')_'])
    if customer_name:
        order_list = order_list.filter(Q(customer__name__icontains=customer_name)).distinct()
        filename_txt += ''.join(['이름(', customer_name, ')_'])
    if product_nickname_kr:
        order_list = order_list.filter(Q(product__nickname_kr__icontains=product_nickname_kr)).distinct()
        filename_txt += ''.join(['상품명(', product_nickname_kr, ')_'])
    if order_receptionist:
        order_list = order_list.filter(Q(receptionist__username__icontains=order_receptionist)).distinct()
        filename_txt += ''.join(['접수자(', order_receptionist, ')_'])
    if order_actor:
        order_list = order_list.filter(Q(buying_actor__username__icontains=order_actor)).distinct()
        filename_txt += ''.join(['대행자(', order_actor, ')_'])
    if qstart:
        order_list = order_list.filter(Q(order_date__gte=qstart)).distinct()
        filename_txt += ''.join(['시작일(', qstart, ')_'])
    if qend:
        order_list = order_list.filter(Q(order_date__lte=qend)).distinct()
        filename_txt += ''.join(['종료일(', qend, ')_'])
    if pkstart:
        order_list = order_list.filter(Q(id__gte=pkstart)).distinct()
        filename_txt += ''.join(['시작번호(', pkstart, ')_'])
    if pkend:
        order_list = order_list.filter(Q(id__lte=pkend)).distinct()
        filename_txt += ''.join(['마지막번호(', pkend, ')_'])
    if check_confirm_transit == '1':
        order_list = order_list.filter(Q(confirm_transit=True)).distinct()
        filename_txt += ''.join(['입금완료건_'])
    elif check_confirm_transit == '0':
        order_list = order_list.filter(Q(confirm_transit=False)).distinct()
        filename_txt += ''.join(['미입금건_'])
    if check_confirm_watch == '1':
        order_list = order_list.filter(Q(confirm_watch=True)).distinct()
        filename_txt += ''.join(['유의건_'])
    if check_blacklist == '1':
        order_list = order_list.filter(Q(customer__blacklist=True)).distinct()
        filename_txt += ''.join(['블랙리스트건_'])

    filename_txt += '.csv'
    filename_txt_utf8 = parse.quote(filename_txt.encode('utf-8'))

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % filename_txt_utf8
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(['no', '일자', '주문자', '연락처', '주소', '항목', '수량', '사이즈', '구입가', '판매가'])
    for order in order_list:
        writer.writerow([
            order.pk, order.order_date, order.customer.name, order.customer.phone, order.order_addr,
            ''.join([order.product.name_kr, '(', order.product.nickname_kr, ')']),
            order.quantity, order.size, order.buying_price, order.selling_price
        ])

    return response

@login_required(login_url='common:login')
def receptionist(request):
    productdb = Product.objects.filter(Q(selling=True) & Q(hide_product=False))
    page = request.GET.get('page', '1')
    current_user = request.user
    object_per_page = 10
    order_list = Order.objects.filter(Q(confirm_watch=True) | Q(receptionist=current_user)).order_by('-confirm_watch', '-order_date', '-id')
    paginator = Paginator(order_list, object_per_page)
    page_obj = paginator.get_page(page)

    if request.method == 'POST':
        customerform = CustomerForm(request.POST)
        orderform = OrderForm(request.POST)
        product_name = request.POST.get('product', '')
        product_id = Product.objects.get(name_kr=product_name)

        if customerform.is_valid() and orderform.is_valid():
            customerquestion = customerform.save(commit=False)
            customerquestion.save()
            orderquestion = orderform.save(commit=False)
            orderquestion.product = product_id
            orderquestion.customer = customerquestion
            orderquestion.order_date = timezone.now()
            orderquestion.receptionist = request.user
            orderquestion.save()

            for img in request.FILES.getlist('imgs'):
                photo = OrderImage()
                photo.order = orderquestion
                photo.image = img
                photo.save()

            return redirect('ordermanager:receptionist')
    else:
        customerform = CustomerForm()
        orderform = OrderForm()

    context = {'order_list': page_obj, 'productdb': productdb, 'customerform': customerform, 'orderform': orderform}
    return render(request, 'ordermanager/receptionist_list.html', context)