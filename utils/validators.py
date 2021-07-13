from django.core.exceptions import ValidationError


def number_validator(value: str):
    '''
    This method valid if the given string value contains only numbers
    '''
    if not value.isdigit():
        raise ValidationError(
            'El campo debe ser un número',
            params={'value': value}
        )


def day_of_week_validator(value: int):
    '''
    Validate if given value is not more than 6.
    Use for limit values acording to `date.weekday()`
    '''
    if value > 6:
        raise ValidationError(
            'Día de la semana fuera de rango',
            params={'value': value}
        )
