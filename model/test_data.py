import json
import os

from utils.common import get_env
from utils.constants import BASE_DIR, ENV_DATA, TEST_DATA


class Pages:
    home: str


class Services:
    xray_url: str


class User:
    email: str
    password: str
    name: str


class Users:
    primary_user: User


class Data:
    base_url: str
    users: Users
    pages: Pages
    services: Services


def _read_test_data_json(obj):
    test_data = Data()
    test_data.__dict__.update(obj)
    return test_data


def open_json(path):
    f = open(os.path.join(BASE_DIR, path))
    return json.load(f, object_hook=_read_test_data_json)


def get_json(obj):
    return json.loads(json.dumps(obj, default=lambda o: getattr(o, "__dict__", str(o))))


_test_data = open_json(TEST_DATA)
_env_data = open_json(ENV_DATA.format(get_env()))


class TestData:
    """
    Test Data class
    """

    data = _test_data
    env = _env_data

    def get_primary_user(self):
        return self.env.users.primary_user

    def get_base_url(self):
        return self.data.base_url

    def get_home_title(self):
        return self.data.pages.home

    def get_xray_url(self):
        return self.data.services.xray_url
