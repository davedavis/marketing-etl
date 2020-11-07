import json
import google


class GoogleProtoEncoder(json.JSONEncoder):
    """
    Custom JSON Encoder for GoogleAdsRow.

    Usage: json.dumps(data, cls=GoogleProtoEncoder)
    """


def default(self, obj):
    """
    Overriden method. When json.dumps() is called, it actually calls this method if
    this class is specified as the encoder in json.dumps() e.g: json.dumps(data, cls=GoogleProtoEncoder).
    """
    if isinstance(obj, google.protobuf.message.Message) and hasattr(obj, 'value'):
        # This covers native data types such as string, int, float etc
        return obj.value

    elif isinstance(obj, google.protobuf.pyext._message.RepeatedCompositeContainer):
        # This is basically for python list and tuples
        data = []
        try:
            while True:
                item = obj.pop()
                data.append(self.default(item))
        except IndexError:
            return data

    elif isinstance(obj, google.ads.google_ads.v1.proto.common.custom_parameter_pb2.CustomParameter):
        # Equivalent to python dictionary
        return {
            self.default(obj.key): self.default(obj.value)
        }

    elif isinstance(obj, google.protobuf.message.Message):
        # All the other wrapper objects which can have different fields.
        return {key[0].name: getattr(obj, key[0].name) for key in obj.ListFields()}

    return json.JSONEncoder.default(self, obj)
