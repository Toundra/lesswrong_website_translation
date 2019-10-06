import unittest
from data_migration import DataMigration

class DataMigrationTest(unittest.TestCase):

    def test_generate_sql(self):
        configs = [
            {
                'node_type': 'page',
                'target_table': 'translations_translationindexpage',
                'mapping_fields': [
                    ['id', 'node.vid'],
                    ['text', 'field_data_body.body_value'],
                ],
            },
            {
                'node_type': 'translation',
                'target_table': 'translations_translationpage',
                'mapping_fields': [
                    ['id', 'node.vid'],
                    ['text', 'field_data_body.body_value'],
                ],
            },
            {
                'node_type': 'book',
                'target_table': 'translations_bookpage',
                'mapping_fields': [
                    ['id', 'node.vid'],
                    ['text', 'field_data_body.body_value'],
                ],
            },
        ]

        configs2 = [
            {
                'node_type': 'page',
                'target_table': 'translations_translationindexpage',
                'mapping_fields': [
                    ['page_ptr_id', 'node.vid'],
                    ['intro', 'field_data_body.body_value'],
                ],
            },
            {
                'node_type': 'translation',
                'target_table': 'translations_translationpage',
                'mapping_fields': [
                    ['page_ptr_id', 'node.vid'],
                    ['body', 'field_data_body.body_value'],
                    ['author', 'field_data_field_author.field_author_value'],
                    ['translators', 'field_data_field_translators.field_translators_value'],
                    ['original_link', 'field_data_field_original_link.field_original_link_url'],
                    ['rfatz_id', 'field_data_field_rfatz_id.field_rfatz_id_value'],
                    ['on_vk', 'field_data_field_on_vk.field_on_vk_value'],
                    ['readthesequences_link', 'field_revision_field_readthesequences_link.field_readthesequences_link_url'],
                ],
            },
            {
                'node_type': 'book',
                'target_table': 'translations_bookpage',
                'mapping_fields': [
                    ['page_ptr_id', 'node.vid'],
                    ['body', 'field_data_body.body_value'],
                    ['author', 'field_data_field_author.field_author_value'],
                    ['translators', 'field_data_field_translators.field_translators_value'],
                    ['original_link', 'field_data_field_original_link.field_original_link_url'],
                    ['rfatz_id', 'field_data_field_rfatz_id.field_rfatz_id_value'],
                    ['on_vk', 'field_data_field_on_vk.field_on_vk_value'],
                    ['readthesequences_link', 'field_revision_field_readthesequences_link.field_readthesequences_link_url'],
                ],
            },
        ]

        translation_index_page_insert = "insert into translations_translationindexpage (id,text) select node.vid,field_data_body.body_value from node left join field_data_body on field_data_body.entity_id = node.nid where node.type = 'page';"
        translation_page_insert = "insert into translations_translationpage (id,text) select node.vid,field_data_body.body_value from node left join field_data_body on field_data_body.entity_id = node.nid where node.type = 'translation';"
        translation_book_insert = "insert into translations_bookpage (id,text) select node.vid,field_data_body.body_value from node left join field_data_body on field_data_body.entity_id = node.nid where node.type = 'book';"
        expected_sql = '\n'.join([translation_index_page_insert, translation_page_insert, translation_book_insert])

        actual_sql = DataMigration(configs2).generate_sql()
        print(actual_sql)
        self.assertEqual(expected_sql, actual_sql)


if __name__ == '__main__':
    unittest.main()
