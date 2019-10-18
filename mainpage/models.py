from django.db import models
from django.contrib import admin


class Picture(models.Model):
    id = models.IntegerField(primary_key=True)
    path = models.CharField(max_length=1000)
    path_thumbnails = models.CharField(max_length=1000)
    name = models.CharField(max_length=1000)


admin.site.register(Picture)
