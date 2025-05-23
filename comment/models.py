from django.db import models
from userctl.models import UserInfo
from book.models import BookInfo

class Comment(models.Model):
    book = models.ForeignKey(BookInfo, on_delete=models.CASCADE, related_name='comments')  # 所属图书
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')  # 父评论，支持多层回复
    created_at = models.DateTimeField(auto_now_add=True)


# Create your models here.
