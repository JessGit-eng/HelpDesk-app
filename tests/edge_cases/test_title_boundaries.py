from tests.unit.unit_testing import validate_ticket

#Just below the minimum: 1 character
def test_title_length_1():
    assert validate_ticket(
        "A",
        "Cannot connect to VPN from home",
        "network"
    ) is False

#At the minimum: 2 characters
def test_title_length_2():
    assert validate_ticket(
        "VP",
        "Cannot connect to VPN from home",
        "network"
    ) is True

#Just above the minimum: 3 characters
def test_title_length_3():
    assert validate_ticket(
        "VPN",
        "Cannot connect to VPN from home",
        "network"
    ) is True

#Just below the maximum: 49
def test_title_length_49():
    assert validate_ticket(
        "A" * 49,
        "Cannot connect to VPN from home",
        "network"
    ) is True

#At the maximum: 50
def test_title_length_50():
    assert validate_ticket(
        "A" * 50,
        "Cannot connect to VPN from home",
        "network"
    ) is True

#Just above the maximum: 51
def test_title_length_51():
    assert validate_ticket(
        "A" * 51,
        "Cannot connect to VPN from home",
        "network"
    ) is False
    