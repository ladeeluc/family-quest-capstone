from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from useraccount.models import UserAccount

from django.utils.translation import ugettext_lazy as _

class UserAccountAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Linked Data'), {'fields': ('person',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'is_staff')
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(UserAccount, UserAccountAdmin)