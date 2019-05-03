class Table:
    class Field:
        def __init__(self, field_name: str, field_type: str):
            self.field_type = field_type
            self.field_name = field_name

    def __init__(self):
        self._fields = []

    def add_field(self, field: Field):
        self._fields.append(field)

    class ReferencingField(Field):
        def __init__(self, referenced_field, referenced_table, *args):
            super().__init__(*args)

            self.referenced_field = referenced_field
            self.referenced_table = referenced_table