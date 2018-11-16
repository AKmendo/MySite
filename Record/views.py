import hashlib

from django.http import Http404
# Create your views here.
from django.shortcuts import get_object_or_404, redirect, render

from .forms import *
from .models import *


def hash_code(s, salt='mysite'):  # 加密
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def index(request):
    HomeList = Home.objects.all().order_by("-c_time")
    status = 'full'
    per = 'open'
    hot_home = Home.objects.all().order_by("-c_time")[:5]
    return render(request, 'home/index.html', locals())


def Homeinfo(request, id):
    Expense_V = Expense.objects.all().order_by("-date_time")
    homeinfo = get_object_or_404(Home, pk=str(id))
    all_roommates = homeinfo.roommates.all()
    home_comment = homeinfo.comments.all().order_by("-leave_time")
    status = 'full'
    per = 'open'
    expense_view = False
    login_user = request.session.get('user_name', None)
    for Fuser in all_roommates:
        if login_user == Fuser.user_name:
            expense_view = True
    if request.method == 'POST':
        comment_form = HomeMailForm(request.POST)
        if comment_form.is_valid():
            leave_user = comment_form.cleaned_data['leave_user']
            leave_word = comment_form.cleaned_data['leave_word']

            contents = get_object_or_404(Home, pk=str(id))
            new_comment = HomeMail(home=homeinfo,
                                   leave_user=leave_user,
                                   leave_word=leave_word)
            new_comment.save()
    comment_form = HomeMailForm()
    return render(request, 'home/homeinfo.html', locals())


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
                return redirect('/')  # 自动跳转到主页
        record_form = ExpenseForm()
        return render(request, 'expense/record.html', locals())
    else:
        return redirect('/')


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
    return redirect("/")


def createhome(request):
    if request.session.get('is_login', None):
        if request.method == "POST":
            home_form = HomeForm(request.POST)
            message = "请检查填写的内容！"
            if home_form.is_valid():  # 获取数据
                home_name = home_form.cleaned_data['home_name']
                create_user = home_form.cleaned_data['create_user']
                home_states = home_form.cleaned_data['home_states']
                permission = home_form.cleaned_data['permission']
                roommates = home_form.cleaned_data['roommates']
                if create_user != request.session.get('user_name', None):
                    message = "请输入正确的用户名！"
                    return render(request, 'home/createhome.html', locals())
                else:
                    same_home_name = Home.objects.filter(home_name=home_name)
                    if same_home_name:  # 房间名唯一
                        message = '房间名已被使用，请重新选择房间名！'
                        return render(request, 'home/createhome.html', locals())
                    # 当一切都OK的情况下，创建房间

                    new_home = Home.objects.create()
                    new_home.home_name = home_name
                    new_home.create_user = create_user
                    new_home.home_states = home_states
                    new_home.permission = permission
                    for roommate in roommates:
                        new_home.roommates.add(roommate)
                    new_home.save()
                    return redirect('/')  # 自动跳转到首页
        home_form = HomeForm()
        return render(request, 'home/createhome.html', locals())


def MyHome(request):
    if request.session.get('is_login', None):
        HomeList = Home.objects.all().order_by("-c_time")
        return render(request, 'home/myhome.html', locals())
