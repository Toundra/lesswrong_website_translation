import json
import re
from django.contrib.contenttypes.models import ContentType
import markdown

from wagtail.core.models import Page
from lw.translations.models.book_page import BookPage
from lw.translations.models.translation_index_page import TranslationIndexPage
from lw.translations.models.translation_page import TranslationPage


def patched_save(self, *args, **kwargs):
    self.full_clean()
    self.set_url_path(self.get_parent())
    result = super(Page, self).save(*args, **kwargs)

    return result


class TranslationPageImporter():

    def __init__(self, json_path):
        self.json_path = json_path
        Page.save = patched_save


    def run(self):
        with open(self.json_path) as f:
            json_content = json.load(f)
            translations_list = self.parse(json_content)
            self.bulk_import(translations_list)


    def parse(self, json_content):
        translations_dict = {}
        for field, values in json_content.items():
            for index, value in values.items():
                translation_index = int(index)
                translation_object = translations_dict[translation_index] if translation_index in translations_dict else {}
                translation_object[field] = value
                translations_dict[translation_index] = translation_object

        translations_list = []
        for _, value in translations_dict.items():
            translations_list.append(value)

        return translations_list


    def bulk_import(self, translations_list):
        books = list(BookPage.objects.all())
        translation_index_page = TranslationIndexPage.objects.live()[0]
        created_translations = []
        for translation_json in translations_list:
            parent_id = translation_json['parent_node_id']
            parent_translation = self.find_parent(books, created_translations, translation_index_page, parent_id)

            translation = self.build_translation(translation_json)
            parent_translation.add_child(instance=translation)
            translation.save_revision()

            created_translations.append(translation)


    def find_parent(self, books, created_translations, index_page, parent_id):
        parent_translations = list(filter(lambda x: x.id == parent_id, created_translations))
        if len(parent_translations) > 0:
            return parent_translations[0]

        parent_books = list(filter(lambda x: x.id == parent_id, books))
        if len(parent_books) > 0:
            return parent_books[0]

        return index_page


    def build_translation(self, translation_json):
        translationpage_type = ContentType.objects.get(app_label='translations', model='translationpage')
        slug = self.generate_slug(translation_json['title'])

        html_body = markdown.markdown(translation_json['body_value'], extensions=['md_in_html'])

        translation = TranslationPage(
                id=translation_json['nid'],
                title=translation_json['title'],
                slug=slug,
                content_type=translationpage_type,
                body=html_body,
                author=translation_json['field_author_value'],
                translators=translation_json['field_translators_value'],
                original_link=translation_json['field_original_link_url'],
                rfatz_id=self.parse_rfatz_id(translation_json['field_rfatz_id_value']),
                on_vk=self.parse_vk_value(translation_json['field_on_vk_value']),
                readthesequences_link=translation_json['field_readthesequences_link_url'],
                )

        return translation


    def parse_rfatz_id(self, field_rfatz_id_value):
        if type(field_rfatz_id_value) == int:
            return rfatz_id


    def parse_vk_value(self, field_on_vk_value):
        return field_on_vk_value == 1.0


    def generate_slug(self, title):
        slug = re.sub(r'[:«»_—,?.!+=\(\) \\"]+', '_', title)

        return slug
