from django.db import models
from django.contrib.auth.models import User

from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator

from django.db.models import (
    DO_NOTHING, CharField, DateField, ForeignKey, IntegerField, DecimalField, Model, TextField, ImageField,
    BooleanField, EmailField
)


# Create your models here.
class Task(Model):

    # These constants contain statuses
    INQU = 'In queue'
    PRGR = 'In progress'
    CMPL = 'Completed'
    PSPD = 'Postponed'

    # This dictionary contains choices for the status
    STATUS_CHOICES = {
        None: 'select status',
        INQU: 'In queue',
        PRGR: 'In progress',
        CMPL: 'Completed',
        PSPD: 'Postponed',
    }

    title = CharField(max_length=200)
    owner = ForeignKey(User, on_delete=DO_NOTHING, default=None)
    description = TextField(default=None)
    status = CharField(max_length=30, choices=STATUS_CHOICES, blank=True)
    creation_date = DateField(default=None, null=False)

    def __str__(self):
        return f"Task: {self.title} (user: {self.owner.name})"
