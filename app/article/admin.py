from django.contrib import admin
from . import models


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    """ Permite gestionar los artículos de la web
    """
    list_display = ('title', 'slug', 'published', 'is_reviewed')


admin.site.register(models.Tag)
admin.site.register(models.MenuItem)
admin.site.register(models.Menu)
admin.site.register(models.Page)

