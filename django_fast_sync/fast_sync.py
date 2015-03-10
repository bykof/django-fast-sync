from django.db import connection


class FastSync(object):
    def __init__(self, data, id_fieldname, table_name):
        self.data = data
        self.id_fieldname = id_fieldname
        self.table_name = table_name

    def _stringify(self, string):
        if string == 0.0 or string:
            return '\'' + str(string) + '\''
        else:
            return 'NULL'

    def set_fields_sql(self, data_row):
        set_string = []

        for key, value in data_row.items():

            if key != self.id_fieldname:
                set_string.append('{}={}'.format(key, self._stringify(value)))

        return ', '.join(set_string)

    def update_sql(self, data_row):
        """
        Create the update sql string with given fields
        :param data_row:
        :return:
        """

        return """
            UPDATE {table_name}
            SET {set_fields}
            WHERE {id_name}={id};
        """.format(
            table_name=self.table_name,
            set_fields=self.set_fields_sql(data_row),
            id_name=self.id_fieldname,
            id=self._stringify(data_row[self.id_fieldname])
        )

    def insert_sql(self, data_row):
        """
        Create the insert sql string with given fields
        :param data_row:
        :return:
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

    def iter_sql(self):
        """
        The generator to create the pgsql inline function for the sync command
        :return:
        """
        for data_row in self.data:
            yield """
            DO $$
            BEGIN
                IF EXISTS (SELECT * from {table_name} WHERE {id_fieldname}={id}) THEN
                    {update_sql}
                ELSE
                    {insert_sql}
                END IF;
            END$$;
            """.format(
                table_name=self.table_name,
                id_fieldname=self.id_fieldname,
                id=self._stringify(data_row[self.id_fieldname]),
                update_sql=self.update_sql(data_row),
                insert_sql=self.insert_sql(data_row)
            )

    def start_sync(self):
        cursor = connection.cursor()
        for sql_string in self.iter_sql():
            cursor.execute(sql_string)
