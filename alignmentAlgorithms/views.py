from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .MatrizGlobal.Meddleman import Matrix
from .MatrizLocal.Smith import ClassSmithWaterman
from alignmentAlgorithms.serializer import InputGlobalSerializer, InputLocalSerializer


# Create your views here.

class GlobalView(APIView):
    serializer_class = InputGlobalSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            string1 = serializer.validated_data["string1"]
            string2 = serializer.validated_data["string2"]
            backtracking = serializer.validated_data["backtracking"]
            MatrixMeddleman = Matrix(string1, string2, debug=True, backtracking=backtracking)
            MatrixMeddleman.fun(string1, string2)
            MatrixMeddleman.alignments(string1, string2)
            list_per_alignments = MatrixMeddleman.get_aligments()
            # clear_Global()
            del MatrixMeddleman
            return Response({'alignments': list_per_alignments})


class LocalView(APIView):
    serializer_class = InputLocalSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            string1 = serializer.validated_data["string1"]
            string2 = serializer.validated_data["string2"]
            MatrixSmith = ClassSmithWaterman(string1, string2, debug=False)
            MatrixSmith.fun(string1, string2)
            MatrixSmith.alignments(string1, string1)
            list_per_alignments = MatrixSmith.get_aligments()
            return Response({'alignments': list_per_alignments})
