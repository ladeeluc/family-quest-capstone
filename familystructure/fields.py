from django.db import models

class SepTextField(models.TextField):
    """
    Model concept adapted from:
    https://stackoverflow.com/questions/1110153/what-is-the-most-efficient-way-to-store-a-list-in-the-django-models
    """

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', '|')
        super(SepTextField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value: return
        if isinstance(value, list):
            return value
        return value.split(self.token)

    def get_db_prep_value(self, value):
        if not value: return
        assert(isinstance(value, list) or isinstance(value, tuple))
        return self.token.join([str(s) for s in value])
    
    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)