""" Models for papi.units """
from django.db import models


class LatestUnitVersionView(models.Model):  # type: ignore
    """ View with unit information and its latest version. """
    name = models.CharField(max_length=64)
    wiki_path = models.CharField(max_length=64)
    image_url = models.CharField(max_length=128)
    panel_url = models.CharField(max_length=128)
    gold = models.IntegerField()
    green = models.IntegerField()
    blue = models.IntegerField()
    red = models.IntegerField()
    energy = models.IntegerField()
    attack = models.IntegerField()
    health = models.IntegerField()
    supply = models.IntegerField()
    unit_spell = models.CharField(max_length=32)
    frontline = models.BooleanField()
    fragile = models.BooleanField()
    blocker = models.BooleanField()
    prompt = models.BooleanField()
    stamina = models.IntegerField()
    lifespan = models.IntegerField()
    build_time = models.IntegerField()
    exhaust_turn = models.IntegerField()
    exhaust_ability = models.IntegerField()
    position = models.CharField(max_length=32)
    abilities = models.CharField(max_length=256)

    class Meta:  # pylint: disable=too-few-public-methods
        """ Metadata for Django models. """
        managed = False
        db_table = 'latest_unit_version'

    def __str__(self) -> str:
        return f"{self.name}"
