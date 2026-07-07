from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Project, Status

User = get_user_model()


class ProjectTaskAPITests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='pass-12345')
        self.member = User.objects.create_user(username='member', password='pass-12345')
        self.outsider = User.objects.create_user(username='outsider', password='pass-12345')

    def test_register(self):
        resp = self.client.post(
            reverse('register'),
            {'username': 'newuser', 'password': 'StrongPass123'},
            format='json',
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_requires_authentication(self):
        resp = self.client.get('/api/projects/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_project_sets_owner(self):
        self.client.force_authenticate(user=self.owner)
        resp = self.client.post(
            '/api/projects/',
            {'name': 'P1', 'description': 'd'},
            format='json',
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['owner']['username'], 'owner')

    def test_member_can_read_but_not_edit(self):
        project = Project.objects.create(name='P', description='d', owner=self.owner)
        project.members.add(self.member)
        self.client.force_authenticate(user=self.member)
        read = self.client.get(f'/api/projects/{project.id}/')
        self.assertEqual(read.status_code, status.HTTP_200_OK)
        edit = self.client.patch(f'/api/projects/{project.id}/', {'name': 'X'}, format='json')
        self.assertEqual(edit.status_code, status.HTTP_403_FORBIDDEN)

    def test_outsider_cannot_see_project(self):
        project = Project.objects.create(name='P', description='d', owner=self.owner)
        self.client.force_authenticate(user=self.outsider)
        resp = self.client.get(f'/api/projects/{project.id}/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_update_and_delete(self):
        project = Project.objects.create(name='P', description='d', owner=self.owner)
        self.client.force_authenticate(user=self.owner)
        upd = self.client.patch(f'/api/projects/{project.id}/', {'name': 'P-upd'}, format='json')
        self.assertEqual(upd.status_code, status.HTTP_200_OK)
        self.assertEqual(upd.data['name'], 'P-upd')
        deleted = self.client.delete(f'/api/projects/{project.id}/')
        self.assertEqual(deleted.status_code, status.HTTP_204_NO_CONTENT)

    def test_task_crud_and_filter(self):
        project = Project.objects.create(name='P', description='d', owner=self.owner)
        self.client.force_authenticate(user=self.owner)
        created = self.client.post(
            '/api/tasks/',
            {'name': 'T1', 'description': 'd', 'project': project.id, 'status': Status.TO_DO},
            format='json',
        )
        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        listed = self.client.get(f'/api/tasks/?project={project.id}')
        self.assertEqual(listed.status_code, status.HTTP_200_OK)
        self.assertEqual(len(listed.data), 1)

    def test_cannot_create_task_in_foreign_project(self):
        project = Project.objects.create(name='P', description='d', owner=self.owner)
        self.client.force_authenticate(user=self.outsider)
        resp = self.client.post(
            '/api/tasks/',
            {'name': 'T', 'description': 'd', 'project': project.id},
            format='json',
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
