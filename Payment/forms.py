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
    sex = forms.ChoiceField(label='性别', choices=SEX_CHOICES,widget=forms.RadioSelect)
    captcha = CaptchaField(label='验证码')

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
        label='支付方式', choices=PAY_WAY,widget=forms.RadioSelect)
    money = forms.DecimalField(label="金额(元)", max_digits=100, decimal_places=2, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    pay_state = forms.ChoiceField(
        label='结算状态', choices=PAY_CHOICES,widget=forms.RadioSelect)
    Comment = forms.CharField(label='备注', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    date_time = forms.DateTimeField(label="时间", widget=forms.DateTimeInput(
        attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')


class ExpenseModelForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['pay_user', 'join_user', 'pay_way',
                  'money', 'pay_state', 'Comment']
        widgets = {
            'pay_user': forms.TextInput(attrs={'class': 'form-control'}),
            'join_user': forms.CheckboxSelectMultiple(),
            'pay_way': forms.RadioSelect,
            'money': forms.TextInput(attrs={'class': 'form-control'}),
            'pay_state': forms.RadioSelect,
            'Comment': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ExpenseModelForm, self).__init__(*args, **kwargs)
