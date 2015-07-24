import re
from django.core.exceptions import ValidationError


def colorValidator(value):
    """
    Validates if the given value is a string representing an hexadecimal color
    value (starts with a #, then RGB composants in hex).

    >>> colorValidator('#0a1b2C')

    >>> colorValidator('#AAAAAA')

    >>> colorValidator('ff00ff')
    ValidationError: ['ff00ff is not a valid hex color.']
    """
    exp = re.compile('^#[a-fA-F0-9]{6}$')
    if not re.match(exp, value):
        raise ValidationError('{} is not a valid hex color.'.format(value))
