def formatPostalCode(register) -> str:

    from .constants import COUNTRY_NAME, POSTAL_CODE

    if register["nif"] is None: return None

    return f"{register['nif']} {COUNTRY_NAME} {POSTAL_CODE}"