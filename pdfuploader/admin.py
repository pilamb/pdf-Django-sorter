from django.contrib import admin
from .models import Archive
import tagulous.admin


class ArchiveAdmin(admin.ModelAdmin):
    pass

#admin.site.register(Archive, ArchiveAdmin)
tagulous.admin.register(Archive)
tagulous.admin.register(Archive.tags)
