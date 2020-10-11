from django.urls import path, include
from article.views import home_view, article_view, page_view

urlpatterns = [
    path('', home_view),
    path('palabra/<slug:slug>/', article_view),
    path('p/<slug:slug>/', page_view),
]