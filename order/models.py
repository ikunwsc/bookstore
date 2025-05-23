from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from book.models import BookInfo  # 假设你的 BookInfo 模型在 book 应用中
from userctl.models import UserInfo
class Order(models.Model):
    STATUS_CHOICES = [
        ('waiting', '等待'),
        ('finished', '结束'),
    ]

    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='orders', verbose_name='用户')
    book = models.ForeignKey(BookInfo, on_delete=models.CASCADE, related_name='orders', verbose_name='书籍')
    number = models.PositiveIntegerField(default=1, verbose_name='数量')
    date = models.DateField(default=timezone.now, verbose_name='下单日期')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting', verbose_name='状态')

    def __str__(self):
        return f"{self.user.name} 的订单：{self.book.name} x {self.number}"
