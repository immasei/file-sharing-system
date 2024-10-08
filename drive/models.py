from django.db.models import *
from django.db.models.functions import Now
from datetime import timedelta

class CUser(Model):
    name = CharField(max_length=30)
    email = EmailField(unique=True)
    password = CharField(max_length=11)
    quota_limit = DecimalField(decimal_places=1, default=300.0, max_digits=4)
    quota_used = DecimalField(decimal_places=1, default=0.0, max_digits=4)

class Group(Model):
    name = CharField(max_length=30)
    creator_id = ForeignKey(CUser, on_delete=CASCADE)

class GroupMember(Model):
    group_id = ForeignKey(Group, on_delete=CASCADE)
    member_id = ForeignKey(CUser, on_delete=CASCADE)

class File(Model):
    class FileType(TextChoices):
        DOCUMENT = 'DOC'
        IMAGE = 'IMG'
        TEXT = 'TXT'
        PDF= 'PDF'
        VIDEO = 'VID'
        AUDIO = 'AUD'

    file_name = CharField(max_length=255)
    file_path = CharField(max_length=255)
    file_hash = CharField(max_length=64)
    file_type = CharField(max_length=3, choices=FileType, default=FileType.TEXT)
    file_size = FloatField(default=0.0)
    owner_id = ForeignKey(CUser, on_delete=CASCADE)
    is_folder = BooleanField(db_default=False)
    created_since = DateTimeField(db_default=Now())

class Chunk(Model):
    chunk_type = CharField(max_length=3, choices=File.FileType, default=File.FileType.TEXT)
    chunk_size = FloatField(default=0.0)
    chunk_hash = CharField(max_length=64)

class FileContent(Model):
    file_id = ForeignKey(File, on_delete=CASCADE)
    chunk_id = ForeignKey(Chunk, on_delete=CASCADE)
    chunk_order = IntegerField(db_default=1)

class Trash(Model):
    file_id = ForeignKey(File, on_delete=CASCADE)
    due = DateTimeField(db_default=Now() + timedelta(days=5))

class Device(Model):
    class DeviceType(TextChoices):
        PHONE = 'PHO'
        TABLET = 'TAB'
        LAPTOP = 'LAB'
        DESKTOP = 'DSK'
        OTHER = 'OTH'

    owner_id = ForeignKey(CUser, on_delete=CASCADE)
    name = CharField(max_length=255)
    type = CharField(max_length=3, choices=DeviceType, default=DeviceType.OTHER)

class SyncService(Model):
    device_id = ForeignKey(Device, on_delete=CASCADE)
    created_since = DateTimeField(db_default=Now())