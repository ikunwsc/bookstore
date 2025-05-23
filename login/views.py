from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login

def login(request):
    if request.method == "GET":
        return render(request, 'login.html', {"msg": ' '})

    elif request.method == "POST":
        username = request.POST.get('user')
        password = request.POST.get('password')
        group = request.POST.get('group')
        user = authenticate(request, name=username, password=password)
        if user is not None:
            if user.group != group:
                return render(request, 'login.html', {"msg": "用户组错误喵~"})
            auth_login(request, user)
            # 登录成功，跳转并带上头像信息（可用session或者直接模板里用request.user.avatar）
            if user.group=='admin':
                return redirect('/adminhome/')
            elif user.group=='user':
                return redirect('/user/home/')
        else:
            return render(request, 'login.html', {"msg": '用户名或密码错误喵~'})
