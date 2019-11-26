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
            "underscore": {
                "query": "some_field",
                "expected_result": [["some_field"]]
                },
            "spaces": {
                "query": "name=double quoted",
                "expected_result": [["name", "=", "double quoted"]]
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

    def test_synonyms(self):
        """ Test all synonyms. """
        # Given
        data = {
            "name": {
                "filter": ["n", "=", "5"],
                "expected_result": {"name__icontains": 5},
                },
            "gold": {
                "filter": ["au", "=", "5"],
                "expected_result": {"gold__icontains": 5},
                },
            "green": {
                "filter": ["g", "=", "5"],
                "expected_result": {"green__icontains": 5},
                },
            "blue": {
                "filter": ["b", "=", "5"],
                "expected_result": {"blue__icontains": 5},
                },
            "red": {
                "filter": ["r", "=", "5"],
                "expected_result": {"red__icontains": 5},
                },
            "energy": {
                "filter": ["e", "=", "5"],
                "expected_result": {"energy__icontains": 5},
                },
            "attack": {
                "filter": ["x", "=", "5"],
                "expected_result": {"attack__icontains": 5},
                },
            "health": {
                "filter": ["h", "=", "5"],
                "expected_result": {"health__icontains": 5},
                },
            "supply": {
                "filter": ["su", "=", "5"],
                "expected_result": {"supply__icontains": 5},
                },
            "frontline": {
                "filter": ["fl", "=", "5"],
                "expected_result": {"frontline__icontains": 5},
                },
            "fragile": {
                "filter": ["f", "=", "5"],
                "expected_result": {"fragile__icontains": 5},
                },
            "blocker": {
                "filter": ["bl", "=", "5"],
                "expected_result": {"blocker__icontains": 5},
                },
            "prompt": {
                "filter": ["p", "=", "5"],
                "expected_result": {"prompt__icontains": 5},
                },
            "stamina": {
                "filter": ["s", "=", "5"],
                "expected_result": {"stamina__icontains": 5},
                },
            "lifespan": {
                "filter": ["l", "=", "5"],
                "expected_result": {"lifespan__icontains": 5},
                },
            "build_time": {
                "filter": ["bt", "=", "5"],
                "expected_result": {"build_time__icontains": 5},
                },
            "exhaust_turn": {
                "filter": ["et", "=", "5"],
                "expected_result": {"exhaust_turn__icontains": 5},
                },
            "exhaust_ability": {
                "filter": ["ea", "=", "5"],
                "expected_result": {"exhaust_ability__icontains": 5},
                },
            "position": {
                "filter": ["pos", "=", "5"],
                "expected_result": {"position__icontains": 5},
                },
            "abilities": {
                "filter": ["a", "=", "5"],
                "expected_result": {"abilities__icontains": 5},
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

    def test_allowed(self):
        """ Test only return keys in the allowed list. """
        # Given
        data = "gold=5,bad_field=5"
        expected_result = {"gold__icontains": 5}, {}

        # When
        result = includes_excludes(data, allowed=["gold"])

        # Then
        self.assertEqual(result, expected_result)
