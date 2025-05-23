from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class UserInfoManager(BaseUserManager):
    def create_user(self, user_name, password=None, **extra_fields):
        if not user_name:
            raise ValueError("用户名不能为空喵~")
        user = self.model(user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(user_name, password, **extra_fields)

class UserInfo(AbstractBaseUser, PermissionsMixin):
    SEX_CHOICES = [('男', '男'), ('女', '女')]
    GROUP_CHOICES = [('admin', '管理员'), ('user', '用户')]

    name = models.CharField(max_length=32, unique=True, verbose_name='用户名')
    avatar = models.ImageField(upload_to='avatars/', default='avatars/cover_default.jpg', verbose_name='头像')
    sex = models.CharField(max_length=2, choices=SEX_CHOICES, default='男', verbose_name='性别')
    age = models.IntegerField(verbose_name='年龄')
    group = models.CharField(max_length=6, choices=GROUP_CHOICES, default='user', verbose_name='用户组')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserInfoManager()

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['age', 'sex', 'group']

    def __str__(self):
        return self.name
