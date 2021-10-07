from django.contrib import admin

from familystructure.models import (
    Person,
    Relation,
    FamilyCircle,
)

admin.site.register(Person)
admin.site.register(Relation)
admin.site.register(FamilyCircle)