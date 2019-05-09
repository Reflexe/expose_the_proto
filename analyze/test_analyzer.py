import random
import string
from unittest import TestCase

from google.protobuf.descriptor import FieldDescriptor, FileDescriptor, Descriptor

from analyze.analyzer import Analyzer
from analyze.table import Table
from analyze.table_resolver import TableResolver


class TestAnalyzer(TestCase):
    @staticmethod
    def rand_string(max_length=None):
        length = random.randrange(0, max_length)

        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    @staticmethod
    def _create_file_with_message(message):
        file = FileDescriptor(name=TestAnalyzer.rand_string(50),
                              package=TestAnalyzer.rand_string(50),
                              )

        file.message_types_by_name[message.name] = message

        return file

    def _test_field(self, table_field: Table.Field, message_field: FieldDescriptor):
        from analyze.database_type import DatabaseType
        self.assertEqual(DatabaseType.from_protobuf_field(message_field),
                         table_field.type)

        self.assertEqual(table_field.name, message_field.name)
        #self.assertEqual(table_field.)
        #TODO: complete the test.

    def _test_message(self, message: Descriptor):
        table_resolver = TableResolver()
        analyzer = Analyzer(table_resolver)
        analyzer.generate_tables_for_file(self._create_file_with_message(message))

        result = list(table_resolver.tables)
        self.assertTrue(len(result) is 1)

        result_table: Table = result[0]

        # Sort the fields by name.
        def sorted_by_fields_name(fields):
            return fields.sort(key=lambda field: field.name)

        for table_field, message_field in zip(sorted_by_fields_name(result_table.fields),
                                              sorted_by_fields_name(message.fields)):
            self._test_field(table_field, message_field)



    def test_generate_tables_for_file(self):
        self.fail()

    def test_link_tables_references(self):
        self.fail()

