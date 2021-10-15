from django.db import models
from familystructure.fields import ListAsStringField

from django.utils.translation import ugettext_lazy as _

class Relation(models.Model):
    """
    | Field       | Details             |
    | :---------- | :------------------ |
    | source      | fk Person           |
    | target      | fk Person           |
    | is_upward   | bool                |
    """
    source = models.ForeignKey(
        'familystructure.Person',
        verbose_name=_('source person'),
        related_name='relations_out',
        on_delete=models.CASCADE,
    )
    target = models.ForeignKey(
        'familystructure.Person',
        verbose_name=_('target person'),
        related_name='relations_in',
        on_delete=models.CASCADE,
    )
    is_upward = models.BooleanField(
        _('is upward'),
        default=True,
    )

    def __str__(self):
        if self.is_upward:
            return f'{self.target} -> {self.source}'
        return f'{self.source} -- {self.target}'

class FamilyCircle(models.Model):
    """
    | Field       | Details             |
    | :---------- | :------------------ |
    | name        | 64 chars            |
    | members     | mtm Person          |
    | managers    | mtm UserAccount     |
    """
    name = models.CharField(_('name'), max_length=64)
    members = models.ManyToManyField(
        'familystructure.Person',
        verbose_name=_('members'),
        related_name='family_circles',
    )
    managers = models.ManyToManyField(
        'useraccount.UserAccount',
        verbose_name=_('managers'),
        related_name='family_circles_managing',
    )

    def __str__(self):
        return f'{self.name} ({len(self.members.all())} members)'
    
    def query_detached_people(self):
        return self.members.filter(relations_in__isnull=True, relations_out__isnull=True)

class Person(models.Model):
    """
    | Field           | Details             |
    | :-------------- | :------------------ |
    | first_name      | 32 chars            |
    | nickname        | 32 chars, optional  |
    | middle_name     | 32 chars, optional  |
    | last_name       | 32 chars            |
    | title           | 16 chars, optional  |
    | tagline         | 64 chars, optional  |
    | birth_date      | Date                |
    | death_date      | Date, optional      |
    | profile_picture | ImageField          |
    | is_claimed      | bool, default False |
    | facts           | ListAsStringField   |
    """

    class Meta:
        verbose_name_plural = _('people')

    first_name = models.CharField(
        _('first name'),
        max_length=32,
    )
    
    nickname = models.CharField(
        _('nickname'),
        max_length=32,
        blank=True,
        null=True,
    )
    
    middle_name = models.CharField(
        _('middle name'),
        max_length=32,
        blank=True,
        null=True,
    )
    
    last_name = models.CharField(
        _('last name'),
        max_length=32,
    )
    
    title = models.CharField(
        _('title'),
        max_length=16,
        blank=True,
        null=True,
    )
    
    tagline = models.CharField(
        _('tagline'),
        max_length=64,
        blank=True,
        null=True,
    )
    
    birth_date = models.DateField(
        _('birth date'),
        auto_now=False,
        auto_now_add=False,
    )
    
    death_date = models.DateField(
        _('death date'),
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )

    profile_photo = models.ImageField(
        _('profile photo'),
        # MEDIA_ROOT/profile_photos/ == website/static/uploads/profile_photos/
        upload_to='profile_photos/',
        null=True,
        blank=True,
    )
    
    is_claimed = models.BooleanField(
        _('is claimed'),
        default=False,
    )
    
    facts = ListAsStringField(default=[], blank=True, null=True)

    def __str__(self):
        middle = ''
        end = f' {self.title}' if self.title else ''
        if self.nickname:
            middle += f' "{self.nickname}"'
        if self.middle_name:
            middle += f' {self.middle_name}'
        return f'{self.first_name}{middle} {self.last_name}{end}'
    
    def query_grandparents(self) -> list:
        """Get the grandparents of this Person"""
        try:
            parent_rels = self.relations_out.filter(is_upward=True)
        except AttributeError: # no parents, no grandparents
            return []
        
        grandparent_rels = []
        for rel in parent_rels:
            try:
                grandparent_rels.extend(list(rel.target.relations_out.filter(is_upward=True)))
            except AttributeError: # parent didn't have parents
                pass
        
        return list(set(rel.target for rel in grandparent_rels))
    
    def query_parents(self) -> list:
        """Get the parents of this Person"""
        try:
            return [rel.target for rel in self.relations_out.filter(is_upward=True)]
        except AttributeError: # no parents
            return []        
    
    def query_generation(self) -> list:
        """Get this person, their siblings and their spouses of this person"""
        try:
            parent_rels = self.relations_out.filter(is_upward=True)
        except AttributeError: # no parents, no siblings
            parent_rels = Relation.objects.none()
        
        children_rels = []
        for rel in parent_rels:
            try:
                children_rels.extend(list(rel.target.relations_in.filter(is_upward=True)))
            except AttributeError: # a parent didn't have children
                pass
        children = set(rel.source for rel in children_rels)
        try:
            spouse_rels = self.relations_in.filter(is_upward=False).union(self.relations_out.filter(is_upward=False))
        except AttributeError:
            spouse_rels = Relation.objects.none()
        spouses = set(rel.target if rel.target != self else rel.source for rel in spouse_rels)
        return list(children | spouses)

    def query_children(self) -> list:
        """Get the direct children of this person"""
        try:
            return [rel.source for rel in self.relations_in.filter(is_upward=True)]
        except AttributeError: # no children
            return []

    def query_grandchildren(self) -> list:
        """Get the direct children of this person's children"""
        try:
            children_rels = self.relations_in.filter(is_upward=True)
        except AttributeError: # no children, no grandchildren
            return []
        
        grandchildren_rels = []
        for rel in children_rels:
            try:
                grandchildren_rels.extend(list(rel.source.relations_in.filter(is_upward=True)))
            except AttributeError: # a child didn't have children
                pass
        
        return list(set(rel.source for rel in grandchildren_rels))
                    
    def query_managers(self) -> list:
        """Get the list of UserAccounts that can edit this Person"""
        try:
            me = [self.useraccount]
        except:
            me = []
        try:
            circles = self.family_circles.all()
            managers = []
            for circle in circles:
                managers.extend(list(circle.managers.all()))
            if me and me[0] not in managers:
                managers = me + managers
            return managers
        except AttributeError: # no family circles, just us (if possible)
            return me