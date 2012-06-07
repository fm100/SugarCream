# -*- condig: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.contrib.auth.views import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from sugarcream.forms import *
from sugarcream.models import *
import json
import datetime
from dateutil.relativedelta import relativedelta
from dateutil import parser

def mainpage(request):
    variables = RequestContext(request, {'request': request})
    return render_to_response('home.html', variables)

def aboutpage(request):
    variables = RequestContext(request, {'request': request})
    return render_to_response('about.html', variables)

def loginpage(request):
    if not request.user.is_authenticated():
        return login(request)
    else:
        return HttpResponseRedirect('/user/')

def logoutpage(request):
    logout(request)
    return HttpResponseRedirect('/')

def registerpage(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'])
            return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()

    variables = RequestContext(request, {'form': form})
    return render_to_response('registration/register.html', variables)

@login_required
def modifypage(request):
    variables = RequestContext(request, {'request': request})
    return render_to_response('registration/modify.html', variables)

@login_required
def userpage(request):
    variables = RequestContext(request, {'request': request})
    return render_to_response('user.html', variables)

def projectpage(request, project):
    try:
        p = Project.objects.get(name=project)
        variables = RequestContext(request,
                                   {'request': request, 'project': project})
        return render_to_response('project.html', variables)
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/')

def myprojects(request):
    if not request.user.is_authenticated():
        return HttpResponse(json.dumps({'fail': 'Auth failed'}))
    else:
        myprojects = [p.name for p in request.user.project_set.all()]
        myprojects.reverse()
        return HttpResponse(json.dumps(myprojects))

def latestprojects(request):
    latest = [p.name for p in Project.objects.order_by('-createdTime')]
    latest = latest[:10]
    return HttpResponse(json.dumps(latest))

def notices(request):
    return HttpResponse(json.dumps(['Notice', 'Notice', 'Notice']))

@login_required
def newprojectpage(request):
    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            p = Project(owner=request.user,
                        name=form.cleaned_data['name'],
                        summary=form.cleaned_data['summary'],
                        sprint=form.cleaned_data['sprint'],
                        sprintUnit=form.cleaned_data['sprintUnit'],
                        status='new')
            p.save()
            p.collaborators.add(request.user)
            return HttpResponseRedirect('/p/%s/' % p.name)
    else:
        form = CreateProjectForm()

    variables = RequestContext(request, {'form': form})
    return render_to_response('newproject.html', variables)

def productbacklogpage(request, project):
    if request.method == 'POST':
        try:
            form = AddBacklogForm(request.POST)
            p = Project.objects.get(name=project)
            if form.is_valid():
                if request.GET.get('am') == 'add':
                    backlog = BacklogItem()
                else:
                    backlog = BacklogItem.objects.get(name=form.cleaned_data['name'])
                backlog.name = form.cleaned_data['name']
                backlog.summary = form.cleaned_data['summary']
                backlog.description = form.cleaned_data['description']
                priority = form.cleaned_data['priority']
                if priority == 'High':
                    backlog.priority = 0
                elif priority == 'Medium':
                    backlog.priority = 1
                else:
                    backlog.priority = 2
                backlog.status = 'pending'
                backlog.project = p
                backlog.save()
        except ObjectDoesNotExist:
            pass
    try:
        p = Project.objects.get(name=project)
        owner = p.owner == request.user
    except:
        owner = None
    variables = RequestContext(request, {'request': request,
                                         'project': project,
                                         'owner': owner})
    return render_to_response('project/productbacklog.html', variables)

def ordinal(n):
    if n % 10 == 1:
        return '%dst' % n
    elif n % 10 == 2:
        return '%dnd' % n
    elif n % 10 == 3:
        return '%drd' % n
    else:
        return '%dth' % n

def getProgressAndIteration(p):
    today = datetime.date.today()
    if p.sprintUnit == 'days':
        delta = today - p.createdTime
        progress = (delta.days % p.sprint) * 100 / p.sprint
        iteration = delta.days / p.sprint + 1
    elif p.sprintUnit == 'weeks':
        delta = today - p.createdTime
        progress = (delta.days % (p.sprint * 7)) * 100 / (p.sprint * 7)
        iteration = delta.days / (p.sprint * 7) + 1
    else:
        monthDelta = relativedelta(months=+p.sprint, days=-1)
        sprintStartDate = p.createdTime
        sprintEndDate = sprintStartDate + monthDelta
        iteration = 1
        while sprintEndDate < today:
            sprintStartDate = sprintEndDate + relativedelta(days=+1)
            sprintEndDate = sprintStartDate + monthDelta
            iteration = iteration + 1
        progress = (today - sprintStartDate).days * 100
        progress = progress / (sprintEndDate - sprintStartDate).days

    return progress, iteration

def sprintbacklogpage(request, project):
    if request.method == 'POST':
        form = UpdateBacklogStatusForm(request.POST)
        if form.is_valid():
            try:
                backlog = BacklogItem.objects.get(name=form.cleaned_data['name'])
                backlog.status = form.cleaned_data['status']
                backlog.save()
            except:
                pass

    try:
        p = Project.objects.get(name=project)
        owner = p.owner == request.user
        progress, iteration = getProgressAndIteration(p)
        progress = 0
    except:
        owner = None

    variables = RequestContext(request, {'request': request,
                                         'project': project,
                                         'owner': owner,
                                         'sprint': p.sprint,
                                         'sprintUnit': p.sprintUnit,
                                         'iteration': ordinal(iteration),
                                         'progress': progress})
    return render_to_response('project/sprintbacklog.html', variables)

def assignjobpage(request, project):
    try:
        p = Project.objects.get(name=project)
        users = [user.username for user in p.collaborators.all()]
        variables = RequestContext(request, {'request': request,
                                             'project': project,
                                             'users': users})
    except:
        variables = RequestContext(request, {'request': request,
                                             'project': project})
    return render_to_response('project/assignjob.html', variables)

def assignjob(request, project, backlogname, username):
    try:
        p = Project.objects.get(name=project)
        backlog = BacklogItem.objects.filter(name=backlogname, project=p)[0]
        user = User.objects.get(username=username)
        backlog.status = 'assigned'
        backlog.assignedTo = user
        backlog.save()
        return HttpResponse(json.dumps({'status': 'success'}))
    except:
        return HttpResponse(json.dumps({'status': 'fail'}))

def disassignjob(request, project, backlogname):
    try:
        p = Project.objects.get(name=project)
        backlog = BacklogItem.objects.filter(name=backlogname, project=p)[0]
        backlog.status = 'pending'
        backlog.assignedTo = None
        backlog.save()
        return HttpResponse(json.dumps({'status': 'success'}))
    except:
        return HttpResponse(json.dumps({'status': 'fail'}))

def userstorypage(request, project):
    variables = RequestContext(request, {'request': request,
                                         'project': project})
    return render_to_response('project/userstory.html', variables)

def documentspage(request, project):
    variables = RequestContext(request, {'request': request,
                                         'project': project})
    return render_to_response('project/documents.html', variables)

def meetinglogpage(request, project):
    if request.method == 'POST':
        form = MeetingLogForm(request.POST)
        if form.is_valid():
            p = Project.objects.get(name=project)
            MeetingLog(project=p,
                       log=form.cleaned_data['meetinglog']).save()
                   
    meetinglogs = []
    logs = MeetingLog.objects.order_by('date')
    for log in logs:
        meetinglogs.append({'date': log.date, 'log': log.log})

    variables = RequestContext(request, {'request': request,
                                         'project': project,
                                         'meetinglogs': meetinglogs})
    return render_to_response('project/meetinglog.html', variables)

def dailyscrums(request, project, isodate):
    try:
        p = Project.objects.get(name=project)
        date = parser.parse(isodate).date()
        logsByDate = DailyScrum.objects.filter(date=date, project=p)
        result = {}
        for log in logsByDate:
            result[log.member.username] = {'jobDidYesterday': log.jobDidYesterday,
                                           'jobTodoToday': log.jobTodoToday}
        return HttpResponse(json.dumps(result))
    except:
        return HttpResponse(json.dumps({'fail': 'No such items'}))

def dailyscrumpage(request, project):
    if request.method == 'POST':
        form = WriteDailyScrumForm(request.POST)
        if form.is_valid():
            p = Project.objects.get(name=project)
            DailyScrum(project=p, member=request.user,
                       jobDidYesterday=form.cleaned_data['jobDidYesterday'],
                       jobTodoToday=form.cleaned_data['jobTodoToday']).save()

    today = datetime.date.today().isoformat()
    variables = RequestContext(request, {'request': request,
                                         'project': project,
                                         'today': today})
    return render_to_response('project/dailyscrum.html', variables)

def searchpage(request):
    variables = RequestContext(request, {'request': request})
    return render_to_response('search.html', variables)
                                         
def backloglist(request, project):
    try:
        p = Project.objects.get(name=project)
        backlogs = BacklogItem.objects.order_by('priority')
        backlogs = filter(lambda backlog: backlog.project == p, backlogs)
        result = {'todo': [], 'doing': [], 'done': []}
        for backlog in backlogs:
            item = {}
            item['name'] = backlog.name
            item['priority'] = backlog.priority
            if backlog.status == 'pending':
                result['todo'].append(item)
            elif backlog.status == 'assigned' or backlog.status == 'started':
                result['doing'].append(item)
            else:
                result['done'].append(item)
        return HttpResponse(json.dumps(result))
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({'fail': 'No such projects'}))

def sprintbackloglist(request, project):
    try:
        p = Project.objects.get(name=project)
        backlogs = BacklogItem.objects.filter(project=p,
                                              assignedTo=request.user)
        backlogs = filter(lambda backlog: backlog.status != 'done', backlogs)
        sprintBacklogs = {}
        for backlog in backlogs:
            sprintBacklogs[backlog.name] = backlog.status
        return HttpResponse(json.dumps(sprintBacklogs))
    except:
        return HttpResponse(json.dumps({'fail': 'No item'}))

def backlogdetail(request, project, name):
    try:
        p = Project.objects.get(name=project)
        backlog = BacklogItem.objects.get(name=name, project=p)
        detail = {}
        detail['name'] = backlog.name
        detail['summary'] = backlog.summary
        detail['description'] = backlog.description
        if backlog.assignedTo is not None:
            detail['assignedTo'] = backlog.assignedTo.username
        return HttpResponse(json.dumps(detail))
    except:
        return HttpResponse(json.dumps({'fail': 'No such item'}))
