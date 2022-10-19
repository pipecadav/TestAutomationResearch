import re
import subprocess

from utils.common import get_env_var
from utils.constants import ACTIVITY, ANDROID, IOS, PACKAGE


def execute_command(command):
    """
    Execute shell command
    :param command: to run
    :return: result of command execution
    """
    return subprocess.run(command, stdout=subprocess.PIPE).stdout.decode("utf-8")


def get_android_caps():
    """
    Get Android capabilities for appium
    :return: dict with capabilities
    """
    device_name, device_version = get_android_device_info()
    return {
        "platformName": ANDROID,
        "platformVersion": device_version,
        "deviceName": device_name,
        "automationName": "UiAutomator2",
        "app": get_env_var("ANDROID_PATH"),
        "appPackage": PACKAGE,
        "appActivity": ACTIVITY,
    }


def get_ios_caps():
    """
    Get IOS capabilities for appium
    :return: dict with capabilities
    """
    device_name, device_version = get_ios_device_info()
    return {
        "platformName": IOS,
        "platformVersion": device_version,
        "deviceName": device_name,
        "udid": get_env_var("UDID"),
        "automationName": "XCUITest",
        "app": get_env_var("IOS_PATH"),
        "bundleId": get_env_var("BUNDLE_ID"),
    }


def get_capabilities():
    """
    Get capabilities
    :return: Dict
    """
    if get_env_var("EXECUTE_ON").lower() == IOS:
        return get_ios_caps()
    else:
        return get_android_caps()


def get_ios_device_info():
    """
    Get IOS device info like device name and version
    :return: device name and version
    """
    # TODO add logic for real device
    devices_list = execute_command(["xcrun", "xctrace", "list", "devices"]).splitlines()
    try:
        device_info = [device for device in devices_list if get_env_var("UDID") in device]
        device_version = re.findall(r"-?\d+\.?\d*\.?\d*", device_info[0].split(")")[0])[-1]
        device_name = device_info[0].split(" (")[0]
        return device_name, device_version
    except Exception as error:
        raise TypeError("The provided UDID doesnt exists or: {}".format(error))


def get_android_device_info():
    """
    Get Android device info like device name and version
    :return: device name and version
    """
    device_name = execute_command(["adb", "devices"])
    device_version = execute_command(["adb", "shell", "getprop ro.build.version.release"])
    if not device_name:
        raise TypeError("There is no device connected")
    return device_name, device_version
