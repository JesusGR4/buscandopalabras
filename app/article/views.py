from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.core.paginator import Paginator
from config.models import SiteConfig
from .models import Article, Tag, Page


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
    """ Get article and show it
     """
    article = Article.objects.get(slug=slug)
    top_articles = Article.objects.filter(is_relevant=True).exclude(pk=article.pk)
    tags = Tag.objects.filter(is_category=True).order_by('name')
    return render(request, 'article.html', {'article': article, 'top_articles': top_articles, 'tags': tags})


def page_view(request, slug):
    """ Get page and show it
    """
    if not Page.objects.filter(published=True, slug=slug).exists():
        # Show 404 page if slug does not exists!
        return HttpResponseNotFound('<h1>Not found</h1>')

    top_articles = Article.objects.filter(is_relevant=True)
    tags = Tag.objects.filter(is_category=True).order_by('name')

    page = Page.objects.get(slug=slug)

    return render(request, 'page.html', {'page': page, 'top_articles': top_articles, 'tags': tags})
