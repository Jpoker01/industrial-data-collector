from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .repository import MeasurementRepository

repo = MeasurementRepository()


class MeasurementListView(APIView):
    def get(self, request):
        source = request.query_params.get("source")
        client_id = request.query_params.get("client_id")
        limit = int(request.query_params.get("limit", 100))
        data = repo.list(source=source, client_id=client_id, limit=limit)
        
        response = Response(data)
        refresh = int(request.query_params.get("refresh", "5"))   # default 5s
        if refresh > 0:
            response["Refresh"] = str(refresh)
        return response