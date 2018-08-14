from django.contrib import admin

# Register your models here.

from . import models


admin.site.register(models.Artist)
admin.site.register(models.Album)
admin.site.register(models.Song)
admin.site.register(models.ScrobbleCard)
