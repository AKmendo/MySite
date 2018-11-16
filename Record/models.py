import datetime

from django.db import models
from django.utils import timezone

# Create your models here.


class User(models.Model):
    '''用户表'''
    SEX_CHOICES = (
        ('male', '男'),
        ('female', '女'),
    )
    user_name = models.CharField(max_length=128, unique=True)
    tag_name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=SEX_CHOICES, default='男')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_name)

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class Home(models.Model):
    '''房间表'''
    PER_CHOICES = (
        ('open', '公开'),
        ('close', '私密'),
    )
    STA_CHOICES = (
        ('full', '满员'),
        ('empty', '可入住'),
    )
    home_name = models.CharField(max_length=256, unique=True)
    create_user = models.CharField(max_length=128)
    permission = models.CharField(
        max_length=32, choices=PER_CHOICES, default='私密')
    roommates = models.ManyToManyField(User)
    home_states = models.CharField(
        max_length=64, choices=STA_CHOICES, default='满员')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.home_name)

    class Meta:
        ordering = ['c_time']
        verbose_name = '房间'
        verbose_name_plural = '房间'


class HomeMail(models.Model):
    '''房间留言表'''
    home = models.ForeignKey(
        Home, related_name='comments', on_delete=models.CASCADE)
    leave_user = models.CharField(max_length=128)
    leave_word = models.TextField()
    leave_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.leave_word)

    class Meta:
        ordering = ['leave_time']
        verbose_name = '房间留言'
        verbose_name_plural = '房间留言'


class Expense(models.Model):
    '''花费记录表'''
    PAY_CHOICES = (
        ('yes', '已结算'),
        ('no', '待结算'),
    )
    PAY_WAY = (
        ('alipay', '支付宝'),
        ('weixinpay', '微信'),
        ('cashpay', '现金'),
    )
    pay_user = models.CharField(max_length=128)
    join_user = models.ManyToManyField(User)
    pay_way = models.CharField(
        max_length=64, choices=PAY_WAY, default='支付宝')
    money = models.DecimalField(max_digits=100, decimal_places=2)
    Comment = models.CharField(max_length=256)
    date_time = models.DateTimeField('date published', default=timezone.now)
    pay_state = models.CharField(
        max_length=32, choices=PAY_CHOICES, default='待结算')

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_time <= now
    was_published_recently.admin_order_field = 'date_time'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def __str__(self):
        return str(self.pay_user)

    class Meta:
        ordering = ['date_time']
        verbose_name = '账单'
        verbose_name_plural = '账单'
