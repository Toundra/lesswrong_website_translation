##!/usr/bin/env python
import os, sys, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lw.core.settings.dev")
django.setup()

from wagtail.core.models import Site, Page
from lw.home.models import HomePage
from lw.translations.models.book_page import BookPage
from lw.translations.models.translation_index_page import TranslationIndexPage
from services.data_migrations.importers.book.book_importer import BookImporter
from services.data_migrations.importers.translation_page.translation_page_importer import TranslationPageImporter

home_page = HomePage.objects.live()[0]

index_page = TranslationIndexPage(intro='', title='Переводы', slug='w')
home_page.add_child(instance=index_page)
index_page.save_revision().publish()

json_path = '/code/services/data_migrations/importers/book/fixtures/one_book.json'
BookImporter(json_path).run()

json_path = '/code/services/data_migrations/importers/translation_page/fixtures/translations.json'
TranslationPageImporter(json_path).run()
