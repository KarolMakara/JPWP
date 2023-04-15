from django.contrib import admin
from apps.accounts.models import MyUser, MyGroup


class MyUserAdmin(admin.ModelAdmin):
    pass


class MyGroupAdmin(admin.ModelAdmin):
    pass


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(MyGroup, MyGroupAdmin)