from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(year):
    current_year = datetime.now().year
    if year > current_year:
        raise ValidationError(
            f'Title cannot be created later than {current_year}'
        )


def validate_score(score):
    if score > 10 or score < 0:
        raise ValidationError(
            'Title cannot be greater than 10 or lesser than 0'
        )