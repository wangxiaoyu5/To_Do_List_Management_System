# 后端Python/Django代码规范

## 1. 项目结构规范

```
backend/
├── todo_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── api/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── permissions.py
│   ├── pagination.py
│   └── tests/
│       ├── __init__.py
│       ├── test_views.py
│       └── test_models.py
├── prisma/
│   ├── schema.prisma
│   └── migrations/
├── scripts/
│   └── seed_data.py
├── .env
├── .env.example
├── manage.py
└── requirements.txt
```

## 2. 命名规范

### 2.1 文件和模块
- **模块/包**：snake_case（如 `api/views.py`）
- **类**：PascalCase（如 `TaskViewSet`）
- **函数/方法**：snake_case（如 `get_queryset`）
- **变量**：snake_case（如 `task_list`）
- **常量**：UPPER_SNAKE_CASE（如 `MAX_PAGE_SIZE`）

### 2.2 Django特定命名
- **模型类**：单数名词（如 `Task`）
- **ViewSet**：模型名 + ViewSet（如 `TaskViewSet`）
- **Serializer**：模型名 + Serializer（如 `TaskSerializer`）
- **URL名称**：app名-model-action（如 `api:task-list`）

## 3. 代码风格规范

### 3.1 PEP 8合规
- 4空格缩进
- 每行最大长度120字符
- 使用空行分隔逻辑块
- 导入顺序：标准库 → 第三方库 → 本地模块

```python
# 正确的导入顺序
import os
import sys
from datetime import datetime

import django
from rest_framework import viewsets
from rest_framework.response import Response

from api.models import Task
from api.serializers import TaskSerializer
```

### 3.2 类型注解
使用类型注解提高代码可读性：

```python
from typing import List, Optional
from django.db.models import QuerySet
from api.models import Task

def get_user_tasks(user_id: str, priority: Optional[str] = None) -> QuerySet[Task]:
    queryset = Task.objects.filter(user_id=user_id)
    if priority:
        queryset = queryset.filter(priority=priority)
    return queryset
```

## 4. Django模型规范

### 4.1 模型定义
```python
# api/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Task(TimeStampedModel):
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        db_index=True
    )
    due_date = models.DateTimeField(null=True, blank=True, db_index=True)
    completed = models.BooleanField(default=False, db_index=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )
    tags = models.ManyToManyField('Tag', blank=True, related_name='tasks')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self) -> str:
        return self.title

    def mark_completed(self) -> None:
        self.completed = True
        self.completed_at = timezone.now()
        self.save()
```

### 4.2 模型最佳实践
- 继承抽象基类（如TimeStampedModel）
- 使用`related_name`定义反向关系
- 合理使用`db_index=True`优化查询
- 定义`__str__`方法便于调试
- 添加`Meta`类配置

## 5. Django REST Framework规范

### 5.1 Serializers
```python
# api/serializers.py
from rest_framework import serializers
from api.models import Task, Category, Tag


class TaskSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    tag_names = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'priority',
            'due_date', 'completed', 'completed_at',
            'category', 'category_name', 'tags', 'tag_names',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_tag_names(self, obj: Task) -> List[str]:
        return [tag.name for tag in obj.tags.all()]

    def validate_due_date(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError("Due date cannot be in the past")
        return value
```

### 5.2 ViewSets
```python
# api/views.py
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import QuerySet

from api.models import Task
from api.serializers import TaskSerializer
from api.permissions import IsOwner


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self) -> QuerySet[Task]:
        user = self.request.user
        queryset = Task.objects.filter(user=user)
        
        priority = self.request.query_params.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        completed = self.request.query_params.get('completed')
        if completed is not None:
            queryset = queryset.filter(completed=completed.lower() == 'true')
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = self.get_object()
        task.mark_completed()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
```

### 5.3 URL路由
```python
# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import TaskViewSet, CategoryViewSet, TagViewSet, AuthViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
]
```

## 6. 权限和认证规范

```python
# api/permissions.py
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
```

