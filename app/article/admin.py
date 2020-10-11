from django.contrib import admin
from . import models

admin.site.register(models.Tag)
admin.site.register(models.Article)
admin.site.register(models.MenuItem)
admin.site.register(models.Menu)
admin.site.register(models.Page)

