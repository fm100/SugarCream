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
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/user/')

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
def userpage(request):
    variables = RequestContext(request, {'username': request.user.username})
    return render_to_response('user.html', variables)

def projectpage(request, project):
    try:
        p = Project.objects.get(name=project)
        variables = RequestContext(request,
                                   {'user': request.user, 'project': project})
        return render_to_response('project.html', variables)
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/')

def myprojects(request):
    if not request.user.is_authenticated():
        return HttpResponse(json.dumps({'fail': 'Auth failed'}))
    else:
        owned = [p.name for p in request.user.owned_project_set.all()]
        owned.reverse()
        myprojects = [p.name for p in request.user.project_set.all()]
        myprojects.reverse()
        return HttpResponse(json.dumps(owned + myprojects))

def allprojects(request):
    allprojects = [p.name for p in Project.objects.all()]
    allprojects.reverse()
    return HttpResponse(json.dumps(allprojects))

def notices(request):
    return HttpResponse(json.dumps(['Notice', 'Notice', 'Notice']))
