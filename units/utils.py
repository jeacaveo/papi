""" Utilities for papi.units """
from typing import (
    Dict,
    Iterator,
    List,
    Optional,
    Tuple,
    Union,
    )
from pyparsing import (
    alphanums,
    alphas,
    Combine,
    delimitedList,
    oneOf,
    ParseException,
    Word,
    )


OPERATORS_MAP = {
    ":": "__icontains",
    "=": "__icontains",
    ">": "__gt",
    ">=": "__gte",
    "<": "__lt",
    "<=": "__lte",
    "!=": "__icontains",
    "<>": "__icontains",
    }
SEARCH_OPERATORS = oneOf(" ".join(OPERATORS_MAP.keys()))
SEARCH_FILTER = (
    Word(alphas + "_") + SEARCH_OPERATORS + Word(alphanums + "_" + " "))
SEARCH_QUERY = delimitedList(Combine(SEARCH_FILTER), delim=",")

SYNONYMS_MAP = {
    "n": "name",
    "au": "gold",
    "g": "green",
    "b": "blue",
    "r": "red",
    "e": "energy",
    "x": "attack",
    "h": "health",
    "su": "supply",
    "fl": "frontline",
    "f": "fragile",
    "bl": "blocker",
    "p": "prompt",
    "s": "stamina",
    "l": "lifespan",
    "bt": "build_time",
    "et": "exhaust_turn",
    "ea": "exhaust_ability",
    "pos": "position",
    "a": "abilities",
    }


def parse_query(raw_query: str) -> Iterator[List[str]]:
    """
    Get valid params from query string.

    Parameters
    ----------
    raw_query : str
        String to be parsed.

    Returns
    -------
    iterator(list(str))

    Examples
    --------
    input:
        "gold=5, blue!=3,    red>=1,drone,energy:2"

    output:
        [
            ["gold", "=", "5"],
            ["blue", "!=", "3"],
            ["red", ">=", "1"],
            ["drone"],
            ["energy", ":", "2"],
        ]

    """

    try:
        return map(
            list,
            map(SEARCH_FILTER.parseString, SEARCH_QUERY.parseString(raw_query))
            )
    except ParseException:
        return (_ for _ in [])  # empty iterator


def filter_to_lookup(data: List[str]) -> Dict[str, Union[str, int]]:
    """
    Get dict with expected format for a Django ORM query/filter lookup.

    Expected data format: ["field name", "operator", "value"]

    Parameters
    ----------
    data : list(str)
        Filter in raw format.

    Returns
    -------
    dict()

    Examples
    --------
    input:
        ["gold", "=", "5"]

    output:
        {"gold__icontains": "5:}

    """
    if len(data) != 3 or data[1] not in OPERATORS_MAP:
        return {}
    field, operator, value = data

    field = SYNONYMS_MAP.get(field) or field
    is_digit = value.isdigit()
    lookup = (
        ""
        if is_digit and data[1] in ["=", ":", "!=", "<>"]
        else OPERATORS_MAP[operator])
    value = int(value) if is_digit else value  # type: ignore

    return {f"{field}{lookup}": value}


def includes_excludes(
        data: str, allowed: Optional[List[str]] = None
        ) -> Tuple[Dict[str, Union[str, int]], Dict[str, Union[str, int]]]:
    """
    Convert query string into a dict of includes and excludes.

    Parameters
    ----------
    data : str
        String to be parsed.
    allowed : list(str), optional
        List of fields to consider. If not provided, allow all.

    Returns
    -------
    tuple(dict, dict)

    Examples
    --------
    input:
        "gold=5,energy!=5"

    output:
        ({"gold__icontains": "5:}, {"energy__icontains": "5"})

    """
    includes = {}
    excludes = {}
    ignored = {}
    for raw_filter in parse_query(data):
        negative_operators = ["!=", "<>"]
        lookup = filter_to_lookup(raw_filter)
        field = SYNONYMS_MAP.get(raw_filter[0]) or raw_filter[0]

        # Only consider allowed fields
        if (allowed and field not in allowed) or False:
            ignored.update(lookup)
        elif set(negative_operators).intersection(raw_filter):
            excludes.update(lookup)
        else:
            includes.update(lookup)
    return includes, excludes
