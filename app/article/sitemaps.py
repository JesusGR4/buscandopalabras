
from django.shortcuts import render

from .models import Article, Tag, Page


# Sitemaps

def generate_sitemap_articles(request):
    urls = []

    # Get offers
    articles = Article.objects.filter(published=True)

    for article in articles:
        main_category = article.main_category()
        category_slug = main_category.slug if main_category else None

        if category_slug:
            path = 'palabra/' + category_slug + '/' + article.slug
        else:
            path = 'palabra/' + article.slug

        urls.append({
            'path': path,
            'last_updated': article.updated_at
        })

    return render(request, 'sitemap.xml', {'urls': urls}, content_type='text/xml')


def generate_sitemap_categories(request):
    urls = []

    # Get categories
    categories = Tag.objects.filter(is_category=True)

    for category in categories:
        urls.append({
            'path': 'palabra/' + category.slug,
            'last_updated': category.updated_at
        })

    return render(request, 'sitemap.xml', {'urls': urls}, content_type='text/xml')


def generate_sitemap_pages(request):
    urls = []

    # Get pages
    pages = Page.objects.filter(published=True)

    # Exclude categories pages
    exclude_slugs = ['category-page', 'home']
    categories_slugs = Tag.objects.filter(is_category=True).values_list('slug', flat=True)
    exclude_slugs += categories_slugs

    for page in pages:
        if page.slug in exclude_slugs:
            continue

        if "index" in page.robots_seo and "noindex" not in page.robots_seo:
            urls.append({
                'path': 'p/' + page.slug,
                'last_updated': page.updated_at
            })

    return render(request, 'sitemap.xml', {'urls': urls}, content_type='text/xml')


def sitemap_index_view(request):
    last_updated_date_pages = Page.objects.filter(published=True).order_by('-updated_at').values_list('updated_at', flat=True).first()
    last_updated_date_articles = Article.objects.filter(published=True).order_by('-updated_at').values_list('updated_at', flat=True).first()
    last_updated_date_categories = Tag.objects.filter(is_category=True).order_by('-updated_at').values_list('updated_at', flat=True).first()
    return render(request, 'sitemap_index.xml', {
        'last_updated_date_pages': last_updated_date_pages,
        'last_updated_date_articles': last_updated_date_articles,
        'last_updated_date_categories': last_updated_date_categories,
    }, content_type='text/xml')
