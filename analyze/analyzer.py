from typing import List, Tuple

from google.protobuf.descriptor import FileDescriptor, Descriptor, FieldDescriptor
from google.protobuf.descriptor_pb2 import MessageOptions

from analyze.database_type import DatabaseType
from analyze.table import Table
from analyze.table_resolver import TableResolver
from proto import options_pb2


class Analyzer:
    """
    Parse messages and generate Tables from them.
    """
    _unresolved_referencing_fields: List[Tuple[Table, Table.ReferencingField]]

    def __init__(self, table_resolver: TableResolver):
        self._unresolved_referencing_fields = []
        self._table_resolver = table_resolver

    def _add_field_to_table(self, table: Table, field: Table.Field):
        if isinstance(field, Table.ReferencingField):
            self._unresolved_referencing_fields.append((table, field))

        table.add_field(field)

    def _add_message(self, message: Descriptor):
        new_table = Table(message.name, message.file.package, message.full_name)

        for field in message.fields:
            field_parameters = dict(
                field_name=field.name,
                field_type=DatabaseType.from_protobuf_field(field),
                is_table_id=self._is_id_field(field)
            )

            references_option = self._get_field_references_option(field)

            if references_option:
                table_field_type = Table.ReferencingField
                field_parameters['referenced_field_name'] = references_option
            else:
                table_field_type = Table.Field

            self._add_field_to_table(new_table, table_field_type(**field_parameters))

        self._table_resolver.assign(message, new_table)

    def generate_tables_for_file(self, file_descriptor: FileDescriptor):
        for message in file_descriptor.message_types_by_name.values():
            options: MessageOptions = message.GetOptions()
            # Skip messages with the no is table option.

            if not options.Extensions[options_pb2.table]:
                continue

            self._add_message(message)

    def link_tables_references(self):
        from analyze.table_linker import TableLinker
        linker = TableLinker(self._table_resolver, self._unresolved_referencing_fields)
        linker.link()

    def _is_id_field(self, field: FieldDescriptor) -> bool:
        return self._get_field_option(field, options_pb2.id, False)

    def _get_field_references_option(self, field: FieldDescriptor) -> str:
        return self._get_field_option(field, options_pb2.references, '')

    @staticmethod
    def _get_field_option(field: FieldDescriptor, option, default_value):
        options: MessageOptions = field.GetOptions()

        if options.HasExtension(option):
            return options.Extensions[option]
        else:
            return default_value
