from unit_testing import validate_ticket

#Title cannot be empty
def test_empty_title():
    assert validate_ticket(
        "",
        "Cannot connect to VPN from home",
        "network"
    ) is False

#Description cannot be empty
def test_empty_description():
    assert validate_ticket(
        "VPN Issue",
        "",
        "network"
    ) is False

#Category cannot be empty
def test_empty_category():
    assert validate_ticket(
        "VPN Issue",
        "Cannot connect to VPN from home",
        ""
    ) is False

#Title cannot contain only spaces
def test_title_with_only_spaces():
    assert validate_ticket(
        "     ",
        "Cannot connect to VPN from home",
        "network"
    ) is False

#Title must meet a minimum length
def test_title_too_short():
    assert validate_ticket(
        "VP",
        "Cannot connect to VPN from home",
        "network"
    ) is True

#Title must not exceed a maximum length
def test_title_too_long():
    assert validate_ticket(
        "A" * 51,
        "Cannot connect to VPN from home",
        "network"
    ) is False

#Description must meet a minimum length
def test_description_too_short():
    assert validate_ticket(
        "VPN Issue",
        "Help",
        "network"
    ) is False

