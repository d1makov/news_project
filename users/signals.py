from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from news_blog.blog.models import Post, Comment
from .models import CustomUser


def populate_models(sender, **kwargs):
    users = Group.objects.get_or_create(name="Users")
    stuff = Group.objects.get_or_create(name="Editors")
    admins = Group.objects.get_or_create(name="Administrators")

    content_type = ContentType.objects.get_for_model(CustomUser)
    add, change, delete, view = Permission.objects.filter(content_type=content_type).all()
    admins.permissions.add(add, delete, change, view)

    content_type = ContentType.objects.get_for_model(Comment)
    add, change, delete, view = Permission.objects.filter(content_type=content_type).all()
    stuff.permissions.add(delete, change, view)
    admins.permissions.add(delete, change, view)

    content_type = ContentType.objects.get_for_model(Post)
    add, change, delete, view = Permission.objects.filter(content_type=content_type).all()
    users.permissions.add(add, view)
    stuff.permissions.add(add, change, view)
    admins.permissions.add(add, change, delete, view)