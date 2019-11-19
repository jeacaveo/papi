""" Tests for units.models """
import unittest

from units.models import (
    LatestUnitVersionView,
    )


class LatestUnitVersionViewCleanTests(unittest.TestCase):
    """ Tests success cases for units.models.LatestUnitVersionView model. """

    def test_fields(self):
        """ Tests database fields. """
        # Given
        expected_result = [
            "id", "name", "wiki_path", "image_url", "panel_url",
            "gold", "green", "blue", "red", "energy",
            "attack", "health", "supply", "unit_spell",
            "frontline", "fragile", "blocker", "prompt",
            "stamina", "lifespan", "build_time",
            "exhaust_turn", "exhaust_ability",
            "position", "abilities",
            ]

        # When
        obj = LatestUnitVersionView()
        # pylint: disable=no-member,protected-access
        columns = [column.name for column in obj._meta.concrete_fields]

        # Then
        self.assertEqual(columns, expected_result)

    def test_repr(self):
        """ Tests string representation. """
        # Given
        name = "unit name"
        expected_result = f"{name}"

        # When
        obj = LatestUnitVersionView(name=name)

        # Then
        self.assertEqual(str(obj), expected_result)
