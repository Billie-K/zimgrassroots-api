from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django import forms
from django.db import models


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email', 'username', 'name',)
    list_filter = ('email', 'username', 'name', 'is_active', 'is_staff')
    ordering = ('-created_at',)
    list_display = ('email', 'username', 'name',
                    'is_active', 'is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'name','avatar','role',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'name', 'avatar', 'address', 'role', 'password1', 'password2', 'is_active', 'is_staff',)}
         ),
    )


admin.site.register(User, UserAdminConfig)
admin.site.register(Permissions)
admin.site.register(Project)
admin.site.register(Sponsor)
admin.site.register(Beneficiary)
admin.site.register(Order)
admin.site.register(Task)


