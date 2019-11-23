""" Tests for units.utils """
import unittest

from units.utils import (
    filter_to_lookup,
    includes_excludes,
    parse_query,
    )


class ParseQueryTests(unittest.TestCase):
    """ Tests all cases for units.utils.parse_query """

    def test_cases(self):
        """ Test all cases. """
        # Given
        data = {
            "multiple": {
                "query": "gold=5, blue!=3,    red>=1,energy:2",
                "expected_result": [
                    ["gold", "=", "5"],
                    ["blue", "!=", "3"],
                    ["red", ">=", "1"],
                    ["energy", ":", "2"],
                    ]
                },
            "single": {
                "query": "gold=5",
                "expected_result": [["gold", "=", "5"]]
                },
            "no_operator": {
                "query": "gold",
                "expected_result": [["gold"]]
                },
            "mixed_end_invalid": {
                "query": "gold=5, 5",
                "expected_result": [["gold", "=", "5"]]
                },
            "mixed_start_invalid": {
                "query": "5, gold=5",
                "expected_result": []
                },
            "mixed_middle_invalid": {
                "query": "gold=5, 1, red!=2",
                "expected_result": [["gold", "=", "5"]]
                },
            "single_empty": {
                "query": "gold=5,",
                "expected_result": [["gold", "=", "5"]]
                },
            "no_value": {
                "query": "gold=",
                "expected_result": [["gold"]]
                },
            "empty": {
                "query": "",
                "expected_result": []
                },
            }

        # When/Then
        for name, params in data.items():
            with self.subTest(name):
                self.assertEqual(
                    list(parse_query(params["query"])),
                    params["expected_result"])


class FilterToDjangoTests(unittest.TestCase):
    """ Tests all cases for units.utils.filter_to_lookup """

    def test_cases(self):
        """ Test all cases. """
        # Given
        data = {
            "equal": {
                "filter": ["name", "=", "drone"],
                "expected_result": {"name__icontains": "drone"},
                },
            "colon": {
                "filter": ["name", ":", "drone"],
                "expected_result": {"name__icontains": "drone"},
                },
            "greater_than": {
                "filter": ["name", ">", "drone"],
                "expected_result": {"name__gt": "drone"},
                },
            "greater_than_or_equal": {
                "filter": ["name", ">=", "drone"],
                "expected_result": {"name__gte": "drone"},
                },
            "less_than": {
                "filter": ["name", "<", "drone"],
                "expected_result": {"name__lt": "drone"},
                },
            "less_than_or_equal": {
                "filter": ["name", "<=", "drone"],
                "expected_result": {"name__lte": "drone"},
                },
            "different_than_1": {
                "filter": ["name", "!=", "drone"],
                "expected_result": {"name__icontains": "drone"},
                },
            "different_than_2": {
                "filter": ["name", "<>", "drone"],
                "expected_result": {"name__icontains": "drone"},
                },
            "number": {
                "filter": ["name", ":", "5"],
                "expected_result": {"name__icontains": 5},
                },
            "empty": {
                "filter": [],
                "expected_result": {},
                },
            "no_value": {
                "filter": ["gold", "="],
                "expected_result": {},
                },
            "too_many": {
                "filter": ["gold", "=", "5", "6"],
                "expected_result": {},
                },
            "bad_operator": {
                "filter": ["gold", "invalid", "5"],
                "expected_result": {},
                },
            }

        # When/Then
        for name, params in data.items():
            with self.subTest(name):
                self.assertEqual(
                    filter_to_lookup(params["filter"]),
                    params["expected_result"])


class IncludesExcludesTests(unittest.TestCase):
    """ Tests all cases for units.utils.inclues_excludes """

    def test_cases(self):
        """ Test all cases. """
        # Given
        data = {
            "includes": {
                "data": "gold=5",
                "expected_result": (
                    {"gold__icontains": 5}, {}),
                },
            "excludes": {
                "data": "gold!=5",
                "expected_result": (
                    {}, {"gold__icontains": 5}),
                },
            "both": {
                "data": "gold=5,gold!=5",
                "expected_result": (
                    {"gold__icontains": 5}, {"gold__icontains": 5}),
                },
            "empty": {
                "data": "",
                "expected_result": ({}, {}),
                },
            }

        # When/Then
        for name, params in data.items():
            with self.subTest(name):
                self.assertEqual(
                    includes_excludes(params["data"]),
                    params["expected_result"])
