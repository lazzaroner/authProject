from shuyuadmin.models import MyUser, Menu, Permission, Role
from shuyuadmin import models


class BaseAdmin(object):
    list_display = []
    list_filter = []
    fields = []
    search_fields = []
    filter_horizontal = []
    list_per_page = 8
    actions = []
    pass


class AdminSite(object):
    def __init__(self):
        """
        构造字典
        enabled_admins = {
            'app': {'user': userAdmin},
            'app名': {'mode名': admin类},
        }
        """
        self.enabled_admins = {}

    def register(self, model_class, admin_class=None):
        """
        注册自定义的admin类
        :param model_class: model类
        :param admin_class: 自定义的admin类
        :return:
        """
        app_name = model_class._meta.app_label
        model_name = model_class._meta.model_name

        # 如果不上送 admin 则默认使用BaseAdmin
        if admin_class is None:
            admin_class = BaseAdmin()
            list_display = []
            for l in model_class._meta.local_fields:
                if l.name == 'password':
                    continue
                list_display.append(l.name)
            admin_class.list_display = list_display
        admin_class.model = model_class

        # 如果admin 没有配置，则默认获取所有字段
        if not admin_class.list_display:
            list_display = []
            for l in model_class._meta.local_fields:
                if l.name == 'password':
                    continue
                list_display.append(l.name)
            admin_class.list_display = list_display

        if app_name not in self.enabled_admins:
            self.enabled_admins[app_name] = {}
        self.enabled_admins[app_name][model_name] = admin_class

    @staticmethod
    def init_tables(model_class):
        # 自动生成菜单、权限内容、角色信息 插入到数据库
        # 创建菜单
        # 创建 系统管理 菜单
        try:
            sys_menu_obj = Menu.objects.get(title='系统管理')
        except Menu.DoesNotExist:
            sys_menu_obj = Menu(title='系统管理')
            sys_menu_obj.save()

        # 创建model菜单
        menu_title = model_class._meta.verbose_name_plural
        app_name = model_class._meta.app_label
        model_name = model_class._meta.model_name
        try:
            menu_obj = Menu.objects.get(title=menu_title)
            if model_name in ['menu', 'role', 'myuser', 'permission']:
                if not menu_obj.parent:
                    menu_obj.parent = sys_menu_obj
                    menu_obj.save()
        except Menu.DoesNotExist:
            if model_name in ['menu', 'role', 'myuser', 'permission']:
                menu_obj = Menu(title=menu_title, parent=sys_menu_obj)
            else:
                menu_obj = Menu(title=menu_title)
            menu_obj.save()

        # 根据菜单创建权限
        for info in [('add', '添加'), ('delete', '删除'), ('update', '修改'), ('display', '查看')]:
            title = '%s%s' % (model_class._meta.verbose_name_plural, info[1])
            url = 'table_obj_%s' % info[0]
            p = {
                'title': title,
                'url': url,
                'app_name': app_name,
                'table_name': model_name,
                'menu': menu_obj
            }
            try:
                Permission.objects.get(title=title)
            except Permission.DoesNotExist:
                Permission.objects.create(**p)

        # 创建角色信息
        try:
            role_obj = Role.objects.get(title='系统管理员')
            role_obj.permissions.add(*Permission.objects.all())
        except Role.DoesNotExist:
            role_obj = Role(title='系统管理员')
            role_obj.save()
            role_obj.permissions.add(*Permission.objects.all())

        # 将系统管理员和角色进行关联
        for user in MyUser.objects.all():
            if user.is_admin:
                user.roles.add(role_obj)


class MyProductAdmin(BaseAdmin):
    list_filter = ['choice1', 'choice2', 'choice3']
    list_per_page = 4


class MyPermissionAdmin(BaseAdmin):
    search_fields = ['title', 'app_name', 'table_name']


site = AdminSite()

site.register(Role)
site.register(MyUser)
site.register(Menu)
site.register(Permission, MyPermissionAdmin)
site.register(models.Product, MyProductAdmin)

site.init_tables(Role)
site.init_tables(MyUser)
site.init_tables(Menu)
site.init_tables(Permission)
site.init_tables(models.Product)
