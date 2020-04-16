from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    nickname = models.CharField(max_length=32, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    roles = models.ManyToManyField(verbose_name='角色', to='Role')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name_plural = '用户管理'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Menu(models.Model):
    """
    菜单
    """
    title = models.CharField(max_length=32, unique=True)
    parent = models.ForeignKey('Menu',null=True, blank=True, on_delete=models.CASCADE)

    # 定义菜单间的自引用关系
    # 权限url 在 菜单下；菜单可以有父级菜单；还要支持用户创建菜单，因此需要定义parent字段（parent_id）
    # blank=True 意味着在后台管理中填写可以为空，根菜单没有父级菜单

    class Meta:
        verbose_name_plural = '菜单管理'

    def __str__(self):
        title_list = [self.title]
        p = self.parent
        while p:
            title_list.insert(0, p.title)
            p = p.parent
        return '->'.join(title_list)


class Permission(models.Model):
    """
    权限
    """
    title = models.CharField(max_length=64, unique=True, verbose_name='名称')
    url = models.CharField(max_length=256)
    app_name = models.CharField(max_length=32, verbose_name='应用名')
    table_name = models.CharField(max_length=32, verbose_name='表名')
    menu = models.ForeignKey('Menu', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '权限管理'

    def __str__(self):
        return '%s-%s' % (self.menu, self.title)


class Role(models.Model):
    """
    角色
    """
    title = models.CharField(max_length=64, unique=True)
    permissions = models.ManyToManyField('Permission')

    class Meta:
        verbose_name_plural = '角色管理'

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=128, unique=True)
    type_choice1 = (
        (1, '16G'),
        (2, '32G'),
        (3, '4G'),
        (4, '8G'),
    )
    choice1 = models.SmallIntegerField(choices=type_choice1, verbose_name='内存容量')
    type_choice2 = (
        (1, '集成显卡'),
        (2, '独立显卡'),
    )
    choice2 = models.SmallIntegerField(choices=type_choice2, verbose_name='显卡类型')

    type_choice3 = (
        (1, 'Windows 10'),
        (2, 'Mac OS'),
        (3, 'Linux'),
    )
    choice3 = models.SmallIntegerField(choices=type_choice3, verbose_name='操作系统')

    size = models.CharField(max_length=10)
    comment = models.TextField()

    class Meta:
        verbose_name_plural = "产品管理"





