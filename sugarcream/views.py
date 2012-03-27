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
