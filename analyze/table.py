from typing import Dict

from analyze.database_type import DatabaseType


class Table:
    TableName = str
    TablePackage = str

    EmptyPackage = TablePackage('')

    class Field:
        FieldName = str

        def __init__(self, field_name: FieldName, field_type: DatabaseType, is_table_id: bool):
            self.is_table_id = is_table_id
            self._type = field_type
            self._name = field_name

        @property
        def type(self):
            return self._type

        @property
        def name(self):
            return self._name

    class ReferencingField(Field):
        def __init__(self, referenced_field_name: str, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self._referenced_table = None
            self._referenced_field = None
            self.referenced_field_full_name = referenced_field_name

        def link(self, referenced_field, referenced_table):
            self._referenced_table = referenced_table
            self._referenced_field = referenced_field

        @property
        def referenced_table_name(self) -> str:
            return '.'.join(self.referenced_field_full_name.split('.')[:-1])

        @property
        def referenced_field_name(self) -> str:
            return self.referenced_field_full_name.split('.')[-1]

        @property
        def referenced_table(self):
            return self._referenced_table

        @property
        def referenced_field(self):
            return self._referenced_field

    _fields: Dict[Field.FieldName, Field]

    def __init__(self, table_name: TableName, package: TablePackage, full_name):
        self._full_name = full_name
        self._package = package
        self.table_name = table_name
        self._fields = {}
        self._has_id_field = False

    @property
    def package(self):
        return self._package

    @property
    def full_name(self):
        return self._full_name

    @property
    def fields(self):
        return self._fields.values()

    def add_field(self, field: Field):
        self._fields[field.name] = field

        if field.is_table_id:
            if self._has_id_field:
                # TODO: better error message.
                raise ValueError("{table}: Can't have two table ids".format(table=self.full_name))

            self._has_id_field = True

    def field_by_name(self, name: Field.FieldName) -> Field:
        return self._fields.get(name)

    def is_id_table(self):
        return self._has_id_field
