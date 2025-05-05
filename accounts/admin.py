from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Broker, Agent

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_broker', 'is_agent')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'is_broker', 'is_agent')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Broker)
admin.site.register(Agent)