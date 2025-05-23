from django.db import models

class BookInfo(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name="书名")
    author = models.CharField(max_length=32, verbose_name="作者")
    price = models.FloatField(verbose_name="价格")
    cover = models.ImageField(upload_to='covers/', blank=True, null=True, verbose_name='封面')

    def __str__(self):
        return self.name
