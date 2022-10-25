from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from alignmentAlgorithms.serializer import InputGlobalLocalSerializer


# Create your views here.

class GlobalView(APIView):
    serializer_class = InputGlobalLocalSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            string1 = serializer.validated_data["string1"]
            string2 = serializer.validated_data["string2"]
            backtracking = serializer.validated_data["backtracking"]

            data = {
                "string1": string1,
                "string2": string2,
                "backtracking": backtracking
            }
            return Response(data)
