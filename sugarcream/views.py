# -*- condig: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from sugarcream.forms import *
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

def mainpage(request):
    output = '<html><body>SugarCream</body></html>'
    return HttpResponse(output)

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
def userpage(request, username):
    try:
        user = User.objects.get(username=username)
        return HttpResponse('<html><body>%s</body></html>' % username)
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/')

@login_required
def projectpage(request, project):
    dummy = '<html><body>project %s page.</body></html>' % project
    return HttpResponse(dummy)
