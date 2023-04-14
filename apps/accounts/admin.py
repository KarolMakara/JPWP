from django.contrib import admin
from apps.accounts.models import MyUser


class MyUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(MyUser, MyUserAdmin)
