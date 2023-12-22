
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'name' ,'hotel', 'membership', 'credit_points', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'name' , 'hotel', 'membership')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    ordering = ('date_joined', )
admin.site.register(CustomUser, CustomUserAdmin)