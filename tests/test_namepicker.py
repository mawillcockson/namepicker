from namepicker import __version__


def test_version():
    """
    Test fails if test suite is run on the wrong application version
    """
    assert __version__ == "0.0.1"
