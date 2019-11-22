""" Utilities for papi.units """
from typing import (
    Iterator,
    List,
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


SEARCH_OPERATORS = oneOf(": < = > >= <= != <>")
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
        "gold=5, blue!=3,    red>=1,energy:2"

    output:
        [
            ['gold', '=', '5'],
            ['blue', '!=', '3'],
            ['red', '>=', '1'],
            ['energy', ':', '2'],
        ]

    """

    try:
        return map(
            list,
            map(SEARCH_FILTER.parseString, SEARCH_QUERY.parseString(raw_query))
            )
    except ParseException:
        return (_ for _ in [])  # empty iterator
