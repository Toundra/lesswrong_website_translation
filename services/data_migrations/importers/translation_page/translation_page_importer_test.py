from django.test import TestCase
from wagtail.core.models import Page

from lw.home.models import HomePage
from lw.translations.models.book_page import BookPage
from lw.translations.models.translation_index_page import TranslationIndexPage
from lw.translations.models.translation_page import TranslationPage

from .translation_page_importer import TranslationPageImporter


class TranslationPageImporterTest(TestCase):
    def setUp(self):
        home_page = HomePage.objects.live()[0]
        index_page = TranslationIndexPage(intro='', title='title', slug='translation_index_page')
        home_page.add_child(instance=index_page)
        index_page.save_revision().publish()

    def test_import_one_translation_page(self):
        # TODO relative path
        json_path = '/code/services/data_migrations/importers/translation_page/fixtures/translations.json'
        old_count = TranslationPage.objects.count()

        TranslationPageImporter(json_path).run()

        count = TranslationPage.objects.count()
        self.assertEqual(old_count + 1, count)


    def test_import_one_translation_page(self):
        # TODO relative path
        json_path = '/code/services/data_migrations/importers/translation_page/fixtures/translations.json'
        old_count = TranslationPage.objects.count()

        TranslationPageImporter(json_path).run()

        count = TranslationPage.objects.count()
        self.assertEqual(old_count + 1, count)
