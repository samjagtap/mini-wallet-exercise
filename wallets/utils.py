def is_valid_amount(amount):
    if amount and amount.isnumeric() and int(amount) >= 0:
        return True
    else:
        return False


def is_valid_uuid(value):
    import uuid
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False
