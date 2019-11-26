from django.contrib import admin
from .models import User


@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ('username', 'mobile', 'email', 'coin')
    search_field = ('username', 'mobile', 'email')
    list_per_page = 20

admin.site.site_title = '护理坊'
admin.site.site_header = '护理坊'
admin.site.index_title = '护理坊'