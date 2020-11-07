from django.urls import path
from article.views import home_view, article_view, page_view, category_view
from .sitemaps import generate_sitemap_pages, generate_sitemap_articles, generate_sitemap_categories, sitemap_index_view

urlpatterns = [
    path('', home_view),
    path('palabra/<category>/<slug:slug>/', article_view),
    path('palabra/<category>/', category_view),
    path('p/<slug:slug>/', page_view),
    path('sitemap_pages.xml', generate_sitemap_pages),
    path('sitemap_articles.xml', generate_sitemap_articles),
    path('sitemap_categories.xml', generate_sitemap_categories),
    path('sitemap_index.xml', sitemap_index_view),
]