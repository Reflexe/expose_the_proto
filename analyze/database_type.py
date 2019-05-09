from google.protobuf.descriptor import FieldDescriptor


class DatabaseType:
    def __init__(self, type: str):
        self._type = type

    @property
    def type(self):
        return self._type

    def __str__(self):
        return self._type

    def __eq__(self, other):
        return self._type == other.type

    # TODO: these are kotlin exposed specific.
    @staticmethod
    def from_protobuf_field(field: FieldDescriptor):
        _CPPTYPE_TO_DATABASE_TYPE = {
            FieldDescriptor.CPPTYPE_DOUBLE: "double",
            FieldDescriptor.CPPTYPE_BOOL: "bool",
            # TODO: handle enum
            FieldDescriptor.CPPTYPE_ENUM: "enum",
            FieldDescriptor.CPPTYPE_FLOAT: "float",
            FieldDescriptor.CPPTYPE_INT32: "integer",
            FieldDescriptor.CPPTYPE_INT64: "integer",
            FieldDescriptor.CPPTYPE_STRING: "string",
            # TODO: should't be unsigned?
            FieldDescriptor.CPPTYPE_UINT32: "integer",
            FieldDescriptor.CPPTYPE_UINT64: "integer",

            # Message should be handled specially and not here.
            # FieldDescriptor.CPPTYPE_MESSAGE: ""
        }

        return DatabaseType(_CPPTYPE_TO_DATABASE_TYPE[field.cpp_type])

