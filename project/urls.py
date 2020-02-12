from django.urls.conf import re_path,path
from django.conf.urls import  url
from .import views
app_name = 'project'
urlpatterns = [
#     path('',views.webLogin),
     # 登陆、注册 以及 信息、密码修改
    # 登陆、注册 以及 信息、密码修改
    path('index/',views.index,name='index'),
    path('regist/',views.register,name='register'),
    path('', views.login, name='login'),
    path('report/',views.webreport,name='report')
]

