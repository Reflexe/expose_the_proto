from typing import List

from analyze.table import Table
from generate.table_generator import TableGenerator


class ProtoPluginResponseWriter:
    """
    Helper class that writes #TableGenerator's results
    into a protobuf plugin response.
    """
    @staticmethod
    def _write_files(files_dict, plugin_response):
        for file_path, file_content in files_dict.items():
            file = plugin_response.file.add()
            file.name = file_path
            file.content = file_content

    def write(self, generator: TableGenerator, tables: List[Table], plugin_response):
        for table in tables:
            files = generator.generate_table(table)
            self._write_files(files, plugin_response)