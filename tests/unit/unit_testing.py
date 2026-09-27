def validate_ticket(title, description, category):

    # Remove leading/trailing spaces
    title = title.strip()
    description = description.strip()
    category = category.strip()

    # Required fields
    if not title:
        return False

    if not description:
        return False

    if not category:
        return False

    # Title length
    if len(title) < 2:
        return False

    if len(title) > 50:
        return False

    # Description length
    if len(description) < 10:
        return False

    return True