"""
URL configuration for DjangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from userctl import views as userctl_views
from login import views as login_views
from book import views as book_views
from adminhome import views as admin_home_views
from order import views as order_views
from django.conf import settings
from django.conf.urls.static import static
from user import views as user_views
urlpatterns = [
    path("admin/", admin.site.urls),
    path('user/add/',userctl_views.user_add),
    path('user/del/',userctl_views.user_del),
    path('user/list/',userctl_views.user_list),
    path('login/',login_views.login),
    path("user/sign/",userctl_views.user_add),
    path('book/add/',book_views.book_add),
    path('book/del/',book_views.book_del),
    path('book/list/',book_views.book_list),
    path('adminhome/',admin_home_views.admin_home),
    path('order/add/',order_views.order_add),
    path('order/list/',order_views.order_list),
    path('user/home/',user_views.user_home),
    path('logout/',admin_home_views.logout_view),
    path('order/del/',order_views.order_del),
    path('shop/',user_views.shop),
    path('user/talk',user_views.user_talk),
    path('user/center/',user_views.user_center),
    path('buy/',user_views.buy),
    path('user/edit/',user_views.user_edit),
    path('user/orders/',user_views.user_orders),
    path('user/orders/pay/<int:order_id>/',user_views.pay_order),
    path('user/safety/',user_views.user_safety),
    path('user/alter/<int:user_id>/',userctl_views.user_alter),
    path('book/alter/<int:book_id>/',book_views.book_alter),
    path('order/alter/<int:order_id>/',order_views.order_alter),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


