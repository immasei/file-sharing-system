from django.contrib import admin
from .models import CUser, Group, GroupMember, File, Chunk, FileContent, Trash, Device, SyncService

# Register
admin.site.register(CUser)
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(File)
admin.site.register(Chunk)
admin.site.register(FileContent)
admin.site.register(Trash)
admin.site.register(Device)
admin.site.register(SyncService)