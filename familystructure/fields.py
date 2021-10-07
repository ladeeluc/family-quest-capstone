from django.db import models
import json
import re

class ListAsStringField(models.TextField):
    """
    Model concept adapted from:
    https://stackoverflow.com/questions/1110153/what-is-the-most-efficient-way-to-store-a-list-in-the-django-models
    """

    def __init__(self, *args, **kwargs):
        super(ListAsStringField, self).__init__(*args, **kwargs)

    # json str -> list
    def to_python(self, value):
        if not value: return
        if isinstance(value, list):
            return value
        value = re.sub(
            r'[\'\"], ?[\'\"]',
            '","',
            value,
        )
        value = re.sub(
            r'\[[\'\"]',
            '["',
            value,
        )
        value = re.sub(
            r'[\'\"]\]',
            '"]',
            value,
        )
        return json.loads(value)

    def from_db_value(self, value, expression=None, connection=None, context=None):           
        return self.to_python(value)

    # list -> json str
    def get_db_prep_value(self, value, **kwargs):
        if not value: return
        assert(isinstance(value, list) or isinstance(value, tuple))
        return json.dumps([str(s) for s in value])

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)