# -*- condig: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
import re

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30)
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username must be letters, numbers and underscore(_) only.')
        try:
            User.objects.get(username=username)
        except:
            return username
        raise forms.ValidationError('Username is already in use.')

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Password does not match.')

class CreateProjectForm(forms.Form):
    name = forms.CharField(max_length=12)
    summary = forms.CharField(max_length=256)
    sprint = forms.IntegerField()
    sprintUnit = forms.CharField()

    def clean_name(self):
        name = self.cleaned_data['name']
        if not re.search(r'^\w+$', name):
            raise forms.ValidationError('Project name must be letters, numbers and underscore(_) only.')
        try:
            Project.object.get(name=name)
        except:
            return name
        raise forms.ValidationError('Project with same name already exists.')

class AddBacklogForm(forms.Form):
    name = forms.CharField(max_length=64)
    summary = forms.CharField(max_length=256)
    description = forms.CharField()
    priority = forms.CharField()

class WriteDailyScrumForm(forms.Form):
    jobDidYesterday = forms.CharField(max_length=256)
    jobTodoToday = forms.CharField(max_length=256)

class MeetingLogForm(forms.Form):
    meetinglog = forms.CharField()

class UserStoryForm(forms.Form):
    name = forms.CharField(max_length=32)
    story = forms.CharField()

class UpdateBacklogStatusForm(forms.Form):
    name = forms.CharField(max_length=64)
    status = forms.CharField(max_length=32)
