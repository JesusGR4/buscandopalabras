from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import render
from django.template import Context, Template
from config.models import SiteConfig
from .models import Article, Tag, Page


def home_view(request):
    page = Page.objects.filter(published=True, slug='home').first()
    articles_list = Article.objects.filter(published=True).order_by('-updated_at')
    top_articles = Article.objects.filter(is_relevant=True)
    tags = Tag.objects.filter(is_category=True).order_by('name')

    config = SiteConfig.objects.last()
    pagination = config.pagination if config else 25

    paginator = Paginator(articles_list, pagination)
    page_num = request.GET.get('page')
    articles = paginator.get_page(page_num)

    return render(request, 'home.html', {'articles': articles, 'paginator': paginator,
                                         'top_articles': top_articles, 'tags': tags, 'page': page})


def article_view(request, category, slug):
    """ Get article and show it
     """
    article = Article.objects.get(slug=slug)
    top_articles = Article.objects.filter(is_relevant=True).exclude(pk=article.pk)
    tags = Tag.objects.filter(is_category=True).order_by('name')
    return render(request, 'article.html', {'article': article, 'top_articles': top_articles, 'tags': tags})


def category_view(request, category):
    """ Get category and show it
    """

    if not Tag.objects.filter(slug=category).exists():
        # Show 404 page if slug does not exists!
        return HttpResponseNotFound('<h1>Not found</h1>')

    page = Page.objects.filter(slug=category).first()

    if not page:
        page = Page.objects.get(slug='category-page')

    tags = Tag.objects.filter(is_category=True).order_by('name')
    article_list = Article.objects.filter(published=True, tags__slug=category).order_by('-id')

    config = SiteConfig.objects.last()
    pagination = config.pagination if config else 25

    paginator = Paginator(article_list, pagination)
    top_articles = Article.objects.filter(is_relevant=True)

    page_num = request.GET.get('page')
    articles = paginator.get_page(page_num)

    # inject attributes
    page = inject_context(page, {'tag': Tag.objects.filter(slug=category).first()})

    return render(request, 'home.html', {
        'page': page, 'articles': articles, 'paginator': paginator,
        'top_articles': top_articles, 'tags': tags,
    })


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



# Aux


def inject_context(page, context):
    """ Evaluate context variables into string fields
    :param page: page to inject
    :param context: context variables
    :return:
    """
    all_fields = Page._meta.get_fields()
    for field in all_fields:
        attr_name = field.name
        res = getattr(page, attr_name)
        if Page._meta.get_field(attr_name).get_internal_type() in ['CharField', 'TextField'] and res:
            t = Template(res)
            res = t.render(Context(context))
        setattr(page, attr_name, res)
    return page
