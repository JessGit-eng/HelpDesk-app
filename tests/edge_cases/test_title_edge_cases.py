from tests.unit.unit_testing import validate_ticket

def test_title_too_short_partition():
    result = validate_ticket(
        title="A",
        description="Printer is broken",
        category="Hardware"
    )

    assert result is False


def test_valid_title_partition():
    result = validate_ticket(
        title="Printer broken",
        description="Printer is broken",
        category="Hardware"
    )

    assert result is True


def test_title_too_long_partition():
    result = validate_ticket(
        title="A" * 51,
        description="Printer is broken",
        category="Hardware"
    )

    assert result is False