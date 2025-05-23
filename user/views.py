from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password,check_password
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from order.models import Order
from userctl.models import UserInfo
from book.models import BookInfo
from django.views.decorators.http import require_POST

def user_home(request):
    if not request.user.is_authenticated or request.user.group != 'user':
        return redirect('/login/')
    user = request.user
    # 判断头像是否存在
    if hasattr(user, 'avatar') and user.avatar:
        avatar_url = user.avatar.url  # 自动生成 /media/... 路径
    else:
        avatar_url = '/static/images/default.jpg'  # 默认头像

    return render(request, 'user_home.html', {
        'username': user.name,
        'avatar_url': avatar_url
    })

def shop(request):
    if not request.user.is_authenticated or request.user.group != 'user':
        return redirect('/login/')
    user = request.user
    query = request.GET.get('q', '')
    book_list = BookInfo.objects.all()
    if query:
        book_list = book_list.filter(name__icontains=query) | book_list.filter(author__icontains=query)
    paginator = Paginator(book_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if hasattr(user, 'avatar') and user.avatar:
        avatar_url = user.avatar.url  # 自动生成 /media/... 路径
    else:
        avatar_url = '/static/images/default.jpg'  # 默认头像
    return render(request, 'shop.html', {
            'books': page_obj,
            'query': query,
            'username': request.user.name,
            'avatar_url': avatar_url,
    })

def user_talk(request):
    if not request.user.is_authenticated or request.user.group != 'user':
        return redirect('/login/')

def user_center(request):
    if not request.user.is_authenticated or request.user.group != 'user':
        return redirect('/login/')
    user = request.user
    if hasattr(user, 'avatar') and user.avatar:
        avatar_url = user.avatar.url  # 自动生成 /media/... 路径
    else:
        avatar_url = '/static/images/default.jpg'  # 默认头像

    return render(request, 'user_center.html', {
        'username': user.name,
        'avatar_url': avatar_url
    })

def buy(request):
    if not request.user.is_authenticated or request.user.group != 'user':
        return redirect('/login/')
    if request.method == 'POST':
        name = request.POST.get('book_name')
        number = request.POST.get('number')

        try:
            book = BookInfo.objects.get(name=name)
            user = request.user
            status = '等待'  # 默认状态
            date = timezone.now().date()

            Order.objects.create(
                user=user,
                book=book,
                number=number,
                status=status,
                date=date
            )

            return JsonResponse({'success': True, 'message': '购买成功喵~'})
        except BookInfo.DoesNotExist:
            return JsonResponse({'success': False, 'message': '书籍不存在喵！'})
    return JsonResponse({'success': False, 'message': '请求方法错误喵！'})

def user_edit(request):
    if not request.user.is_authenticated or request.user.group != 'user':
        return redirect('/login/')

    user = request.user
    msg = ''

    if hasattr(user, 'avatar') and user.avatar:
        avatar_url = user.avatar.url
    else:
        avatar_url = '/media/covers/cover_default.jpg'

    if request.method == 'POST':
        name = request.POST.get('name')
        sex = request.POST.get('sex')
        avatar = request.FILES.get('avatar')

        if UserInfo.objects.exclude(id=user.id).filter(name=name).exists():
            msg = "该用户名已存在"
        else:
            user.name = name
            user.sex = sex
            if avatar:
                user.avatar = avatar
            user.save()
            msg = "修改成功"
            avatar_url = user.avatar.url  # 更新新的头像地址

    return render(request, 'user_edit.html', {
        'username': user.name,
        'avatar_url': avatar_url,
        'msg': msg
    })

def user_orders(request):
    if not request.user.is_authenticated or request.user.group != 'user':
        return redirect('/login/')
    user = request.user
    if hasattr(user, 'avatar') and user.avatar:
        avatar_url = user.avatar.url  # 自动生成 /media/... 路径
    else:
        avatar_url = '/media/covers/cover_default.jpg'  # 默认头像

    user=request.user
    orders = Order.objects.all()
    orders=orders.filter(user=user)
    for order in orders:
        order.total_price=order.number*order.book.price
    return render(request, 'user_orders.html', {
        'username': user.name,
        'avatar_url': avatar_url,
        'orders': orders,
    })

def user_safety(request):
    if not request.user.is_authenticated or request.user.group != 'user':
        return redirect('/login/')
    user = request.user
    if hasattr(user, 'avatar') and user.avatar:
        avatar_url = user.avatar.url  # 自动生成 /media/... 路径
    else:
        avatar_url = '/media/covers/cover_default.jpg'  # 默认头像
    user = request.user
    msg=''
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        if not check_password(old_password,user.password):
            msg='密码错误'
        elif old_password==new_password1:
            msg='新密码不能与旧密码相同'
        elif new_password1!=new_password2:
            msg='两次输入不一致'
        else:
                user.password=make_password(new_password1)
                user.save()
                update_session_auth_hash(request, user)  # 防止修改密码后自动登出
                msg='修改成功'
    return render(request, 'user_safety.html', {
        'username': user.name,
        'avatar_url': avatar_url,
        'msg': msg,
    })

@require_POST
def pay_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == "等待":
        order.status = "结束"
        order.save()
    return redirect('/user/orders/')

def chart(request):
    pass
# Create your views here.
