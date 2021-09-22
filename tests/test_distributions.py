from virgil.core.models import get_packages


def test_distributions():
    assert get_packages()
