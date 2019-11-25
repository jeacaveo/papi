""" Tests for units.views """
import unittest
from mock import (
    call,
    MagicMock,
    )

from django.urls import reverse
from rest_framework.test import APIRequestFactory

from units.views import LatestUnitVersionViewSet


class LatestUnitVersionCleanTests(unittest.TestCase):
    """ Tests success cases for units.views.LatestUnitVersionViewSet. """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.url = reverse("latestunitversionview-list")
        self.view = LatestUnitVersionViewSet()
        self.queryset_mock = MagicMock()

    def test_no_query(self):
        """ Test queryset when no query params provided. """
        # Given
        request = self.factory.get(self.url, {})
        self.view.request = request
        self.view.queryset = self.queryset_mock
        expected_result = MagicMock()

        self.queryset_mock.filter.return_value = self.queryset_mock
        self.queryset_mock.exclude.return_value = expected_result

        # When
        result = LatestUnitVersionViewSet.get_queryset(self.view)

        # Then
        self.assertEqual(result, expected_result)
        self.queryset_mock.assert_has_calls([
            call.filter(),
            call.exclude(),
            ])

    def test_includes(self):
        """ Test queryset when only includes are provided. """
        # Given
        request = self.factory.get(self.url, {"q": "gold=5"})
        self.view.request = request
        self.view.queryset = self.queryset_mock
        expected_result = MagicMock()

        self.queryset_mock.filter.return_value = self.queryset_mock
        self.queryset_mock.exclude.return_value = expected_result

        # When
        result = LatestUnitVersionViewSet.get_queryset(self.view)

        # Then
        self.assertEqual(result, expected_result)
        self.queryset_mock.assert_has_calls([
            call.filter(gold__icontains=5),
            call.exclude(),
            ])

    def test_excludes(self):
        """ Test queryset when only excludes are provided. """
        # Given
        request = self.factory.get(self.url, {"q": "gold!=5"})
        self.view.request = request
        self.view.queryset = self.queryset_mock
        expected_result = MagicMock()

        self.queryset_mock.filter.return_value = self.queryset_mock
        self.queryset_mock.exclude.return_value = expected_result

        # When
        result = LatestUnitVersionViewSet.get_queryset(self.view)

        # Then
        self.assertEqual(result, expected_result)
        self.queryset_mock.assert_has_calls([
            call.filter(),
            call.exclude(gold__icontains=5),
            ])

    def test_both(self):
        """ Test queryset when both includes and excludes are provided. """
        # Given
        request = self.factory.get(self.url, {"q": "gold=5,gold!=5"})
        self.view.request = request
        self.view.queryset = self.queryset_mock
        expected_result = MagicMock()

        self.queryset_mock.filter.return_value = self.queryset_mock
        self.queryset_mock.exclude.return_value = expected_result

        # When
        result = LatestUnitVersionViewSet.get_queryset(self.view)

        # Then
        self.assertEqual(result, expected_result)
        self.queryset_mock.assert_has_calls([
            call.filter(gold__icontains=5),
            call.exclude(gold__icontains=5),
            ])

    def test_invalid_field(self):
        """
        Test queryset when both includes and excludes are provided,
        and some of the fields are not valid.

        """
        # Given
        request = self.factory.get(
            self.url, {"q": "gold=5,invalid=5,gold!=5,invalid<>5"})
        self.view.request = request
        self.view.queryset = self.queryset_mock
        expected_result = MagicMock()

        self.queryset_mock.filter.return_value = self.queryset_mock
        self.queryset_mock.exclude.return_value = expected_result

        # When
        result = LatestUnitVersionViewSet.get_queryset(self.view)

        # Then
        self.assertEqual(result, expected_result)
        self.queryset_mock.assert_has_calls([
            call.filter(gold__icontains=5),
            call.exclude(gold__icontains=5),
            ])
