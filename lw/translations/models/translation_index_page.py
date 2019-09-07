from django.db import models
from django.http.response import Http404

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.url_routing import RouteResult

from .book_page import BookPage

class TranslationIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        context = super().get_context(request)

        context['books'] = BookPage.objects.child_of(self).live()
        return context

    def route(self, request, path_components):
        if path_components:
            # request is for a child of this page, probably Book or Translation
            child_slug = path_components[0]
            remaining_components = path_components[1:]

            if len(remaining_components):
                raise Http404 # subpages /w/foo/subpage are forbidden

            # is it a book?
            try:
                subpage = BookPage.objects.get(slug=child_slug)
                return subpage.specific.route(request, [])
            except BookPage.DoesNotExist:
                pass

            # is it a translation?
            try:
                subpage = TranslationPage.objects.get(slug=child_slug)
                return subpage.specific.route(request, [])
            except TranslationPage.DoesNotExist:
                pass

            raise Http404
        else:
            if self.live:
                # Return a RouteResult that will tell Wagtail to call
                # this page's serve() method
                return RouteResult(self)
            else:
                # the page matches the request, but isn't published, so 404
                raise Http404


    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]
