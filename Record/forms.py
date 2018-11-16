from django import forms
from captcha.fields import CaptchaField
from django.contrib.admin import widgets
from .models import *


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')


class RegisterForm(forms.Form):
    SEX_CHOICES = (
        ('male', "男"),
        ('female', "女"),
    )
    user_name = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    tag_name = forms.CharField(label="昵称", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=SEX_CHOICES)
    captcha = CaptchaField(label='验证码')


class HomeForm(forms.Form):
    PER_CHOICES = (
        ('open', '公开'),
        ('close', '私密'),
    )
    STA_CHOICES = (
        ('full', '满员'),
        ('empty', '可入住'),
    )
    home_name = forms.CharField(label="房间名", max_length=256, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    create_user = forms.CharField(label="创建人", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    permission = forms.ChoiceField(label='权限', choices=PER_CHOICES)
    roommates = forms.ModelMultipleChoiceField(
        label="室友", queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple())
    home_states = forms.ChoiceField(label='状态', choices=STA_CHOICES)


class HomeMailForm(forms.Form):
    leave_user = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    leave_word = forms.CharField(label="内容", widget=forms.Textarea(
        attrs={'class': 'form-control'}))


class ExpenseForm(forms.Form):
    PAY_CHOICES = (
        ('yes', '已结算'),
        ('no', '待结算'),
    )
    PAY_WAY = (
        ('alipay', '支付宝'),
        ('weixinpay', '微信'),
        ('cashpay', '现金'),
    )
    pay_user = forms.CharField(label="支付人", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    join_user = forms.ModelMultipleChoiceField(
        label="共同使用人", queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple())
    pay_way = forms.ChoiceField(
        label='支付方式', choices=PAY_WAY)
    money = forms.DecimalField(label="金额(元)", max_digits=100, decimal_places=2, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    pay_state = forms.ChoiceField(
        label='结算状态', choices=PAY_CHOICES)
    Comment = forms.CharField(label='备注', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    date_time = forms.DateTimeField(label="时间", widget=forms.DateTimeInput(
        attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')
