##!/usr/bin/env python
import os, sys, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lw.core.settings.dev")
django.setup()

from lw.home.models import HomePage
from lw.translations.models.book_page import BookPage
from lw.translations.models.translation_index_page import TranslationIndexPage
from services.data_migrations.importers.book.book_importer import BookImporter
from services.data_migrations.importers.translation_page.translation_page_importer import TranslationPageImporter
from django.contrib.contenttypes.models import ContentType
from wagtail.core.models import Page


def patched_save(self, *args, **kwargs):
    self.full_clean()
    self.set_url_path(self.get_parent())
    result = super(Page, self).save(*args, **kwargs)

    return result


Page.save = patched_save

home_page = HomePage.objects.live()[0]

index_page_type = ContentType.objects.get(app_label='translations', model='TranslationIndexPage')
index_page = TranslationIndexPage(id=253, intro='', title='Переводы', slug='w', content_type=index_page_type)
home_page.add_child(instance=index_page)
index_page.save_revision().publish()

json_path = '/work/books_lw_dump.json'
BookImporter(json_path).run()

json_path = '/work/translations_lw_dump.json'
TranslationPageImporter(json_path).run()
