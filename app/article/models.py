from django.conf import settings
import time
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext as _
from ckeditor.fields import RichTextField
import re
from django.template.loader import render_to_string
from article.scrapping_objects import Rae, WordReference, Translation

from article.scrapping_objects import WordReference

B_O_V = 'b o v'
C_O_S = 'c o s'
H_O_SIN_HACHE = 'h o sin hache'
LL_O_Y = 'll o y'
G_O_J = 'g o j'
A_O_A_CON_ACENTO = 'a o á'
E_O_E_CON_ACENTO = 'e o é'
I_O_I_CON_ACENTO = 'i o í'
O_O_O_CON_ACENTO = 'o o ó'
U_O_U_CON_ACENTO = 'u o ú'
S_O_X = 's o x'
S_O_Z = 's o z'

conditions = {
    B_O_V: '[vb]{2}',
    H_O_SIN_HACHE: '[h]',
    LL_O_Y: '[ly]{2}',
    C_O_S: '[cs]{2}',
    G_O_J: '[gj]{2}',
    S_O_X: '[sx]{2}',
    S_O_Z: '[sz]{2}',
    A_O_A_CON_ACENTO: '[aá]{2}',
    E_O_E_CON_ACENTO: '[eé]{2}',
    I_O_I_CON_ACENTO: '[ií]{2}',
    O_O_O_CON_ACENTO: '[oó]{2}',
    U_O_U_CON_ACENTO: '[uú]{2}',
}


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
    description = RichTextField(max_length=9999, verbose_name=_('Contenido'), blank=True, null=True)
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


class Page(SEOAttributes, UserBy, DatesAt):
    """ Representa una página del sitio
    """
    title = models.CharField(max_length=100, verbose_name=_('Titulo'))
    content = RichTextField(max_length=50000, verbose_name=_('Contenido'))
    published = models.BooleanField(default=False, verbose_name=_('Publicada'))

    def __str__(self):
        return _('{}'.format(self.slug))

    class Meta:
        verbose_name = _('Página')
        verbose_name_plural = _('Páginas')

    def save(self, *args, **kwargs):
        if not self.id:
            # Only set the slug when the object is created.
            self.slug = slugify(self.title + " " + str(time.time()).split('.')[0])
        super(Page, self).save(*args, **kwargs)


