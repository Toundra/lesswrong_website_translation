select node.vid, field_data_body.body_value
from node
left join field_data_body on field_data_body.entity_id = node.nid
where node.type = 'translation'
limit 10
into OUTFILE '/var/lib/mysql/exports/pages.csv';
--FIELDS ENCLOSED BY '"'
--TERMINATED BY '|||';
--ESCAPED BY '"'
--LINES TERMINATED BY '\r\n';
