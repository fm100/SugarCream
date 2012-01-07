# -*- condig: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    owner = models.ForeignKey(User, related_name='owned_project_set')
    name = models.CharField(max_length=128, unique=True)
    collaborators = models.ManyToManyField(User, related_name='project_set')
