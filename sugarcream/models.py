# -*- condig: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    '''
    @owner : The person who made this project.
    @name : Project name.
    @summary : Short summary about project.
    @collaborators : Project members.
    @sprint : Time quantum of one iteration.
    @sprintUnit : One of the days, weeks, or months.
    @status : Project status. This field should have one of the following:
        - new : Project is just created but not started.
        - running : Project is started and is going on track.
        - blocked : Project is temporarily paused for some kind of reasons.
        - done : Project is ended successfully.
        - dumped : Project is ended but not successfully.
    '''
    owner = models.ForeignKey(User, related_name='owned_project_set')
    name = models.CharField(max_length=12, unique=True)
    summary = models.CharField(max_length=256)
    collaborators = models.ManyToManyField(User, related_name='project_set')
    createdTime = models.DateTimeField(auto_now=True, auto_now_add=True)
    sprint = models.IntegerField(default=0)
    sprintUnit = models.CharField(max_length=8, default="")
    status = models.CharField(max_length=16)

    def __unicode__(self):
        return self.name

class BacklogItem(models.Model):
    '''
    @name : Backlog item name.
    @summary : Short summary of backlog item.
    @description : Description of backlog item. This can be long.
    @priority : Priority of backlog item. This has range of 0 to 128.
    @status : Backlog item status.
        - pending: Item is in the ProductBacklog but not in SprintBacklog.
        - assigned : Item is assigned to user.
        - started : User started item.
        - done : User finished item.
    @project : Project that item belongs to.
    @assignedTo : User that item is assigned to.
    '''
    name = models.CharField(max_length=64)
    summary = models.CharField(max_length=256)
    description = models.TextField()
    priority = models.IntegerField()
    status = models.CharField(max_length=16)
    project = models.ForeignKey(Project)
    assignedTo = models.ForeignKey(User, null=True)

    def __unicode__(self):
        return self.name
