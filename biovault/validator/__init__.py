import jsonschema

def dateMinimum(validator, dateMinimum, instance, schema):
    if instance < dateMinimum:
        yield jsonschema.ValidationError(f"{instance} is before minimum date {dateMinimum}")


def dateMaximum(validator, dateMaximum, instance, schema):
    if instance > dateMaximum:
        yield jsonschema.ValidationError(f"{instance} is after maximum date {dateMaximum}")

BioVaultValidator = jsonschema.validators.extend(jsonschema.Draft202012Validator,
                                                 validators = {"dateMinimum" : dateMinimum,
                                                               "dateMaximum" : dateMaximum})