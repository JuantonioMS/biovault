def formatPostalCode(register) -> str:

    from .constants import COUNTRY_NAME, POSTAL_CODE

    return f"{register['nif']} {COUNTRY_NAME} {POSTAL_CODE}"