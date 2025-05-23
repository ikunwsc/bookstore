from django.db.models import Q
from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
from book.models import BookInfo


def book_del(request):
    if not request.user.is_authenticated or request.user.group != 'admin':
        return redirect('/login/')
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ids = data.get('ids', [])
            BookInfo.objects.filter(id__in=ids).delete()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

def book_add(request):
    if not request.user.is_authenticated or request.user.group != 'admin':
        return redirect('/login/')
    if request.method == "GET":
        return render(request, 'book_add.html', {'msg': ''})
    elif request.method == "POST":
        get_post = request.POST
        name = get_post.get('name')
        author = get_post.get('author')
        price= get_post.get('price')
        cover = request.FILES.get('cover')
        from book.models import BookInfo
        if BookInfo.objects.filter(name=name).exists():
            return render(request,'book_add.html',{"msg":"该用书籍已经存在!"})
        try:
            BookInfo.objects.create(name=name, author=author, price=float(price), cover=cover)
            return render(request, 'book_add.html', {"msg": '添加成功'})
        except Exception as e:
            return render(request, 'book_add.html', {"msg": '添加失败'})

def book_list(request):
    if not request.user.is_authenticated or request.user.group != 'admin':
        return redirect('/login/')
    admin_user = request.user
    keyword = request.GET.get('keyword', '')
    order = request.GET.get('order', 'desc')  # 默认价格降序

    books = BookInfo.objects.all()

    if keyword:
        books = books.filter(Q(name__icontains=keyword) | Q(author__icontains=keyword))

    if order == 'asc':
        books = books.order_by('price')
    else:
        books = books.order_by('-price')

    context = {
        'books': books,
        'keyword': keyword,
        'order': order,
        'admin_name': admin_user.name,
        'admin_avatar': admin_user.avatar.url if admin_user.avatar else 'media/avatars/default.jpg',
    }
    return render(request, 'book_list.html', context)

# Create your views here.
