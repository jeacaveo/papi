""" Serializers for papi.units """
from rest_framework import serializers

from units.models import LatestUnitVersionView


class LatestUnitVersionViewSerializer(
        serializers.HyperlinkedModelSerializer):  # type: ignore
    """ Main serializer for LatestUnitVersionView model. """

    class Meta:  # pylint: disable=too-few-public-methods
        """ Metadatda for serializer. """
        model = LatestUnitVersionView
        fields = "__all__"
