"""
REST API view rendering MongoDB time-series measurement data as JSON responses.
"""

from rest_framework.response import Response
from rest_framework.views import APIView

from .repository import MeasurementRepository

repo = MeasurementRepository()


class MeasurementListView(APIView):
    """Returns JSON measurements that can be queried through pymongo"""

    def get(self, request) -> Response:
        source = request.query_params.get("source")
        client_id = request.query_params.get("client_id")
        limit = int(request.query_params.get("limit", 100))

        data = repo.list(source=source, client_id=client_id, limit=limit)
        response = Response(data)

        refresh = int(request.query_params.get("refresh", "5"))
        if refresh > 0:
            response["Refresh"] = str(refresh)

        return response
