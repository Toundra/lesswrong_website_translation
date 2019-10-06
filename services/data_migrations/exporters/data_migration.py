class DataMigration():

    def __init__(self, configs):
        self.configs = configs

    def generate_sql(self):
        operations = []

        for config in self.configs:
            operation = self.generate_sql_for(config)
            operations.append(operation)

        common_sql = '\n'.join(operations)

        return common_sql


    def generate_sql_for(self, config):
        select_sql = self.generate_select_sql(config)
        insert_sql = self.generate_insert_sql(select_sql, config)

        return insert_sql


    def generate_select_sql(self, config):
        node_type = config['node_type']
        select_sql, join_sql = self.prepare_clauses(config)
        sql = "select {select_sql} from node {join_sql} where node.type = '{node_type}';".format(
            select_sql=select_sql,
            join_sql=join_sql,
            node_type=node_type,
        )

        return sql


    def prepare_clauses(self, config):
        mapping_fields = config['mapping_fields']
        select_clauses = []
        join_clauses = []

        for _, origin_field in mapping_fields:
            origin_table = origin_field.split('.')[0]
            join_sql = "left join {origin_table} on {origin_table}.entity_id = node.nid".format(origin_table=origin_table)
            join_clauses.append(join_sql) if origin_table != 'node' else None
            select_clauses.append(origin_field)

        select_sql = ','.join(select_clauses)
        join_sql = ' '.join(join_clauses)

        return select_sql, join_sql


    def generate_insert_sql(self, select_sql, config):
        node_type = config['node_type']
        target_table = config['target_table']
        mapping_fields = config['mapping_fields']
        target_fields = []

        for target_field, _ in mapping_fields:
            target_fields.append(target_field)

        target_fields_sql = ','.join(target_fields)

        sql = "insert into {target_table} ({target_fields_sql}) {select_sql}".format(
            target_table=target_table,
            target_fields_sql=target_fields_sql,
            select_sql=select_sql,
        )

        return sql
