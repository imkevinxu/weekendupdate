from weekendupdate_app.models import *
from django.contrib import admin

class ArchiveAdmin(admin.ModelAdmin):
    list_display = ('link', 'edition', 'description', 'created_at')
    ordering = ['-edition']

admin.site.register(Archive, ArchiveAdmin)