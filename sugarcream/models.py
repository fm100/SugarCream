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
    createdTime = models.DateField(auto_now=True, auto_now_add=True)
    sprint = models.IntegerField()
    sprintUnit = models.CharField(max_length=8)
    status = models.CharField(max_length=16)

    def __unicode__(self):
        return self.name

class BacklogItem(models.Model):
    '''
    @name : Backlog item name.
    @summary : Short summary of backlog item.
    @description : Description of backlog item. This can be long.
    @priority : Priority of backlog item. This has range of 0 to 2.
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

class UserStory(models.Model):
    '''
    @name : Short name which describes the story.
    @story : User story which user posted.
    '''
    name = models.CharField(max_length=32)
    story = models.TextField()

class Document(models.Model):
    pass

class MeetingLog(models.Model):
    '''
    @date : The day and time that meeting log is written.
    @project : Project that this log belongs to.
    @log : The log of the meeting.
    '''
    date = models.DateTimeField(auto_now=True, auto_now_add=True)
    project = models.ForeignKey(Project)
    log = models.TextField()

class DailyScrum(models.Model):
    '''
    @date : The day daily scrum is written.
    @project : Project which daily scrum is about.
    @member : User(member of project) who writes this daily scrum.
    @jobDidYesterday : Job what the member did yesterday.
    @jobTodoToday : Job what the member will do today.
    '''
    date = models.DateField(auto_now=True, auto_now_add=True)
    project = models.ForeignKey(Project)
    member = models.ForeignKey(User)
    jobDidYesterday = models.CharField(max_length=128)
    jobTodoToday = models.CharField(max_length=128)
