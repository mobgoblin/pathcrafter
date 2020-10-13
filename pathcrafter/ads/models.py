import json

from django.db import models


CATEGORIES = (
    ('LAB', 'labor'),
    ('CAR', 'cars'),
    ('TRU', 'trucks'),
    ('WRI', 'writing'),
)
LOCATIONS = (
    ('BRO', 'Bronx'),
    ('BRK', 'Brooklyn'),
    ('QNS', 'Queens'),
    ('MAN', 'Manhattan'),
    ('STN', 'Staten Island'),
)

data = {}
list = ()

with open('spells.txt') as json_file:
    data = json.load(json_file)
    index = 0
    for key in data:
        list += (('SP' + str(index), key),)
        index += 1

class PostAd(models.Model):
    name        = models.CharField(max_length=50)
    email       = models.EmailField()
    gist        = models.CharField(max_length=50)
    category    = models.CharField(max_length=5, choices=list)
    location    = models.CharField(max_length=3, choices=LOCATIONS)
    description = models.TextField(max_length=300)
    expire      = models.DateField()