## 7. 错误处理规范

```python
# api/exceptions.py
from rest_framework.exceptions import APIException


class TaskNotFound(APIException):
    status_code = 404
    default_detail = 'Task not found'
    default_code = 'task_not_found'


class InvalidPriority(APIException):
    status_code = 400
    default_detail = 'Invalid priority value'
    default_code = 'invalid_priority'
```

## 8. 测试规范

```python
# api/tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from api.models import Task

User = get_user_model()


class TaskViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.task = Task.objects.create(
            title='Test Task',
            user=self.user
        )

    def test_list_tasks(self):
        url = reverse('api:task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_task(self):
        url = reverse('api:task-list')
        data = {'title': 'New Task'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
```

## 9. 配置管理规范

```python
# todo_project/settings.py
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    
    'api',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

## 10. 开发流程规范

### 10.1 单功能开发原则
每次只开发一个功能，完成一个功能后再开发下一个功能。

#### 开发流程
1. 选择一个功能（例如：创建任务API）
2. 编写该功能的完整实现
3. 调用相关skill检查代码（如 `backend-developer`、`TRAE-code-review`）
4. 确认无错误后，提交该功能
5. 再继续下一个功能

#### 错误示例
```python
# ❌ 错误：同时开发多个功能
# api/views.py
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    
    def create(self, request, *args, **kwargs):
        # 同时实现创建任务、发送通知、统计更新
        task = Task.objects.create(**request.data)
        send_notification(task.user)  # 另一个功能
        update_statistics(task.user)  # 第三个功能
        return Response(...)
```

#### 正确示例
```python
# ✅ 正确：一个功能一个功能开发
# api/views.py
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    
    # 第一步：先实现创建任务基本功能
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # 调用skill检查通过后，再开发下一个功能...
```

### 10.2 单路由单功能原则
每个路由只负责一个功能，不要在一个路由中实现多个功能。

#### 错误示例
```python
# ❌ 错误：一个路由做太多事情
# api/views.py
@action(detail=True, methods=['post'])
def multi_action(self, request, pk=None):
    # 同一个路由同时处理标记完成、修改优先级、更新截止日期
    action_type = request.data.get('type')
    
    if action_type == 'complete':
        task = self.get_object()
        task.completed = True
        task.save()
    elif action_type == 'priority':
        task = self.get_object()
        task.priority = request.data.get('priority')
        task.save()
    elif action_type == 'due_date':
        task = self.get_object()
        task.due_date = request.data.get('due_date')
        task.save()
    
    return Response(...)

# 对应URL: POST /api/tasks/{id}/multi-action
```

#### 正确示例
```python
# ✅ 正确：每个路由一个功能
# api/views.py
@action(detail=True, methods=['post'])
def complete(self, request, pk=None):
    # 单个功能：标记任务完成
    task = self.get_object()
    task.mark_completed()
    return Response(self.get_serializer(task).data)

@action(detail=True, methods=['patch'])
def update_priority(self, request, pk=None):
    # 单个功能：更新任务优先级
    task = self.get_object()
    task.priority = request.data.get('priority')
    task.save()
    return Response(self.get_serializer(task).data)

@action(detail=True, methods=['patch'])
def update_due_date(self, request, pk=None):
    # 单个功能：更新任务截止日期
    task = self.get_object()
    task.due_date = request.data.get('due_date')
    task.save()
    return Response(self.get_serializer(task).data)
```

#### 正确的URL路由示例
```python
# api/urls.py
# 每个功能有独立的路由
POST /api/tasks/{id}/complete          # 标记完成
PATCH /api/tasks/{id}/update-priority  # 更新优先级
PATCH /api/tasks/{id}/update-due-date  # 更新截止日期
```

### 10.3 功能验证流程
1. 完成功能编写
2. 运行相关检查（如 `python manage.py check`、测试）
3. 调用skill进行代码审查
4. 确认无错误后，**用户手动执行git提交**
5. 再开始下一个功能

## 11. Git提交规范

见 `git.md`
