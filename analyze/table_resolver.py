from typing import Dict

from google.protobuf.descriptor import Descriptor

from analyze.table import Table

# TODO: rename to table database
class TableResolver:
    """
    Container for resolving Tables from messages.
    (for linking purposes)
    """

    class Entry:
        table: Table

        def __init__(self, descriptor: Descriptor, table):
            self.table = table
            self.descriptor = descriptor

    _symbols_dict: Dict[str, Entry]

    def __init__(self):
        self._symbols_dict = {}

    def lookup(self, descriptor: Descriptor):
        return self._symbols_dict.get(descriptor.full_name)

    def lookup_by_name(self, name: str):
        return self._symbols_dict.get(name)

    def assign(self, descriptor: Descriptor, table: Table):
        self._symbols_dict[descriptor.full_name] = self.Entry(descriptor, table)

    @property
    def tables(self):
        return (entry.table for entry in self._symbols_dict.values())
