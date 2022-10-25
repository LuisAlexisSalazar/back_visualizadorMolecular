from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .MatrizGlobal.Meddleman import Matrix, clear_Global
from .MatrizLocal.Meddleman import ClassSmithWaterman, clear_Local  # list_G,G
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
            # NeedlemanWunsch = ClassNeedlemanWunsch(string1, string2, backtracking=backtracking, debug=False)
            # print(string1)
            # print(string2)
            MatrixMeddleman = Matrix(string1, string2, debug=False, backtracking=backtracking)
            MatrixMeddleman.fun(string1, string2)
            MatrixMeddleman.alignments(string1, string2)
            list_per_alignments = MatrixMeddleman.get_aligments()
            clear_Global()
            del MatrixMeddleman
            return Response({'alignments': list_per_alignments})


class LocalView(APIView):
    serializer_class = InputLocalSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            string1 = serializer.validated_data["string1"]
            string2 = serializer.validated_data["string2"]
            NeedlemanWunsch = ClassSmithWaterman(string1, string2)
            NeedlemanWunsch.fun(string1, string2)
            NeedlemanWunsch.alignments(string1, string1)
            list_per_alignments = NeedlemanWunsch.get_aligments()
            del NeedlemanWunsch
            clear_Local()
            # print(G.number_of_nodes())
            # print(len(list_G))
            return Response({'alignments': list_per_alignments})
