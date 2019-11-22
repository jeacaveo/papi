""" Tests for units.utils """
import unittest

from units.utils import (
    parse_query,
    )


class ParseQueryDirtyTests(unittest.TestCase):
    """ Tests fail cases for units.utils.parse_query """

    def test_queries(self):
        """ Test all possible failures. """
        # Given
        data = {
            "mixed_end_invalid": {
                "query": "gold=5, 5",
                "expected_url": [['gold', '=', '5']]
                },
            "mixed_start_invalid": {
                "query": "5, gold=5",
                "expected_url": []
                },
            "mixed_middle_invalid": {
                "query": "gold=5, 1, red!=2",
                "expected_url": [['gold', '=', '5']]
                },
            "single_empty": {
                "query": "gold=5,",
                "expected_url": [['gold', '=', '5']]
                },
            "no_value": {
                "query": "gold=",
                "expected_url": [['gold']]
                },
            "empty": {
                "query": "",
                "expected_url": []
                },
            }

        # When/Then
        for name, params in data.items():
            with self.subTest(name):
                self.assertEqual(
                    list(parse_query(params["query"])),
                    params["expected_url"])


class ParseQueryCleanTests(unittest.TestCase):
    """ Tests success cases for units.models.LatestUnitVersionView model. """

    def test_queries(self):
        """ Test all possible queries. """
        # Given
        data = {
            "multiple": {
                "query": "gold=5, blue!=3,    red>=1,energy:2",
                "expected_url": [
                    ['gold', '=', '5'],
                    ['blue', '!=', '3'],
                    ['red', '>=', '1'],
                    ['energy', ':', '2'],
                    ]
                },
            "single": {
                "query": "gold=5",
                "expected_url": [['gold', '=', '5']]
                },
            "no_operator": {
                "query": "gold",
                "expected_url": [['gold']]
                },
            }

        # When/Then
        for name, params in data.items():
            with self.subTest(name):
                self.assertEqual(
                    list(parse_query(params["query"])),
                    params["expected_url"])
