import json
import pymysql
import sqlalchemy
import pandas as pd

host = 'db'
port = '3306'
username = 'root'
password = ''
db_name = 'lw_old'
outfolder = '/home/jovyan/work/'
books_outfile_name = 'books_lw_dump.json'
translations_outfile_name = 'translations_lw_dump.json'
constring = f'''mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}'''

engine = sqlalchemy.create_engine(constring)

sql = '''select
    distinct node.nid,
    node.title,
	node.vid,
	field_data_body.body_value,
	field_data_field_author.field_author_value,
	field_data_field_translators.field_translators_value,
	field_data_field_original_link.field_original_link_url,
	field_data_field_rfatz_id.field_rfatz_id_value,
	field_data_field_on_vk.field_on_vk_value,
	field_revision_field_readthesequences_link.field_readthesequences_link_url,
    node.created,
    menu_links.plid
from
	node
	left join field_data_body on field_data_body.entity_id = node.nid
	left join field_data_field_author on field_data_field_author.entity_id = node.nid
    left join field_data_field_translators on field_data_field_translators.entity_id = node.nid
    left join field_data_field_original_link on field_data_field_original_link.entity_id = node.nid
    left join field_data_field_rfatz_id on field_data_field_rfatz_id.entity_id = node.nid
    left join field_data_field_on_vk on field_data_field_on_vk.entity_id = node.nid
	left join field_revision_field_readthesequences_link on field_revision_field_readthesequences_link.entity_id = node.nid
    left join book on book.nid = node.nid
    left join menu_links on menu_links.mlid = book.mlid
where
	node.type = 'translation';'''

sql = sqlalchemy.text(sql)
translations = pd.read_sql(sql, engine)


sql = '''select
	distinct node.nid,
    node.title,
    node.vid,
	field_data_body.body_value,
	field_data_field_author.field_author_value,
	field_data_field_translators.field_translators_value,
	field_data_field_original_link.field_original_link_url,
	field_data_field_rfatz_id.field_rfatz_id_value,
	field_data_field_on_vk.field_on_vk_value,
	field_revision_field_readthesequences_link.field_readthesequences_link_url,
	node.created,
    menu_links.plid
from
	node
	left join field_data_body on field_data_body.entity_id = node.nid
	left join field_data_field_author on field_data_field_author.entity_id = node.nid
	left join field_data_field_translators on field_data_field_translators.entity_id = node.nid
	left join field_data_field_original_link on field_data_field_original_link.entity_id = node.nid
	left join field_data_field_rfatz_id on field_data_field_rfatz_id.entity_id = node.nid
	left join field_data_field_on_vk on field_data_field_on_vk.entity_id = node.nid
	left join field_revision_field_readthesequences_link on field_revision_field_readthesequences_link.entity_id = node.nid
    left join book on book.nid = node.nid
    left join menu_links on menu_links.mlid = book.mlid
where
        node.type = 'book';'''

sql = sqlalchemy.text(sql)
books = pd.read_sql(sql, engine)

translations.to_json(outfolder + translations_outfile_name)
books.to_json(outfolder + books_outfile_name)
