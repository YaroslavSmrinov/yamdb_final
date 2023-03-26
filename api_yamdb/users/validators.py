from django.core.exceptions import ValidationError


def validate_me(value):
    if value.lower() == 'me':
        raise ValidationError(
            ' Использовать имя "me" в качестве username запрещено ',
            params={'value': value},
        )
