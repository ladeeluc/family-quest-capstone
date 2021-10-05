from django.db import models
from familystructure.fields import SepTextField

class Person(models.Model):
    """
    | Field       | Details             |
    | :---------- | :------------------ |
    | first_name  | 32 chars            |
    | nickname    | 32 chars, optional  |
    | middle_name | 32 chars, optional  |
    | last_name   | 32 chars            |
    | title       | 16 chars, optional  |
    | tagline     | 128 chars, optional |
    | birth_date  | Date                |
    | death_date  | Date, optional      |
    | is_claimed  | bool, default False |
    | facts       | SepTextField        |
    """
    pass

class UpwardRelation(models.Model):
    pass

class FamilyCircle(models.Model):
    pass