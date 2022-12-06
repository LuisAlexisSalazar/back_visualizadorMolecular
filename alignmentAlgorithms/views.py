from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .MatrizGlobal.Meddleman import Matrix
from .MatrizLocal.Smith import ClassSmithWaterman
from alignmentAlgorithms.serializer import InputGlobalSerializer, InputLocalSerializer, InputStarSerializer, \
    InputNussinovSerializer
from .AlineamientoStar.Global import MatrixScoreAllString
from .PrediccionEstructuraSecuencial import Nussinov

ADN = "CGAT"
ARN = "CGAU"


def contains_certain_characters(string, characters):
    return all(char in characters for char in string)


# def checkRules(string, rules):
#     list_boolean = []
#     for r in rules:
#         index = string.rfind(r)
#         expr = True if index != -1 else False
#         list_boolean.append(expr)
#     return all(list_boolean)


# https://commons.wikimedia.org/wiki/File:Difference_DNA_RNA-ES.svg
def get_type_string(string):
    isARN = contains_certain_characters(ARN, string)
    isADN = contains_certain_characters(ADN, string)
    isProtein = isARN and isADN

    if isProtein:
        return "Proteina"
    elif isARN:
        return "ARN"
    else:
        return "ADN"


class GlobalView(APIView):
    serializer_class = InputGlobalSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            string1 = serializer.validated_data["string1"].upper()
            string2 = serializer.validated_data["string2"].upper()
            backtracking = serializer.validated_data["backtracking"]
            MatrixMeddleman = Matrix(string1, string2, debug=False, backtracking=backtracking)
            MatrixMeddleman.fun(string1, string2)
            MatrixMeddleman.alignments(string1, string2)
            list_per_alignments = MatrixMeddleman.get_aligments()
            score = MatrixMeddleman.get_score(string1, string2)

            dataResponse = {
                'alignments': list_per_alignments,
                'type_string1': get_type_string(string1),
                'type_string2': get_type_string(string2),
                'len_string1': len(string1),
                'len_string2': len(string2),
                'score': score
            }

            del MatrixMeddleman
            return Response(dataResponse)


class LocalView(APIView):
    serializer_class = InputLocalSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            string1 = serializer.validated_data["string1"].upper()
            string2 = serializer.validated_data["string2"].upper()
            MatrixSmith = ClassSmithWaterman(string1, string2, debug=False)
            MatrixSmith.fun(string1, string2)
            MatrixSmith.alignments(string1, string1)
            list_per_alignments = MatrixSmith.get_aligments()
            score = MatrixSmith.get_score()
            dataResponse = {
                'alignments': list_per_alignments,
                'type_string1': get_type_string(string1),
                'type_string2': get_type_string(string2),
                'len_string1': len(string1),
                'len_string2': len(string2),
                'score': score
            }
            return Response(dataResponse)


class NussinovView(APIView):
    serializer_class = InputNussinovSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            string = serializer.validated_data["string"].upper()

            MatrixNussinov = Nussinov.MatrixNussinov(string, string, debug=False, backtracking=False)
            MatrixNussinov.fun(string, string)
            MatrixNussinov.alignments(string, string)
            sequence, structure = MatrixNussinov.getSecuencePatron()

            dataResponse = {
                'sequence': sequence,
                'structure': structure,
                'len_string': len(string),
                'type': get_type_string(string),
            }

            return Response(dataResponse)


# { "strings": ["ATTGCCATT","ATGGCCATT","ATCCAATTTT","ATCTTCTT","ACTGACC"] }
class StarView(APIView):
    # serializer_class = InputStarSerializer
    # serializer_class = InputLocalSerializer

    def post(self, request):
        strings = self.request.data.get('strings', [])
        temp_strings = []
        for s in strings:
            if s.isalpha():
                temp_strings.append(s)
        strings = temp_strings
        strings = list(map(lambda x: x.upper(), strings))
        types_strings = list(map(lambda x: get_type_string(x), strings))
        # print(strings)
        # print(types_strings)
        listNone = []
        for i in range(len(strings)):
            listNone.append(None)
        data = MatrixScoreAllString(strings, listNone)
        data["types_strings"] = types_strings
        return Response(data)
