from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from userctl.models import UserInfo
from django.http import JsonResponse
import json


def user_list(request):
    if not request.user.is_authenticated or request.user.group != 'admin':
        return redirect('/login/')
    group = request.GET.get("group", '')
    keyword = request.GET.get("keyword", '')
    admin_user = request.user
    users = UserInfo.objects.all()
    if group:
        users = users.filter(group=group)
    if keyword:
        users = users.filter(
            Q(name__icontains=keyword) |
            Q(sex__icontains=keyword)
        )
    if request.method == "POST":
        ids = request.POST.getlist("delete_ids")
        UserInfo.objects.filter(id__in=ids).delete()
        return redirect("/user/list/")

    return render(request, "user_list.html", {
        "users": users,
        "selected_group": group,
        "keyword": keyword,
        'admin_name': admin_user.name,
        'admin_avatar': admin_user.avatar.url if admin_user.avatar else 'media/avatars/default.jpg',
    })


def user_add(request):
    if request.path == '/user/add/':
        if not request.user.is_authenticated or request.user.group != 'admin':
            return redirect('/login/')
        p = 'user_add.html'
    elif request.path == '/user/sign/':
        p = 'user_sign.html'

    if request.method == "GET":
        return render(request, p, {
            'msg': '',
            'ages': range(1, 101)
        })

    elif request.method == "POST":
        get_post = request.POST
        username = get_post.get('username')
        password = get_post.get('password')
        age = get_post.get('age')
        sex = get_post.get("sex")
        group = get_post.get("group")

        if UserInfo.objects.filter(name=username).exists():
            return render(request, p, {"msg": "该用户名已被注册!", 'ages': range(1, 101)})

        if 'avatar' in request.FILES:
            img = request.FILES['avatar']
        else:
            img = None

        # 先创建用户实例，不保存密码
        user = UserInfo(
            name=username,
            age=int(age),
            sex=sex,
            group=group,
            avatar=img
        )
        user.set_password(password)  # 加密密码
        user.save()  # 保存到数据库

        if UserInfo.objects.filter(name=username).exists():
            if p == 'user_sign.html':
                return render(request, p, {"msg": '注册成功,3秒后返回登录界面', 'success': True})
            elif p == 'user_add.html':
                return render(request, p, {"msg": '添加成功', 'ages': range(1, 101)})
        else:
            return render(request, p, {"msg": '注册失败', 'ages': range(1, 101)})


@csrf_exempt
def user_del(request):
    if not request.user.is_authenticated or request.user.group != 'admin':
        return redirect('/login/')
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            ids = data.get("ids", [])
            UserInfo.objects.filter(id__in=ids).delete()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "无效请求"})

def user_alter(request,user_id):
    if not request.user.is_authenticated or request.user.group != 'admin':
        return redirect('/login/')
    alteruser = get_object_or_404(UserInfo, id=user_id)
    if request.method == "POST":
        alteruser.name = request.POST.get("name")
        alteruser.age = int(request.POST.get("age"))
        alteruser.sex=request.POST.get('sex')
        alteruser.group=request.POST.get("group")
        alteruser.avatar = request.FILES.get('avatar') if request.FILES.get('avatar') else alteruser.avatar
        alteruser.password = make_password(request.POST.get("password"))
        alteruser.save()
        return render(request,'user_alter.html',{'user': alteruser,'ages':range(1,101),'msg':'修改成功'})
    return render(request,'user_alter.html',{'user': alteruser,'ages':range(1,101)})
# Create your views here.

