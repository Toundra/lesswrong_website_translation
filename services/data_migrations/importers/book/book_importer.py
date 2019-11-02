import json
from django.contrib.contenttypes.models import ContentType

from wagtail.core.models import Page
from lw.translations.models.book_page import BookPage
from lw.translations.models.translation_index_page import TranslationIndexPage
from lw.translations.models.translation_page import TranslationPage
from django.conf import settings

WAGTAIL_ALLOW_UNICODE_SLUGS = True

def patched_save(self, *args, **kwargs):
    print('exec patched Page save method')
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
            book_list = self.parse(json_content)
            self.bulk_import(book_list)


    def parse(self, json_content):
        book_list = []
        for item in json_content.items():
            field = item[0]
            values = item[1]
            for index, value in values.items():
                book_index = int(index)
                book_json = book_list[book_index] if len(book_list) > book_index else {}
                book_json[field] = value
                if len(book_list) > book_index:
                    book_list[book_index] = book_json
                else:
                    book_list.append(book_json)

        return book_list


    def bulk_import(self, book_list):
        translation_index_page = TranslationIndexPage.objects.live()[0]
        created_books = []
        for book_json in book_list:
            parent_book_id = book_json['plid']
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
        slug = self.generate_slug(book_json)

        book = BookPage(
                id=book_json['nid'],
                title='book',
                slug=slug,
                content_type=bookpage_type,
                body=book_json['body_value'],
                author=book_json['field_author_value'],
                translators=book_json['field_translators_value'],
                original_link=book_json['field_original_link_url'],
                rfatz_id=book_json['field_rfatz_id_value'],
                on_vk=book_json['field_on_vk_value'] or False,
                readthesequences_link=book_json['field_readthesequences_link_url'],
                )

        return book


    def generate_slug(self, book_json):
        link_title = book_json['link_title']
        formatted_link_title = link_title.replace(' ', '_')
        slug = '{link_title}'.format(link_title=formatted_link_title)

        return slug
