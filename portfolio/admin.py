from django.contrib import admin
from .models import Message


# Register your models here.
class HomeAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization_name', 'message',)


admin.site.register(Message, HomeAdmin)
