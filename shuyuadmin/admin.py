from django.contrib import admin
from shuyuadmin import models

admin.site.register(models.MyUser)
admin.site.register(models.Menu)
admin.site.register(models.Role)
admin.site.register(models.Permission)
admin.site.register(models.Product)

