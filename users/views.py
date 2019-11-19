from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm


def logout_view(request):
    """注销用户"""
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))


def register(request):
    """注册新用户"""
    if request.method != 'POST':
        # 显示空的注册表单
        form = UserCreationForm()
    else:
        # 处理填写好的表单
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()  # 将用户名和密码的散列值保存到数据库中
            # 让用户自动登录并重定向到主页
            # 返回一个通过了身份验证的用户对象并保存到authenticated_user中
            authenticated_user = authenticate(username=new_user.username,
                                              password=request.POST['password1'])
            # 为新用户创建有效的会话
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('learning_logs:index'))

    context = {'form': form}
    return render(request, 'users/register.html', context)
