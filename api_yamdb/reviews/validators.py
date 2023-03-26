from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils import timezone as tz
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class MinMaxValidator(BaseValidator):
    message = _(
        'Ensure that the value %(value)s is on [%(min_value)s..%(max_value)s].'
    )
    code = 'minmax_value'

    def __init__(self, min_value, max_value, message=None):
        self.min_value = min_value
        self.max_value = max_value
        if message:
            self.message = message

    def __call__(self, value):
        cleaned = self.clean(value)
        min_value = (
            self.min_value() if callable(self.min_value) else self.min_value
        )
        max_value = (
            self.max_value() if callable(self.max_value) else self.max_value
        )
        params = {
            'min_value': min_value,
            'max_value': max_value,
            'value': value}
        if self.compare(cleaned, min_value, max_value):
            raise ValidationError(self.message, code=self.code, params=params)

    def compare(self, value, min_value, max_value):
        return not (value >= min_value
                    and value <= max_value)


def year_validator(value):
    if value > tz.datetime.now().year:
        raise ValidationError(
            f'{value} не может быть годом выхода произведения.'
        )
