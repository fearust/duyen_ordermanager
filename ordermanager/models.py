from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from simplemde.fields import SimpleMDEField
from django.conf import settings
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase

class PhoneTag(TagBase):
    slug = models.SlugField(
        verbose_name='slug',
        unique=True,
        max_length=100,
        allow_unicode=True,
    )
    class Meta:
        verbose_name = "전화번호"
        verbose_name_plural = "전화번호"

    def slugify(self, tag, i=None):
        return slugify(tag, allow_unicode=True)

class ProductTag(TagBase):
    slug = models.SlugField(
        verbose_name='slug',
        unique=True,
        max_length=100,
        allow_unicode=True,
    )
    class Meta:
        verbose_name = "제품"
        verbose_name_plural = "제품"

    def slugify(self, tag, i=None):
        return slugify(tag, allow_unicode=True)

class PhoneTagsAll(GenericTaggedItemBase):
    tag = models.ForeignKey(
        PhoneTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )

class ProductTagsAll(GenericTaggedItemBase):
    tag = models.ForeignKey(
        ProductTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )


class Order(models.Model):
    class Meta:
        verbose_name = "주문"
        verbose_name_plural = "주문"

    customer = models.CharField('고객명', max_length=20, blank=True)
    phone = TaggableManager(blank=True, through=PhoneTagsAll, verbose_name="전화번호", help_text='-는 제외하고 입력',)
    facebook_url = models.URLField('페이스북 링크', max_length=500, blank=True)
    order_addr = models.CharField('주문주소', max_length=200, blank=True)
    bank_depositor = models.CharField('별도 입금자명', max_length=100, blank=True)
    bank_refund = models.CharField('환불계좌', max_length=100, blank=True)

    order_date = models.DateTimeField('주문시간')
    modify_date = models.DateTimeField('수정시간', null=True, blank=True)

    product = TaggableManager(through=ProductTagsAll, verbose_name="제품")
    quantity = models.IntegerField('수량')
    size = models.CharField('사이즈', max_length=100, blank=True,)

    confirm_transit = models.BooleanField('입금확인', default=False)
    confirm_cancel = models.BooleanField('주문취소', default=False)
    confirm_watch = models.BooleanField('유의항목', default=False)

    receptionist = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='접수자')
    receptionist_memo = SimpleMDEField('접수자메모', blank=True,)

    buying_actor = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='대행자')
    buying_url = models.URLField('대행자 구매링크', max_length=500, blank=True)
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
    class Meta:
        verbose_name = "계정세팅"
        verbose_name_plural = "계정세팅"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_per_page = models.IntegerField('페이지당게시글수', default=10)
