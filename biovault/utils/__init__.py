from typing import Any


def evalSentence(sentence: str,
                 imports: list[str] = [],
                 **kwargs) -> Any:

    for element in imports: exec(element)

    locals().update(kwargs)

    try: return eval(sentence)

    except (ValueError, TypeError, NameError, KeyError, IndexError) as error:
        return None