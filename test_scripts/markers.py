import pytest


class Marker:
    """
    Markers class
    """

    regression = pytest.mark.regression
    smoke = pytest.mark.smoke
    broken = pytest.mark.broken
