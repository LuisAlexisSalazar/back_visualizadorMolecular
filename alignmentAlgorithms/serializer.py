from rest_framework import serializers


class InputGlobalSerializer(serializers.Serializer):
    string1 = serializers.CharField()
    string2 = serializers.CharField()
    backtracking = serializers.BooleanField()


class InputLocalSerializer(serializers.Serializer):
    string1 = serializers.CharField()
    string2 = serializers.CharField()


class InputNussinovSerializer(serializers.Serializer):
    string = serializers.CharField()


class InputStringSerializer(serializers.Serializer):
    string = serializers.CharField()


class InputStarSerializer(serializers.Serializer):
    strings = serializers.ListField(child=InputStringSerializer())

# class AlignmentSerializer(serializers.ListField):
#     child = serializers.CharField()
#
#
# class ArrayAlignmentGlobalSerializer(serializers.ListField):
#     # child = serializers.CharField()
#     child = AlignmentSerializer()
#
#
# class ArrayAlignmentLocalSerializer(serializers.ListField):
#     child = serializers.CharField()
