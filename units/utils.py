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
    operators = oneOf(": < = > >= <= != <>")
    param = Word(alphas) + Optional(operators + Word(alphanums))
    query = delimitedList(Combine(param), delim=",")

    try:
        return map(
            list,
            map(param.parseString, query.parseString(raw_query))
            )
    except ParseException:
        return (_ for _ in [])  # empty iterator
