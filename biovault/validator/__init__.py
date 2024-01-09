import jsonschema
from datetime import date

def dateMinimum(validator, minimumDate, instance, schema):

    minimumDate = date.fromisoformat(minimumDate)
    flag = True

    if isinstance(instance, str):
        try: instance = date.fromisoformat(instance)
        except ValueError: flag = False

    if flag and instance < minimumDate:
        yield jsonschema.ValidationError(f"{instance} is before minimum date {minimumDate}")



def dateMaximum(validator, maximumDate, instance, schema):

    maximumDate = date.fromisoformat(maximumDate)
    flag = True

    if isinstance(instance, str):
        try: instance = date.fromisoformat(instance)
        except ValueError: flag = False

    if flag and instance < maximumDate:
        yield jsonschema.ValidationError(f"{instance} is after maximum date {maximumDate}")



def isDate(_, instance):

    try:
        date.fromisoformat(instance)
        return True

    except ValueError:
        return False



BioVaultValidator = jsonschema.validators.extend(jsonschema.Draft202012Validator,
                                                 validators = {"dateMinimum" : dateMinimum,
                                                               "dateMaximum" : dateMaximum},
                                                 type_checker= jsonschema.Draft202012Validator.TYPE_CHECKER.redefine('date',
                                                                                                                     isDate))