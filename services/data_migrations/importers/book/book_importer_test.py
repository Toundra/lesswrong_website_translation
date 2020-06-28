from django.test import TestCase
from wagtail.core.models import Page

from lw.home.models import HomePage
from lw.translations.models.book_page import BookPage
from lw.translations.models.translation_index_page import TranslationIndexPage

from .book_importer import BookImporter

class BookImporterTest(TestCase):
    def setUp(self):
        home_page = HomePage.objects.live()[0]
        index_page = TranslationIndexPage(intro='', title='title', slug='translation_index_page')
        home_page.add_child(instance=index_page)
        index_page.save_revision().publish()


    def test_import_one_book(self):
        # TODO relative path
        json_path = '/code/services/data_migrations/importers/book/fixtures/one_book.json'
        old_count = BookPage.objects.count()

        BookImporter(json_path).run()

        count = BookPage.objects.count()
        self.assertEqual(old_count + 1, count)


    def test_import_two_books(self):
        # TODO relative path
        json_path = '/code/services/data_migrations/importers/book/fixtures/two_books.json'
        old_count = BookPage.objects.count()

        BookImporter(json_path).run()

        count = BookPage.objects.count()
        self.assertEqual(old_count + 2, count)


    def test_import_child_and_parent_books(self):
        # TODO relative path
        json_path = '/code/services/data_migrations/importers/book/fixtures/child_and_parent.json'
        old_count = BookPage.objects.count()

        BookImporter(json_path).run()

        index_page = TranslationIndexPage.objects.live()[0]
        roots = index_page.get_children()
        self.assertEqual(roots.count(), 1)

        parent_book = roots[0]
        child_books = parent_book.get_children()
        self.assertEqual(child_books.count(), 1)