class Article(SEOAttributes, UserBy, DatesAt):
    """ Representan los artículos sobre palabras en la web
    """
    title = models.CharField(max_length=100, verbose_name=_('Titulo'), null=True, blank=True)
    content = RichTextField(max_length=99999, verbose_name=_('Contenido'), null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=False, verbose_name=_('Publicada'),
                                    help_text=_('Para hacerla visible públicamente'))
    is_relevant = models.BooleanField(default=False, verbose_name=_('Relevante'),
                                      help_text=_('Para referenciar su enlace dentro de otros artículos'))
    is_reviewed = models.BooleanField(default=False, verbose_name=_('Revisada'),
                                      help_text=_('Para confirmar su revisión manual'))
    keywords = models.CharField(max_length=100, null=True, blank=True,
                                verbose_name=_('Keywords únicos en el sistema del artículo'))

    joined_chars = None
    splitted_keywords = None
    rule = None

    def generate_title(self):
        return "¿%s?" % self.keywords

    def generate_meta_title(self):
        return "Buscando la palabra correcta: ¿%s?, ¿con %s? " % (
            self.keywords, self.joined_chars)

    def generate_meta_description(self):
        return "¿Estás buscando la palabra correcta entre %s? ¿No sabes si se escribe con %s?. En castellano es una duda más que ..." % (
            self.keywords, self.joined_chars)

    def main_category(self):
        return self.tags.filter(is_category=True).first()

    def __str__(self):
        return _('{}'.format(self.title))

    class Meta:
        verbose_name = _('Articulo')
        verbose_name_plural = _('Articulos')

    @staticmethod
    def keywords_exists(keywords):
        splitted_keywords = Article.split_keywords(keywords)
        regex = r"({0}|{1}) [yo] ({0}|{1})".format(splitted_keywords[0].strip(), splitted_keywords[1].strip())
        return Article.objects.filter(
            keywords__iregex=regex).exists()

    @staticmethod
    def split_keywords(keywords):
        return [str.lower() for str in re.compile(' [yo] ').split(keywords)]

    @staticmethod
    def get_diff_in_keywords(keywords):
        array_a = list(keywords[0])
        array_b = list(keywords[1])
        t = [(a, b) for a, b in zip(array_a, array_b) if a != b]
        if not t:
            raise Exception("Las keywords %s no tienen diferencias" % keywords)
        return t[0]

    def get_rule(self):
        result = ''
        joined_tuple_chars = ''.join(self.tuple_chars)
        for key in conditions:
            expression = conditions[key]
            if re.search(expression, joined_tuple_chars):
                self.rule = result = key
        return result

    def generate_slug(self):
        # Siendo keywords p.e.: Movil o mobil y differences_chars una tuple de las diferencias, en este caso ('b', 'v')
        conditions_with_accents = [A_O_A_CON_ACENTO, E_O_E_CON_ACENTO, I_O_I_CON_ACENTO, O_O_O_CON_ACENTO,
                                   U_O_U_CON_ACENTO]
        rule = self.get_rule()
        result = slugify(self.keywords)
        if rule in conditions_with_accents:
            result += '-con-acento'
        return result

    def generate_chars(self):
        strs_to_split = [" o ", " y "]
        for str_to_split in strs_to_split:
            keywords_splitted = [str.lower() for str in self.keywords.split(str_to_split)]
            if not len(keywords_splitted) > 1:
                continue
            tuple_chars = self.get_diff_in_keywords(keywords_splitted)
            self.tuple_chars = tuple_chars
            self.joined_chars = str_to_split.join(tuple_chars)
            self.splitted_keywords = keywords_splitted
            break

    def generate_content(self):
        definitions = []
        synonymous = []
        translations = []

        for keyword in self.splitted_keywords:
            rae_content = Rae().get_word_definition(keyword)
            definitions.append(rae_content)

            if rae_content:  # La palabra existe
                synonymous.append(WordReference().get_synonymous(keyword))
                translations.append(Translation().get_translations_from_word(keyword))
            else:
                synonymous.append(None)
                translations.append(None)
        # Generate context...
        context = {
           'keywords': self.splitted_keywords,
           'rule': self.rule,
           'definitions': definitions,
           'synonymous': synonymous,
           'translations': translations
        }
        html = render_to_string('article_content.html', context)
        return html

    def generate_tag(self):
        tag, created = Tag.objects.get_or_create(
            name=self.rule, is_category=True
        )
        self.tags.add(tag)

    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.keywords_exists(self.keywords):
                self.generate_chars()
                self.title = self.generate_title()
                self.title_seo = self.generate_meta_title()
                self.description_seo = self.generate_meta_description()
                self.slug = self.generate_slug()
                self.content = self.generate_content()
                super(Article, self).save(*args, **kwargs)
                self.generate_tag()
            else:
                raise Exception("La keyword %s ya existe en DB" % self.keywords)
        else:
            super(Article, self).save(*args, **kwargs)

class MenuItem(models.Model):
    """ Representa los links a mostrar en el menu
    """
    name = models.CharField(max_length=50, verbose_name=_('Nombre'))
    title = models.CharField(max_length=100, verbose_name=_('Atributo Title'), blank=True, null=True)
    link = models.CharField(max_length=150, verbose_name=_('Enlace'), blank=True, null=True)

    object_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, verbose_name=_('Tipo de Objeto'), blank=True,
                                    null=True)
    object_id = models.PositiveIntegerField(verbose_name=_('Id de Objeto'), blank=True, null=True)
    item = GenericForeignKey('object_type', 'object_id')

    def is_post(self):
        return self.item and self.object_type.model_class() is Article

    def is_link(self):
        return not self.item and self.link

    def __str__(self):
        return _('{}'.format(self.name))

    def is_page(self):
        return self.item and self.object_type.model_class() is Page

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
    placement = models.SmallIntegerField(choices=[(k, v) for k, v in PLACEMENT.items()], blank=True,
                                         verbose_name=_('Posición'))
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
