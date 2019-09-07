from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel

from .book_page import BookPage

class TranslationIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        context = super().get_context(request)

        context['books'] = BookPage.objects.child_of(self).live()
        return context

    template = 'translations/index.html'
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]
