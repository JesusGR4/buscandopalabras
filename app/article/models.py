from django.conf import settings
import time
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext as _
from ckeditor.fields import RichTextField


class SEOAttributes(models.Model):
    """ Representa una clase genérica para actualizar información de SEO
    """
    title_seo = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Título del sitio (SEO)'))
    description_seo = models.TextField(null=True, blank=True, verbose_name=_('Descripción del sitio (SEO)'))
    keywords_seo = models.TextField(null=True, blank=True, verbose_name=_('Keywords del sitio (SEO)'))
    slug = models.SlugField(_('slug (SEO)'), max_length=60, null=True, blank=True, unique=True)
    robots_seo = models.TextField(null=True, blank=True, verbose_name=_('Robots (SEO)'))

    class Meta:
        abstract = True


class DatesAt(models.Model):
    """ Representa una clase genérica para controlar la creación y actualización de los objetos.
    """
    created_at = models.DateTimeField(
        verbose_name=_('Creado el'), auto_now_add=True
    )

    updated_at = models.DateTimeField(
        verbose_name=_('Actualizado el'), auto_now=True
    )

    class Meta:
        abstract = True


class UserBy(models.Model):
    """ Representa una clase genérica para controlar las acciones de los usuarios sobre objetos.
    """
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('Crea'), on_delete=models.PROTECT,
        null=True, blank=True, related_name='+', help_text=_('Quien lo crea')
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('Actualiza'), on_delete=models.PROTECT,
        null=True, blank=True, related_name='+', help_text=_('El último que lo actualizo')
    )

    class Meta:
        abstract = True


class Tag(UserBy, DatesAt):
    """ Representan etiquetas para los articulos

        Una etiequeta puede ser a la vez una categoría en la web
    """
    name = models.CharField(verbose_name=_('Nombre'), max_length=50)
    slug = models.CharField(verbose_name=_('Slug'), max_length=50, blank=True, unique=True)
    description = RichTextField(max_length=9999, verbose_name=_('Contenido'),  blank=True, null=True)
    is_category = models.BooleanField(verbose_name=_('Es categoría?'), default=False)

    def __str__(self):
        return _('{}'.format(self.name))

    class Meta:
        verbose_name = _('Etiqueta')
        verbose_name_plural = _('Etiquetas')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)


class Article(SEOAttributes, UserBy, DatesAt):
    """ Representan los artículos sobre palabras en la web
    """
    title = models.CharField(max_length=100, verbose_name=_('Titulo'))
    content = RichTextField(max_length=9999, verbose_name=_('Contenido'))
    tags = models.ManyToManyField(Tag)
    published = models.BooleanField(default=False, verbose_name=_('Publicada'), help_text=_('Para hacerla visible públicamente'))
    is_relevant = models.BooleanField(default=False, verbose_name=_('Relevante'), help_text=_('Para referenciar su enlace dentro de otros artículos'))
    
    def main_category(self):
        return self.tags.filter(is_category=True).first()

    def __str__(self):
        return _('{}'.format(self.title))

    class Meta:
        verbose_name = _('Articulo')
        verbose_name_plural = _('Articulos')

    def save(self, *args, **kwargs):
        if not self.id:
            # Only set the slug when the object is created.
            self.slug = slugify(self.title + " " + str(time.time()).split('.')[0])
        super(Article, self).save(*args, **kwargs)


class MenuItem(models.Model):
    """ Representa los links a mostrar en el menu
    """
    name = models.CharField(max_length=50, verbose_name=_('Nombre'))
    title = models.CharField(max_length=100, verbose_name=_('Atributo Title'), blank=True, null=True)
    link = models.CharField(max_length=150, verbose_name=_('Enlace'), blank=True, null=True)

    object_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, verbose_name=_('Tipo de Objeto'), blank=True, null=True)
    object_id = models.PositiveIntegerField(verbose_name=_('Id de Objeto'), blank=True, null=True)
    item = GenericForeignKey('object_type', 'object_id')

    def is_post(self):
        return self.item and self.object_type.model_class() is Article

    def is_link(self):
        return not self.item and self.link

    def __str__(self):
        return _('{}'.format(self.name))

    class Meta:
        verbose_name = _('Elemento de Menú')
        verbose_name_plural = _('Elementos de Menú')


class Menu(UserBy, DatesAt):
    """ Representa los menus de la página
    """
    FOOTER = 0
    HEADER = 1
    SIDEBAR = 2

    PLACEMENT = {
        HEADER: _('Cabecera'),
        FOOTER: _('Pie de página'),
        SIDEBAR: _('Barra lateral')
    }

    name = models.CharField(max_length=100, verbose_name=_('Nombre'))
    placement = models.SmallIntegerField(choices=[(k, v) for k, v in PLACEMENT.items()], blank=True, verbose_name=_('Posición'))
    is_active = models.BooleanField(default=False, verbose_name=_('Activado'))
    items = models.ManyToManyField(MenuItem)

    def __str__(self):
        return _('{}'.format(self.name))

    class Meta:
        verbose_name = _('Menú')
        verbose_name_plural = _('Menús')

    def save(self, *args, **kwargs):
        if self.is_active:
            Menu.objects.filter(is_active=True, placement=self.placement).update(is_active=False)
        super(Menu, self).save(*args, **kwargs)
