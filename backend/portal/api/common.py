from rest_framework import serializers

from dotmap import DotMap


class ObjListSerializer(serializers.ListSerializer):
    @property
    def objects(self):
        return [DotMap(d, _dynamic=False) for d in self.validated_data]


class ModelObjSerializer(serializers.ModelSerializer):
    @property
    def obj(self):
        return DotMap(self.validated_data, _dynamic=False)


class ObjSerializer(serializers.Serializer):
    class Meta:
        list_serializer_class = ObjListSerializer

    @property
    def obj(self):
        return DotMap(self.validated_data, _dynamic=False)


class UnvalidatedField(serializers.Field):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return value
