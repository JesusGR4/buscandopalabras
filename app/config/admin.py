from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import SiteConfig, AdsConfig

admin.site.register(SiteConfig, SingletonModelAdmin)
admin.site.register(AdsConfig, SingletonModelAdmin)
