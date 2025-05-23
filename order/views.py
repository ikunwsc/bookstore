from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Order
from book.models import BookInfo
from userctl.models import UserInfo
from django.utils import timezone
import json

def order_list(request):
    if not request.user.is_authenticated or request.user.group != 'admin':
        return redirect('/login/')
    keyword = request.GET.get('keyword', '')
    status = request.GET.get('status', '')
    admin_user=request.user
    orders = Order.objects.all()

    if keyword:
        orders = orders.filter(
            Q(user__name__icontains=keyword) |
            Q(book__name__icontains=keyword)
        )

    if status:
        orders = orders.filter(status=status)

    orders = orders.order_by('-id')  # 默认降序

    return render(request, 'order_list.html', {'orders': orders,'admin_name': admin_user.name,
        'admin_avatar': admin_user.avatar.url if admin_user.avatar else 'media/avatars/default.jpg',})


def order_del(request):
    if not request.user.is_authenticated or request.user.group != 'admin':
        return redirect('/login/')
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ids = data.get('ids', [])
            Order.objects.filter(id__in=ids).delete()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

def order_add(request):
    if not request.user.is_authenticated or request.user.group != 'admin':
        return redirect('/login/')
    if request.method == 'POST':
        user_id = request.POST.get('user')
        book_id = request.POST.get('book')
        number = request.POST.get('number')
        status = request.POST.get('status')
        date = request.POST.get('date')
        user = UserInfo.objects.get(id=user_id)
        book = BookInfo.objects.get(id=book_id)

        Order.objects.create(
            user=user,
            book=book,
            number=number,
            status=status,
            date=date
        )
        return render(request, 'order_add.html',{'msg': '添加成功'})

    users = UserInfo.objects.all()
    books = BookInfo.objects.all()
    today = timezone.now().date()

    return render(request, 'order_add.html', {
        'users': users,
        'books': books,
        'today': today
    })

# Create your views here.
