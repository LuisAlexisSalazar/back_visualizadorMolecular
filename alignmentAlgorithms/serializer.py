from abc import ABC

from rest_framework import serializers


class InputGlobalLocalSerializer(serializers.Serializer, ABC):
    string1 = serializers.CharField()
    string2 = serializers.CharField()
    backtracking = serializers.BooleanField()


class AlignmentSerializer(serializers.ListField):
    child = serializers.CharField()


class ArrayAlignmentGlobalSerializer(serializers.ListField):
    # child = serializers.CharField()
    child = AlignmentSerializer(many=True)


class ArrayAlignmentLocalSerializer(serializers.ListField):
    child = serializers.CharField()
