from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from shuyuadmin.admin_sites import site
from shuyuadmin.utils import pager, permissions


@login_required()
def index(request):
    return_data = {
        'enabled_admins': site.enabled_admins,
        'my_menu': permissions.get_permissions_menu(request.user)
    }
    return render(request, 'shuyuadmin/table_obj_index.html', return_data)


def login(request):
    """
    登录
    :param request:
    :return:
    """
    return_data = {
        'errors': '',
        'username': ''
    }
    if request.method == 'GET':
        return render(request, 'shuyuadmin/login.html', return_data)
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_page = request.GET.get('next') or '/shuyuadmin/index'
        user = authenticate(request, email=username, password=password)
        if user:
            auth_login(request, user)
            return redirect(next_page)
        else:
            return_data['errors'] = '用户名或者密码错误'
            return_data['username'] = username
        return render(request, 'shuyuadmin/login.html', return_data)


@login_required
def logout(request):
    """
    注销
    :param request:
    :return:
    """
    return_data = {
        'errors': ''
    }
    auth_logout(request)
    return render(request, 'shuyuadmin/login.html', return_data)


@login_required
def password_reset(request):
    """
    密码重置
    :param request:
    :return:
    """
    pass


def password_reminder(request):
    """
    忘记密码
    :param request:
    :return:
    """
    pass


def register(request):
    """
    注册
    :param request:
    :return:
    """
    pass


def table_obj_index(request):
    return_data = {
        'enabled_admins': site.enabled_admins,
        'my_menu': permissions.get_permissions_menu(request.user),
    }
    return render(request, 'shuyuadmin/table_obj_index.html', return_data)


def table_obj_display(request, app_name, table_name):
    # # 通过反射根据表名获取表名的对象
    # model_obj = getattr(models_module, table_name)
    # 不通过上面的反射获取model对象 直接通过app_name 和table_name 到king_admin字典里面获取
    admin_class = site.enabled_admins[app_name][table_name]
    object_list, filter_conditions = pager.table_filter(request, admin_class)
    admin_class.filter_conditions = filter_conditions

    # 分页
    # paginator = Paginator(object_list, admin_class.per_page)
    # print(paginator.page_range)
    # object_list = paginator.page(1)

    page_data = pager.split_page(object_list, page_num=request.GET.get('page'), per_page=admin_class.list_per_page)
    return_data = {
        'enabled_admins': site.enabled_admins,
        'app_name': app_name,
        'table_name': table_name,
        "page_data": page_data,
        'admin_class': admin_class,
        'my_menu': permissions.get_permissions_menu(request.user),
    }

    return render(request, 'shuyuadmin/table_obj_display.html', return_data)


def table_obj_add(request):
    pass


def table_obj_delete(request, nid):
    pass


def table_obj_update(request, nid):
    pass