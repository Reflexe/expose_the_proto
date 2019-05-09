#!/usr/bin/env python3
import sys
from google.protobuf.compiler import plugin_pb2 as plugin
from google.protobuf.descriptor_pool import DescriptorPool

from analyze.analyzer import Analyzer
from analyze.table_resolver import TableResolver
from generate.kotlin_exposed.kotlin_exposed_generator import KotlinExposedGenerator
from generate.proto_plugin_response_writer import ProtoPluginResponseWriter


def main():
    # Read request message from stdin
    data = sys.stdin.buffer.read()

    # Parse request
    request = plugin.CodeGeneratorRequest()
    request.ParseFromString(data)

    # Create response
    response = plugin.CodeGeneratorResponse()

    # TODO: clean this part.
    # Generate code
    table_resolver = TableResolver()
    analyzer = Analyzer(table_resolver)

    pool = DescriptorPool()

    for proto_file in request.proto_file:
        pool.Add(proto_file)

        analyzer.generate_tables_for_file(file_descriptor=pool.FindFileByName(proto_file.name))

    analyzer.link_tables_references()

    writer = ProtoPluginResponseWriter()
    writer.write(
        generator=KotlinExposedGenerator(),
        tables=table_resolver.tables,
        plugin_response=response
    )

    # Serialise response message
    output = response.SerializeToString()

    # Write to stdout
    sys.stdout.buffer.write(output)


if __name__ == '__main__':
    main()
