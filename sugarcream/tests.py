# -*- condig: utf-8 -*-

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from sugarcream.models import *
from django.contrib.auth.models import User

class ProjectTest(TestCase):
    def setUp(self):
        testOwner = User.objects.create_user(username='testOwner',
                                             password='password',
                                             email='testOwner@sugarcream.org')
        project1 = Project(owner=testOwner, name='project1')
        project1.save()
        project2 = Project(owner=testOwner, name='project2')
        project2.save()

    def testNameUniqueness(self):
        testOwner = User.objects.get(username='testOwner')
        try:
            project = Project(owner=testOwner, name='testProject')
            project.save()
            self.fail()
        except:
            pass

    def testOwner(self):
        project = Project.objects.get(id=1)
        self.assertEqual(project.owner.username, 'testOwner')
        owner = User.objects.get(username='testOwner')
        self.assertEqual(owner.owned_project_set.count(), 2)

    def testName(self):
        project = Project.objects.get(id=1)
        self.assertEqual(project.name, 'project1')

    def testCollaborators(self):
        user1 = User.objects.create_user(username='user1',
                                         password='password',
                                         email='user1@sugarcream.org')
        user2 = User.objects.create_user(username='user2',
                                         password='password',
                                         email='user2@sugarcream.org')
        user3 = User.objects.create_user(username='user3',
                                         password='password',
                                         email='user3@sugarcream.org')
        project1 = Project.objects.get(name='project1')
        project2 = Project.objects.get(name='project2')
        project1.collaborators.add(user1)
        project1.collaborators.add(user2)
        project2.collaborators.add(user2)
        project2.collaborators.add(user3)

        self.assertEqual(user1.project_set.count(), 1)
        self.assertEqual(user2.project_set.count(), 2)
        self.assertEqual(user3.project_set.count(), 1)

    def tearDown(self):
        projects = Project.objects.all()
        for project in projects:
            project.delete()
        users = User.objects.all()
        for user in users:
            user.delete()

class BacklogItemTest(TestCase):
    def setUp(self):
        item = BacklogItem()
        item.name = 'testItem'
        item.summary = 'summary'
        item.description = 'description'
        item.priority = 0
        item.status = 'pending'
        item.save()

    def testItemValues(self):
        item = BacklogItem.objects.get(id=1)
        self.assertEqual(item.name, 'testItem')
        self.assertEqual(item.summary, 'summary')
        self.assertEqual(item.description, 'description')
        self.assertEqual(item.priority, 0)
        self.assertEqual(item.status, 'pending')

    def tearDown(self):
        items = BacklogItem.objects.all()
        for item in items:
            item.delete()
