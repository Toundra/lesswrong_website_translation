from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel

from wagtailmedia.edit_handlers import MediaChooserPanel

from wagtail.search import index
from django.utils import timezone

class TranslationPage(Page):
    body = RichTextField(blank=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    translators = models.CharField(max_length=100, blank=True, null=True)
    original_link = models.CharField(max_length=100, blank=True, null=True)
    rfatz_id = models.PositiveSmallIntegerField(null=True, blank=True)
    on_vk = models.BooleanField(default=False)
    readthesequences_link = models.CharField(max_length=100, blank=True, null=True)

    audio = models.ForeignKey(
            'wagtailmedia.Media',
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            related_name='+'
            )

    parent_page_types = ['translations.BookPage', 'translations.TranslationIndexPage']
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        FieldPanel('author'),
        FieldPanel('translators'),
        FieldPanel('original_link'),
        FieldPanel('rfatz_id'),
        FieldPanel('on_vk'),
        FieldPanel('readthesequences_link'),
        MediaChooserPanel('audio'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('body'),
        index.FilterField('date'),
    ]

    def get_url_parts(self, *args, **kwargs):
        (site_id, root_url, _) = super().get_url_parts(*args, **kwargs)
        return (site_id, root_url, '/w/' + self.slug)
