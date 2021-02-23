from django.core.management.base import BaseCommand
from article.models import *
from article.models import Article

class Command(BaseCommand):
    def handle(self, **options):
        first_article = Article.objects.filter(is_reviewed=True, published=False).order_by('order', 'pk').first()
        if first_article:
            first_article.published = True
            first_article.save()