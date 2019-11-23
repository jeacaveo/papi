""" Utilities for papi.units """
from typing import (
    Dict,
    Iterator,
    List,
    Tuple,
    Union,
    )
from pyparsing import (
    alphanums,
    alphas,
    Combine,
    delimitedList,
    oneOf,
    Optional,
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
SEARCH_FILTER = Word(alphas) + Optional(SEARCH_OPERATORS + Word(alphanums))
SEARCH_QUERY = delimitedList(Combine(SEARCH_FILTER), delim=",")


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
    return {
        f"{field}{OPERATORS_MAP[operator]}":
        int(value) if value.isdigit() else value
        }


def includes_excludes(
        data: str
        ) -> Tuple[Dict[str, Union[str, int]], Dict[str, Union[str, int]]]:
    """
    Convert query string into a dict of includes and excludes.

    Parameters
    ----------
    data : str
        String to be parsed.

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
    for raw_filter in parse_query(data):
        negative_operators = ["!=", "<>"]
        lookup = filter_to_lookup(raw_filter)
        # If operator for filter is negative, use it in exclude
        if set(negative_operators).intersection(raw_filter):
            excludes.update(lookup)
        else:
            includes.update(lookup)
    return includes, excludes
