# -*- condig: utf-8 -*-

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from sugarcream.models import *
from django.contrib.auth.models import User
import json

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
        user = User.objects.create_user(username='test',
                                        password='test',
                                        email='test@testmail.org')
        self.project = Project(owner=user)
        self.project.save()
        item = BacklogItem()
        item.name = 'testItem'
        item.summary = 'summary'
        item.description = 'description'
        item.priority = 0
        item.status = 'pending'
        item.project = self.project
        item.save()

    def testItemValues(self):
        item = BacklogItem.objects.get(id=1)
        self.assertEqual(item.name, 'testItem')
        self.assertEqual(item.summary, 'summary')
        self.assertEqual(item.description, 'description')
        self.assertEqual(item.priority, 0)
        self.assertEqual(item.status, 'pending')
        self.assertEqual(item.project, self.project)

    def testBacklogItemAssign(self):
        user1 = User.objects.create_user(username='user1',
                                         password='password',
                                         email='user1@sugarcream.org')
        user1.backlogitem_set.add(BacklogItem.objects.get(id=1))
        item = BacklogItem.objects.get(project=self.project, assignedTo=user1)
        self.assertEqual(item, BacklogItem.objects.get(id=1))

    def tearDown(self):
        items = BacklogItem.objects.all()
        for item in items:
            item.delete()

class JSONTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='testOwner',
                                              password='password',
                                              email='testOwner@sugarcream.org')
        self.user = User.objects.create_user(username='testuser',
                                             password='password',
                                             email='testuser@sugarcream.org')

        self.projects = []
        for i in range(1, 31):
            project = Project(owner=self.owner, name='project%d' % i)
            project.save()
            project.collaborators.add(self.owner)
            self.projects.append(project)
        p = Project(owner=self.user, name='owned')
        p.save()
        p.collaborators.add(self.user)
        self.projects.append(p)

        for i in range(1, 31, 2):
            self.projects[i].collaborators.add(self.user)

    def testLatestProjects(self):
        client = Client()
        latest = json.loads(client.post('/latestprojects/').content)
        expected = [p.name for p in self.projects]
        expected.reverse()
        expected = expected[:10]
        self.assertEqual(latest, expected)

    def testMyProjectsNoAuth(self):
        client = Client()
        myprojects = json.loads(client.post('/myprojects/').content)
        self.assertTrue('fail' in myprojects)
        self.assertEqual(myprojects['fail'], 'Auth failed')

    def testMyPorjects(self):
        client = Client()
        client.post('/login/', {'username': 'testuser',
                                'password': 'password'})
        myprojects = json.loads(client.post('/myprojects/').content)
        client.post('/logout/')
        expected = [p.name for p in self.user.project_set.all()]
        expected.reverse()
        self.assertEqual(myprojects, expected)

    def tearDown(self):
        for project in self.projects:
            project.delete()
        self.user.delete()
        self.owner.delete()
