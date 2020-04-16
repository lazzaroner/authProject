from django.urls import path
from shuyuadmin import views

urlpatterns = [
    path('', views.table_obj_index, name='index'),
    path('index', views.table_obj_index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('reset', views.password_reset, name='password_reset'),
    path('reminder', views.password_reminder, name='password_reminder'),

    path('<app_name>/<table_name>', views.table_obj_display, name='table_obj_display'),
    path('<app_name>/<table_name>/add', views.table_obj_add, name='table_obj_add'),
    path('<app_name>/<table_name>/delete/<int:nid>', views.table_obj_delete, name='table_obj_delete'),
    path('<app_name>/<table_name>/update/<int:nid>', views.table_obj_update, name='table_obj_update'),
]
