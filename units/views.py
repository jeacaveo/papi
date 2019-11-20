""" Views for papi.units """
# pylint: disable=too-many-ancestors
from rest_framework import viewsets

from units.models import LatestUnitVersionView
from units.serializers import LatestUnitVersionViewSerializer


class LatestUnitVersionViewSet(viewsets.ReadOnlyModelViewSet):  # type: ignore
    """ API endpoint for latest version of a unit. """

    # pylint: disable=no-member
    queryset = LatestUnitVersionView.objects.all().order_by("name")
    serializer_class = LatestUnitVersionViewSerializer
