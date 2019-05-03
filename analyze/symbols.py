from google.protobuf.descriptor_pb2 import DescriptorProto


class Symbols:
    """
    Container for the purpose of looking up
    other messages and retrieving its DescriptorProto from
    its symbol.

    TODO: testcases for this class. im not sure about that class.
    """

    class Symbol:
        table: Table

        def __init__(self, descriptor, table):
            self.table = table
            self.descriptor = descriptor

    def __init__(self, request):
        self._symbols_dict = self._get_all_symbols(request)

    def lookup(self, name: str, package: str = None):
        if not package:
            lookup_name = name
        else:
            lookup_name = package + '.' + name

        return self._symbols_dict.get(lookup_name)

    def traverse(self, proto_file):
        def _traverse(package, items):
            for item in items:
                with open("file", "w") as f:
                    f.write(str(package))
                yield item, package

                if isinstance(item, DescriptorProto):
                    for enum in item.enum_type:
                        yield enum, package

                    for nested in item.nested_type:
                        nested_package = package + item.name

                        for nested_item in _traverse(nested, nested_package):
                            yield nested_item, nested_package

        # return itertools.chain(
        #     # _traverse(proto_file.package, proto_file.enum_type),
        #     _traverse(proto_file.package, proto_file.message_type),
        # )

        return _traverse(proto_file.package, proto_file.message_type)

    def _get_all_symbols(self, request):
        def _symbols_pairs():
            for proto_file in request.proto_file:
                for message, package in self.traverse(proto_file):
                    yield (package + "." + message.name, Symbols.Symbol(message,
                                                                        table=None))

        return dict(_symbols_pairs())