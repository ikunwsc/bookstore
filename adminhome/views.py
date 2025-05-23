from django.http import HttpResponseNotAllowed
from django.shortcuts import render,redirect
from userctl.models import UserInfo
from django.contrib.auth import logout



def admin_home(request):
    if not request.user.is_authenticated or request.user.group != 'admin':
        return redirect('/login/')

    admin_user = request.user  # 当前登录用户
    return render(request, 'admin_home.html', {
        'admin_name': admin_user.name,
        'admin_avatar': admin_user.avatar.url if admin_user.avatar else 'media/avatars/default.jpg',  # 头像url
    })

# Create your views here.
def logout_view(request):
    logout(request)
    return redirect('/login/')