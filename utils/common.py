import datetime as dt
import os
import random
from datetime import datetime

import allure
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from loguru import logger as log

from utils.constants import BROWSERS, DEFAULT_FORMAT_DATE, ENVS, INCORRECT_ENV_VAR

load_dotenv()


def create_random_name():
    """
    Create random name
    :return: String
    """
    n = random.randint(0, 10000)
    return "Test_name_" + str(n)


def get_random_number(max_num=12):
    """
    Get random number hours
    :return: random number
    """
    return random.randint(1, max_num)


def get_date(date=None, formatter="%Y-%m-%d"):
    """
    Get current date
    :return: datetime object
    """
    # TODO check the final return
    if date is not None:
        return datetime.strptime(str(date), formatter)
    return datetime.strptime(str(datetime.now().date()), formatter)


def get_current_time(formatter="%d%m%y-%H%M%S%f", time_zone=dt.timezone.utc):
    """
    Get current time of date and time
    :return: strings with now time
    """
    return datetime.now(tz=time_zone).strftime(formatter)


def get_date_from_now(years=0, months=0, days=0, formatter=DEFAULT_FORMAT_DATE):
    """
    Get string date from today on
    :param years: how many years
    :param months: how many months
    :param days:  how many days
    :param formatter: string format for date
    :return: string with date
    """
    today = datetime.now().date()
    return (today + relativedelta(years=years, months=months, days=days)).strftime(formatter)


@allure.step(" **** STEP {step} **** ")
def log_step(step):
    """
    Log step number
    :param step: number
    """
    log.info(" **** STEP {} **** ".format(step))


def get_env_var(var, default=None):
    """
    Get Environment variable
    :param var: variable name
    :param default: default value
    :return: env value
    """
    return os.getenv(var, default)


def get_env():
    """
    Get environment for the execution
    :return: String with env value
    """
    env = get_env_var("ENV", default="dev").lower()
    if env in ENVS:
        return env
    else:
        raise ValueError(INCORRECT_ENV_VAR.format("env"))


def get_env_browser():
    """
    Get environment for the execution
    :return: String with env value
    """
    browser = get_env_var("BROWSER", default="chrome").lower()
    if browser in BROWSERS:
        return browser
    else:
        raise ValueError(INCORRECT_ENV_VAR.format("driver"))


def get_random_from_list(lst):
    """
    Get Randon item from list
    :param lst: list of any
    :return: random item
    """
    return lst[get_random_number(len(lst)) - 1]
