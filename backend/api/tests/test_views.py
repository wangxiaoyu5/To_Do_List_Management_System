from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from prisma import Prisma


class BaseAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.prisma = Prisma()
        self.prisma.connect()
        
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
    
    def tearDown(self):
        self.prisma.disconnect()
    
    def register_user(self):
        response = self.client.post(
            reverse('api:register'),
            self.user_data,
            format='json'
        )
        return response
    
    def login_user(self):
        response = self.client.post(
            reverse('api:login'),
            {
                'username': self.user_data['username'],
                'password': self.user_data['password']
            },
            format='json'
        )
        return response
    
    def authenticate(self):
        self.register_user()
        response = self.login_user()
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')


class AuthAPITest(BaseAPITest):
    def test_register_user(self):
        response = self.register_user()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
    
    def test_login_user(self):
        self.register_user()
        response = self.login_user()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_invalid_login(self):
        response = self.client.post(
            reverse('api:login'),
            {
                'username': 'wronguser',
                'password': 'wrongpass'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TaskAPITest(BaseAPITest):
    def setUp(self):
        super().setUp()
        self.authenticate()
        self.task_data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'priority': 'MEDIUM'
        }
    
    def test_create_task(self):
        response = self.client.post(
            reverse('api:tasks-list-create'),
            self.task_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.task_data['title'])
    
    def test_list_tasks(self):
        self.client.post(
            reverse('api:tasks-list-create'),
            self.task_data,
            format='json'
        )
        response = self.client.get(reverse('api:tasks-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)


class CategoryAPITest(BaseAPITest):
    def setUp(self):
        super().setUp()
        self.authenticate()
        self.category_data = {
            'name': 'Test Category',
            'color': '#1890ff'
        }
    
    def test_create_category(self):
        response = self.client.post(
            reverse('api:categories-list-create'),
            self.category_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.category_data['name'])
    
    def test_list_categories(self):
        self.client.post(
            reverse('api:categories-list-create'),
            self.category_data,
            format='json'
        )
        response = self.client.get(reverse('api:categories-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)


class TagAPITest(BaseAPITest):
    def setUp(self):
        super().setUp()
        self.authenticate()
        self.tag_data = {
            'name': 'Test Tag',
            'color': '#52c41a'
        }
    
    def test_create_tag(self):
        response = self.client.post(
            reverse('api:tags-list-create'),
            self.tag_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.tag_data['name'])
    
    def test_list_tags(self):
        self.client.post(
            reverse('api:tags-list-create'),
            self.tag_data,
            format='json'
        )
        response = self.client.get(reverse('api:tags-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
