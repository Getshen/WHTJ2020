from django.shortcuts import render, redirect
from django.contrib import auth
# from .models import User
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import   connection

# Create your views here.
def get_corsor():
    return connection.cursor()

# Create your views here.
def webLogin(request):
    return render(request,"login.html")


def index(request):
    return render(request,'index.html')
 
def register(request):
    if request.method == 'POST':
        # 验证表单RegistrationForm的数据是否有效
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            
            # 使用内置User自带create_user方法创建用户，不需要使用save()
            User.objects.create_user(username=username, password=password)
            #  注册成功，通过HttpResponseRedirect方法转到登陆页面
            return HttpResponseRedirect(reverse('project:login'))
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

 
def login(request):
    print(request.method)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # 调用Django自带的auth.authenticate() 来验证用户名和密码是否正确
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                # 调用auth.login()来进行登录
                auth.login(request, user)
                # 登录成功，转到用户个人信息页面
                # []是有序的可reverse，{}是无序的
                return HttpResponseRedirect(reverse('project:index'))
            else:
                # 登陆失败
               
                return render(request, 'login.html', {'form': form,'message': '密码错误，请重试！'})
    else:
        # 如果用户没有提交表单或不是通过POST方法提交表单，转到登录页面，生成一张空的LoginForm
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})
def webreport(request):
    cursor = get_corsor()
    cursor.execute('''SELECT  
    DATE_FORMAT(
      jr.calltime,
      '%Y-%m-%d'
     ) days, 
    COUNT(DISTINCT IF(jr.city="宜昌",jr.callednum,null)) as "宜昌-外呼量",
    COUNT(DISTINCT IF(jr.city="江汉",jr.callednum,null)) as "江汉-外呼量",
    COUNT(DISTINCT IF(jr.city="襄阳",jr.callednum,null)) as "襄阳-外呼量",
    COUNT(DISTINCT IF(jr.city="荆门",jr.callednum,null)) as "荆门-外呼量"
    from jz_record as jr
    where jr.calltime  BETWEEN "2020-01-10 00:00:00" and "2020-01-15 00:00:00"
    GROUP BY days''')
    report_datas = cursor.fetchall()
    datas = [['日期','宜昌','江汉','襄阳','荆门'],]
    for da in list(map(list, report_datas)):
        datas.append(da)
    print(datas)
    return render(request,"report.html",context={"datas":datas})
