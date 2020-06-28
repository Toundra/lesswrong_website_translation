##!/usr/bin/env python
import os, sys, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lw.core.settings.dev")
django.setup()

from lw.translations.models.book_page import BookPage
from lw.translations.models.translation_index_page import TranslationIndexPage

translation_index_page = TranslationIndexPage.objects.first()
translation_index_page.delete()
