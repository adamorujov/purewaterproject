from django.contrib import admin
from account.models import UserMoreInfoModel
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class UserMoreInfoInline(admin.StackedInline):
    model = UserMoreInfoModel

class CustomUserAdmin(UserAdmin):
    inlines = (UserMoreInfoInline,)
    # Modify fieldsets to remove 'groups'
    fieldsets = tuple(
        (title, {**options, 'fields': [field for field in options['fields'] if field != 'groups']})
        if isinstance(options, dict) and 'fields' in options
        else (title, options)
        for title, options in UserAdmin.fieldsets
    )
    
    # Optionally, you can also exclude 'groups' like this (if desired):
    # exclude = ('groups',)  # Removes groups from the form.

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
