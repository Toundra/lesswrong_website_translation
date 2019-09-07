from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel

class TranslationPage(Page):
    body = RichTextField(blank=True)

    field_author = models.CharField(max_length=100)
    field_translators = models.CharField(max_length=100)
    field_original_link = models.CharField(max_length=100)
    field_rfatz_id = models.PositiveSmallIntegerField()
    field_on_vk = models.BooleanField()
    field_readthesequences_link = models.CharField(max_length=100)
    field_rating = models.PositiveSmallIntegerField()

    # field_illustrations
    # field_ref_audio

    content_panels = Page.content_panels + [
        FieldPanel('title'),
        FieldPanel('body', classname="full"),
        FieldPanel('field_author'),
        FieldPanel('field_translators'),
        FieldPanel('field_original_link'),
        FieldPanel('field_rfatz_id'),
        FieldPanel('field_on_vk'),
        FieldPanel('field_readthesequences_link'),
        FieldPanel('field_rating'),
    ]
