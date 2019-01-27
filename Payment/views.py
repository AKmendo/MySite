import hashlib
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
# Create your views here.
from django.shortcuts import get_object_or_404, redirect, render
from haystack.views import SearchView
from .forms import *
from .models import *


def hash_code(s, salt='mysite'):  # 加密
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def index(request):
    if request.session.get('is_login', None):
        Expense_V = Expense.objects.all().order_by("-date_time")
        paginator = Paginator(Expense_V, 20) # Show 20 contacts per page
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)
        paychiocse1='no'
        paychiocse2='yes'
        months=[]
        pay_money=[]
        for i in range(1,13):
            Date_time=Expense.objects.all().filter(date_time__month=i)
            pays=0
            for pay_data in Date_time:
                pays=pays+int(pay_data.money)
            d=str(i)+"月"
            months.append(d)
            pay_money.append(pays)
        pay_users=User.objects.all()
        pay_sum=0
        datas=[]
        for users in pay_users:
            for expens in Expense_V:
                if expens.pay_user==users.user_name:
                     pay_sum=pay_sum+int(expens.money)
            data={"value":pay_sum,"name":users.user_name}
            datas.append(data)
            pay_sum=0
        return render(request, 'index.html', locals())
    else:
        return redirect("/login/")

def help(request):
    return render(request,'help/help.html')

class MySeachView(SearchView):
    def extra_context(self):
        context = super(MySeachView,self).extra_context()
        return context

def Show_accounts(request):
    if request.session.get('is_login', None):
        login_name=request.session.get('user_name', None)
        Expense_V = Expense.objects.all().order_by("-date_time").filter(pay_user=login_name)
        paychiocse1='no'
        paychiocse2='yes'
        M_n=[]
        M_n_a=[]
        M_n_na=[]
        M_y=[]
        M_y_a=[]
        M_y_na=[]
        for accounts in Expense_V:
            if accounts.pay_state==paychiocse1:
                M_n.append(0)
                M_n.append(accounts.money)
                if len(accounts.join_user.all())==3:
                    M_n_a.append(0)
                    M_n_a.append(accounts.money)
                else:
                    M_n_na.append(0)
                    M_n_na.append(accounts.money)
            else: 
                M_y.append(accounts.money)
                M_y.append(0)
                if len(accounts.join_user.all())==3:
                    M_y_a.append(0)
                    M_y_a.append(accounts.money)
                else:
                    M_y_na.append(0)
                    M_y_na.append(accounts.money)
        Sum_n=sum(M_n)
        Sum_n_a=sum(M_n_a)
        Sum_n_na=sum(M_n_na)
        Sum_y=sum(M_y)
        Sum_y_a=sum(M_y_a)
        Sum_y_na=sum(M_y_na)
        return render(request, 'payment/show_accounts.html', locals())

def Show_info(request, exp_id):
    if request.session.get('is_login', None):
        Expenses = Expense.objects.get(pk=exp_id)
        return render(request, 'payment/only_one.html', locals())

def record(request):
    if request.session.get('is_login', None):
        if request.method == "POST":
            record_form = ExpenseForm(request.POST)
            message = "请检查填写的内容！"
            if record_form.is_valid():  # 获取数据
                pay_user = record_form.cleaned_data['pay_user']
                join_user = record_form.cleaned_data['join_user']
                pay_way = record_form.cleaned_data['pay_way']
                money = record_form.cleaned_data['money']
                date_time = record_form.cleaned_data['date_time']
                Comment = record_form.cleaned_data['Comment']
                pay_state = record_form.cleaned_data['pay_state']

                new_Expense = Expense.objects.create(
                    pay_user=pay_user,
                    pay_way=pay_way,
                    money=money,
                    date_time=date_time,
                    Comment=Comment,
                    pay_state=pay_state
                )
                for tag in join_user:
                    new_Expense.join_user.add(tag)
                new_Expense.save()
                return redirect('/myexpense_list/')  # 自动跳转到用户主页
        record_form = ExpenseForm()
        return render(request, 'payment/record.html', locals())
    else:
        return redirect('/')

def ChangeExpense(request, exp_id):
    if request.session.get('is_login', None):
        expenseinfo = Expense.objects.get(pk=exp_id)
        if request.method == "POST":
            record_form = ExpenseModelForm(request.POST, instance=expenseinfo)
            if record_form.is_valid():
                record_form.save()
                return redirect('/myexpense_list/')
        record_form = ExpenseModelForm(instance=expenseinfo)
        return render(request, 'payment/expense_ch.html', locals())


def DeleteExpense(request, del_id):
    if request.session.get('is_login', None):
        Expense_V = Expense.objects.all().order_by("-date_time")
        Expense.objects.get(pk=del_id).delete()
        return render(request, 'payment/myexpense.html', locals())


def MyExpense(request):
    Expense_V = Expense.objects.all().order_by("-date_time")
    paychiocse1='no'
    paychiocse2='yes'
    return render(request, 'payment/myexpense.html', locals())


def login(request):
    if request.session.get('is_login', None):
        return redirect('/')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(user_name=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.user_name
                    return redirect('/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。
        return redirect("/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            user_name = register_form.cleaned_data['user_name']
            tag_name = register_form.cleaned_data['tag_name']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = User.objects.filter(user_name=user_name)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_tag_name = User.objects.filter(tag_name=tag_name)
                if same_tag_name:  # 用户名唯一
                    message = '昵称已经被使用，请重新选择昵称！'
                    return render(request, 'login/register.html', locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = User.objects.create()
                new_user.user_name = user_name
                new_user.tag_name = tag_name
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login/")