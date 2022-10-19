import json
from typing import Any, Callable, List, TypeVar

from loguru import logger

from model.test_data import TestData

data = TestData()
T = TypeVar("T")


def from_str(x: Any) -> str:
    """
    Check value is string
    :param x: value
    :return: string value
    """
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    """
    Check value is boolean
    :param x: value
    :return: boolean value
    """
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    """
    Check value from list
    :param f: function
    :param x: value
    :return: list of objects
    """
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_none(x: Any) -> Any:
    """
    Check value is none
    :param x: value
    :return: value
    """
    assert x is None
    return x


def from_union(fs, x):
    """
    Check if value is in union
    :param fs: function
    :param x: value
    :return: function value
    """
    for f in fs:
        try:
            return f(x)
        except Exception as e:
            logger.trace(e)
    raise AssertionError()


def from_int(x: Any) -> int:
    """
    Check value is integer
    :param x: value
    :return: int value
    """
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def get_response(response):
    """
    Load json from text
    :param response: text string
    :return: response output
    """
    return json.loads(response.text)


class BaseAPI:
    """
    Base API class to initialize all base services info
    """

    url = data.get_base_url()
    headers = {"Content-Type": "application/json"}

    def __init__(self, base_url=url):
        """
        Constructor Base service API
        :param base_url: string with base url for calls
        """
        self.base_url = base_url
