from django.db import models

from wagtail.core.models import Page
from wagtail.core import fields
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

class HomePage(Page):
    body = fields.RichTextField(blank=True)
    site_areas = fields.StreamField([
        (
            'site_area',
            blocks.StructBlock([
                ('header', blocks.CharBlock(classname='title')),
                ('text', blocks.CharBlock()),
                ('image', ImageChooserBlock()),
            ])
        )
    ], blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        StreamFieldPanel('site_areas'),
    ]
