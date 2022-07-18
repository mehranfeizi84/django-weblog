from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# add fields to user manager
UserAdmin.fieldsets[2][1]['fields'] = (
                                'is_active',
                                'is_staff',
                                'is_superuser',
                                'is_author',
                                'special_user',
                                'groups',
                                'user_permissions',
                                'image'
                            ),

# show items in django panel
UserAdmin.list_display += ('is_author', 'is_special_user', 'image')


admin.site.register(User, UserAdmin)