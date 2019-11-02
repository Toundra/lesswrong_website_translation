import json
from django.contrib.contenttypes.models import ContentType

from wagtail.core.models import Page
from lw.translations.models.translation_index_page import TranslationIndexPage
from lw.translations.models.translation_page import TranslationPage


def patched_save(self, *args, **kwargs):
    print('exec patched Page save method')
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
            translation_list = self.parse(json_content)
            self.bulk_import(translation_list)


    def parse(self, json_content):
        translation_list = []
        for item in json_content.items():
            field = item[0]
            values = item[1]
            for index, value in values.items():
                translation_index = int(index)
                translation_json = translation_list[translation_index] if len(translation_list) > translation_index else {}
                translation_json[field] = value
                if len(translation_list) > translation_index:
                    translation_list[translation_index] = translation_json
                else:
                    translation_list.append(translation_json)

        return translation_list


    def bulk_import(self, translation_list):
        translation_index_page = TranslationIndexPage.objects.live()[0]
        created_translations = []
        for translation_json in translation_list:
            parent_translation_id = translation_json['plid']
            parent_translation = self.find_parent(created_translations, translation_index_page, parent_translation_id)

            translation = self.build_translation(translation_json)
            parent_translation.add_child(instance=translation)
            translation.save_revision()

            created_translations.append(translation)


    def find_parent(self, created_translations, index_page, parent_id):
        parent_translation = list(filter(lambda x: x['id'] == parent_id, created_translations))
        if len(parent_translation) > 0:
            return parent_translation[0]

        return index_page


    def build_translation(self, translation_json):
        translationpage_type = ContentType.objects.get(app_label='translations', model='TranslationPage')
        slug = self.generate_slug(translation_json)

        translation = TranslationPage(
                id=translation_json['nid'],
                title=translation_json['title'],
                slug=slug,
                content_type=translationpage_type,
                body=translation_json['body_value'],
                author=translation_json['field_author_value'],
                translators=translation_json['field_translators_value'],
                original_link=translation_json['field_original_link_url'],
                rfatz_id=translation_json['field_rfatz_id_value'],
                on_vk=translation_json['field_on_vk_value'] or False,
                readthesequences_link=translation_json['field_readthesequences_link_url'],
                )

        return translation


    def generate_slug(self, book_json):
        link_title = book_json['link_title']
        slug = link_title.replace(' ', '_')

        return slug
