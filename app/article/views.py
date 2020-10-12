from django.shortcuts import render
from django.core.paginator import Paginator
from config.models import SiteConfig
from .models import Article, Tag


def home_view(request):
    articles_list = Article.objects.filter(published=True).order_by('-id')
    top_articles = Article.objects.filter(is_relevant=True)
    tags = Tag.objects.filter(is_category=True).order_by('name')

    config = SiteConfig.objects.last()
    pagination = config.pagination if config else 25

    paginator = Paginator(articles_list, pagination)
    page_num = request.GET.get('page')
    articles = paginator.get_page(page_num)

    return render(request, 'home.html', {'articles': articles, 'paginator': paginator,
                                         'top_articles': top_articles, 'tags': tags})


def article_view(request, slug):
    article = Article.objects.get(slug=slug)
    top_articles = Article.objects.filter(is_relevant=True)
    tags = Tag.objects.filter(is_category=True).order_by('name')
    return render(request, 'article.html', {'article': article, 'top_articles': top_articles, 'tags': tags})


def page_view(request):
    pass
