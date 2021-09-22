from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill
from simplemde.fields import SimpleMDEField
from django.conf import settings


class Product(models.Model):
    name_kr = models.CharField('품명(한국어)', max_length=500)
    name_vn = models.CharField('품명(베트남어)', max_length=500, blank=True, null=True)
    nickname_kr = models.CharField('닉네임(한국어)', max_length=500)
    nickname_vn = models.CharField('닉네임(베트남어)', max_length=500, blank=True, null=True)
    selling = models.BooleanField('판매여부', default=False)
    hide_product = models.BooleanField('시스템에서 숨기기', default=False)
    description = models.TextField('상품설명', blank=True, null=True)
    add_date = models.DateField('상품등록일', auto_now_add=True)

    def __str__(self):
        return self.nickname_kr
    # 대표 이름을 닉네임으로 설명


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    # 이미지 수정 및 업로드 경로 설정
    image = ProcessedImageField(verbose_name='상품이미지',
                                upload_to='product/%Y/%m/',
                                processors=[ResizeToFit(2400, 2400)],
                                format='JPEG',
                                options={'quality': 80},
                                blank=True,
                                null=True)
    # 썸네일용 이미지 생성
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(1000, 1000)],
                                     format='JPEG')
    image_thumbnail_fit = ImageSpecField(source='image',
                                     processors=[ResizeToFit(1000, 1000)],
                                     format='JPEG')


class Customer(models.Model):
    phone = models.CharField('전화번호', max_length=100, blank=True, null=True)
    name = models.CharField('고객 이름', max_length=100, blank=True, null=True)
    facebook_url = models.URLField('페이스북 프로필 링크', max_length=500, blank=True, null=True)
    bank_depositor = models.CharField('별도입금자명', max_length=100, blank=True, null=True)
    bank_refund = models.CharField('환불계좌정보', max_length=200, blank=True, null=True)
    postcode = models.CharField('우편번호', max_length=10, blank=True, null=True)
    addr = models.CharField('기본주소', max_length=500, blank=True, null=True)
    detail_addr = models.CharField('상세주소', max_length=500, blank=True, null=True)
    extra_addr = models.CharField('참고주소', max_length=500, blank=True, null=True)
    description = models.TextField('고객 메모', blank=True, null=True)
    blacklist = models.BooleanField('블랙리스트', default=False)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    backup_order_info = models.CharField('주문정보백업', max_length=200, blank=True, null=True)
    order_date = models.DateTimeField('주문시간')
    modify_date = models.DateTimeField('수정시간', null=True, blank=True)
    quantity = models.IntegerField('수량')
    size = models.CharField('사이즈', max_length=200, blank=True, null=True)
    confirm_transit = models.BooleanField('입금확인', default=False)
    confirm_cancel = models.BooleanField('주문취소', default=False)
    confirm_watch = models.BooleanField('유의항목', default=False)
    receptionist = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='receptionist')
    receptionist_memo = SimpleMDEField('접수자메모', blank=True, null=True)
    order_addr = models.CharField('주문건주소', max_length=100, blank=True, null=True)
    buying_actor = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='buying_actor')
    buying_url = models.URLField('대행자 구매링크', max_length=500, blank=True, null=True)
    buying_price = models.IntegerField('구매가', default=0)
    selling_price = models.IntegerField('판매가', default=0)
    # def __str__(self): return self.name


class OrderImage(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    image = ProcessedImageField(verbose_name='주문이미지',
                                upload_to='order/%Y/%m/',
                                processors=[ResizeToFit(2400, 2400)],
                                format='JPEG',
                                options={'quality': 80},
                                blank=True,
                                null=True)

class Actor(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    actor_memo = SimpleMDEField('대행자 메모', blank=True, null=True)
    actor_date = models.DateTimeField('등록시간')
    modify_date = models.DateTimeField('수정시간', null=True, blank=True)


class AccountSetting(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_per_page = models.IntegerField('페이지당게시글수', default=10)