from django.db import connection


class FastSync(object):
    def __init__(self, data, id_fieldnames, table_name):
        self.data = data
        self.id_fieldnames = id_fieldnames
        self.table_name = table_name

    def _stringify(self, string):
        if string == 0.0 or string:
            return '\'' + str(string) + '\''
        else:
            return 'NULL'

    def set_fields_sql(self, data_row):
        set_string = []

        for key, value in data_row.items():

            if key not in self.id_fieldnames:
                set_string.append('{}={}'.format(key, self._stringify(value)))

        return ', '.join(set_string)

    def update_sql(self, data_row):
        """
        Create the update sql string with given fields
        :param data_row:
        :return: update_sql_string
        """

        return """
            UPDATE {table_name}
            SET {set_fields}
            WHERE {where_queries};
        """.format(
            table_name=self.table_name,
            set_fields=self.set_fields_sql(data_row),
            where_queries=self.where_sql(data_row)
        )

    def insert_sql(self, data_row):
        """
        Create the insert sql string with given fields
        :param data_row:
        :return: insert_sql_string
        """
        for key, value in data_row.items():
            data_row[key] = self._stringify(value)

        return """
            INSERT INTO {custom_table_name} ({field_names})
            VALUES ({custom_values});
        """.format(
            custom_table_name=self.table_name,
            field_names=', '.join(data_row.keys()),
            custom_values=', '.join(data_row.values()),
        )

    def where_sql(self, data_row):
        where_queries = []

        for id_fieldname in self.id_fieldnames:
            where_queries.append('{}={}'.format(id_fieldname, self._stringify(data_row[id_fieldname])))
        return 'AND'.join(where_queries)

    def select_sql(self, data_row):
        return """
            (SELECT * from {table_name} WHERE {where_queries})
        """.format(
            table_name=self.table_name,
            where_queries=self.where_sql(data_row)
        )

    def iter_sql(self):
        """
        The generator to create the pgsql inline function for the sync command
        :return: sql_string
        """
        for data_row in self.data:
            yield """
            DO $$
            BEGIN
                IF EXISTS {select_sql} THEN
                    {update_sql}
                ELSE
                    {insert_sql}
                END IF;
            END$$;
            """.format(
                select_sql=self.select_sql(data_row),
                update_sql=self.update_sql(data_row),
                insert_sql=self.insert_sql(data_row)
            )

    def start_sync(self):
        """
        Starts to sync the data with the default database
        :return:
        """
        cursor = connection.cursor()
        for sql_string in self.iter_sql():
            cursor.execute(sql_string)
