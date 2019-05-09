from typing import List, Tuple

from analyze.table import Table
from analyze.table_resolver import TableResolver


class TableLinker:
    def __init__(self,
                 table_resolver: TableResolver,
                 unresolved_fields: List[Tuple[Table, Table.ReferencingField]]):
        self._table_resolver = table_resolver
        self._unresolved_fields = unresolved_fields

    def link(self):
        """
        "Link" a referencing field.

        After we've done analyzing and creating Table and Field objects
        for every message, we still have to fill up ReferencedField's
        table and field objects from the field's string option.

        We could not do that previously, because we might try to look
        for a table that wasn't analyzed yet.
        """
        for referencing_table, referencing_field in self._unresolved_fields:
            # Parse and resolve the table in the "references" option.
            # FIXME: error with unresolved references.
            referenced_table = self._table_resolver.lookup_by_name(referencing_field.referenced_table_name).table
            referenced_field = referenced_table.field_by_name(referencing_field.referenced_field_name)

            # Ok, we've found the referenced fields.
            # Now, let's make sure it is valid.
            self._process_link_field_validations(referencing_field, referencing_table,
                                                 referenced_field, referenced_table)

            # Ok, link it.
            referencing_field.link(referenced_field, referenced_table)

    @staticmethod
    def _process_link_field_validations(referencing_field: Table.ReferencingField,
                                        referencing_table: Table,
                                        referenced_field: Table.Field,
                                        referenced_table: Table):
        if referenced_field.type != referencing_field.type:
            raise ValueError("{referencing_type} \"{referencing_table}.{referencing_field}\" referenced to "
                             "{referenced_type} \"{referencing_table}.{referenced_field}\" but "
                             "has a different value type.".format(
                referencing_field=referencing_field.name,
                referencing_table=referencing_table.full_name,
                referenced_field=referenced_field.name,
                referenced_table=referenced_table.full_name,
                referenced_type=referenced_field.type,
                referencing_type=referencing_field.type
            ))
