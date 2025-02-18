from django.contrib import admin
from .models import MyUser, Publication, Comment


admin.site.register(MyUser)
admin.site.register(Publication)
admin.site.register(Comment)