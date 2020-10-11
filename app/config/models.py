from django.db import models
from solo.models import SingletonModel
from django.utils.translation import gettext as _
from article.models import SEOAttributes


class SiteConfig(SingletonModel, SEOAttributes):
    """ Representa la configuración del sitio
    """
    maintenance_mode = models.BooleanField(default=False, verbose_name=_('Modo mantenimiento'))

    analytics_id = models.CharField(max_length=50, blank=True, verbose_name=_('ID de Google Analytics'))
    pagination = models.IntegerField(default=25, verbose_name=_('Paginación'))

    class Meta:
        verbose_name = _('Configuración del Sitio')


class AdsConfig(SingletonModel):
    """ Representa la configuración del los espacios
    """
    active_ads = models.BooleanField(verbose_name=_('Activación de Ads'), default=False)
    auto_ads = models.BooleanField(verbose_name=_('Activación de Ads automáticos'), default=False)
    adsense_id = models.CharField(verbose_name=_('ID de Adsense'), max_length=50, blank=True)
    ad_header = models.TextField(verbose_name=_('Espacio superior'), blank=True)
    ad_list = models.TextField(verbose_name=_('Espacio entre elementos de una lista'), blank=True)
    ad_footer = models.TextField(verbose_name=_('Espacio inferior'), blank=True)
    ad_sidebar = models.TextField(verbose_name=_('Espacio lateral'), blank=True)

    class Meta:
        verbose_name = _('Configuración de los espacios')
