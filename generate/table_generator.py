from typing import Dict

from analyze.table import Table

FilePath = str
FileContent = str


class TableGenerator:
    def generate_table(self, table: Table) -> Dict[FilePath, FileContent]:
        """
        Generate code files for this table.
        """
        raise NotImplementedError
