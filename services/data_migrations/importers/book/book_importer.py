import json
import re
from django.contrib.contenttypes.models import ContentType

from wagtail.core.models import Page
from lw.translations.models.book_page import BookPage
from lw.translations.models.translation_index_page import TranslationIndexPage
from lw.translations.models.translation_page import TranslationPage


def patched_save(self, *args, **kwargs):
    self.full_clean()
    self.set_url_path(self.get_parent())
    result = super(Page, self).save(*args, **kwargs)

    return result


class BookImporter():

    def __init__(self, json_path):
        self.json_path = json_path
        Page.save = patched_save


    def run(self):
        with open(self.json_path) as f:
            json_content = json.load(f)
            books_list = self.parse(json_content)
            self.bulk_import(books_list)


    def parse(self, json_content):
        books_dict = {}
        for field, values in json_content.items():
            for index, value in values.items():
                book_index = int(index)
                book_object = books_dict[book_index] if book_index in books_dict else {}
                book_object[field] = value
                books_dict[book_index] = book_object

        books_list = []
        for _, value in books_dict.items():
            books_list.append(value)

        return books_list


    def bulk_import(self, books_list):
        translation_index_page = TranslationIndexPage.objects.live()[0]
        created_books = []
        for book_json in books_list:
            parent_book_id = book_json['parent_node_id']
            parent_book = self.find_parent(created_books, translation_index_page, parent_book_id)

            book = self.build_book(book_json)
            parent_book.add_child(instance=book)
            book.save_revision()

            created_books.append(book)


    def find_parent(self, created_books, index_page, parent_id):
        parent_book = list(filter(lambda x: x.id == parent_id, created_books))
        if len(parent_book) > 0:
            return parent_book[0]

        return index_page


    def build_book(self, book_json):
        bookpage_type = ContentType.objects.get(app_label='translations', model='BookPage')
        slug = self.generate_slug(book_json['title'])

        book = BookPage(
                id=book_json['nid'],
                title=book_json['title'],
                slug=slug,
                content_type=bookpage_type,
                body=book_json['body_value'],
                author=book_json['field_author_value'],
                translators=book_json['field_translators_value'],
                original_link=book_json['field_original_link_url'],
                rfatz_id=self.parse_rfatz_id(book_json['field_rfatz_id_value']),
                on_vk=self.parse_vk_value(book_json['field_on_vk_value']),
                readthesequences_link=book_json['field_readthesequences_link_url'],
                )

        return book


    def parse_rfatz_id(self, field_rfatz_id_value):
        if type(field_rfatz_id_value) == int:
            return rfatz_id


    def parse_vk_value(self, field_on_vk_value):
        return field_on_vk_value == 1.0


    def generate_slug(self, title):
        slug = re.sub(r'[:«»_—,?.!+= "\\]+', '_', title)

        return slug
