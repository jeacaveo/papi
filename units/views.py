""" Views for papi.units """
# pylint: disable=too-many-ancestors
from django.db.models import QuerySet
from rest_framework import viewsets

from units.models import LatestUnitVersionView
from units.serializers import LatestUnitVersionViewSerializer
from units.utils import includes_excludes


class LatestUnitVersionViewSet(viewsets.ReadOnlyModelViewSet):  # type: ignore
    """
    API endpoint for latest version of each unit.

    Sample query:

    /api/latest/units/?q=gold>3,frontline=true,abilities="gain X",name!=head

    """

    # pylint: disable=no-member
    queryset = LatestUnitVersionView.objects.filter()
    serializer_class = LatestUnitVersionViewSerializer

    def get_queryset(self) -> QuerySet:
        """
        Custom filtering.

        Split filters into includes and excludes depeding on the operator

        """
        includes, excludes = includes_excludes(self.request.GET.get("q") or "")
        return self.queryset.filter(**includes).exclude(**excludes)
