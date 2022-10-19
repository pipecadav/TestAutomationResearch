import os
from enum import Enum
from pathlib import Path

from appium.webdriver.common.mobileby import MobileBy
from dotenv import load_dotenv
from selenium.webdriver.common.by import By

load_dotenv()

BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
NO_WAIT = 0
SHORT_WAIT_TIME = 5
MEDIUM_WAIT_TIME = 15
LONG_WAIT_TIME = 30
DEFAULT_FORMAT_DATE = "%m/%d/%Y"
API_FORMAT_DATE = "%Y-%m-%d"
XRAY_DATE = "%Y-%m-%dT%H:%M:%S%z"

TEST_DATA = "data_source/test_data.json"
ENV_DATA = "data_source/{}_data.json"
# Capabilities section
PACKAGE = "com.disney.wdpro.dlr"
ACTIVITY = "com.disney.wdpro.park.activities.SplashActivity"
ANDROID = "android"
IOS = "ios"

# Validation messages
ELEMENT_DISPLAYED = "Element {} is displayed"
PAGE_DISPLAYED = "Page {} is displayed"
INCORRECT_ENV_VAR = "The provided {0} is not correct please check the working {0}s: "

# Locators section
CSS = By.CSS_SELECTOR
ACCESSIBILITY_ID = MobileBy.ACCESSIBILITY_ID
XPATH = By.XPATH
UI_AUTOMATOR = MobileBy.ANDROID_UIAUTOMATOR
ID = MobileBy.ID
BY_RESOURCE = 'new UiSelector().resourceIdMatches(".*{}")'

# Pages or commons
BROWSERS = ["chrome", "firefox"]
ENVS = ["dev", "qa", "uat"]


class WindowSize(Enum):
    """
    Enum for Window sizes info
    """

    desktop = 1440
    tablet = 768
    height = 1024
