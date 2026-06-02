from datetime import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpRequest, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category, Tag, Task
from .serializers import (
    UserSerializer,
    LoginSerializer,
    CategorySerializer,
    TagSerializer,
    TaskSerializer,
)

# RAG 导入
try:
    from .rag import get_rag_service
    RAG_AVAILABLE = True
except Exception as e:
    print(f"RAG 模块未加载: {e}")
    RAG_AVAILABLE = False

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request: HttpRequest) -> Response:
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    
    try:
        if User.objects.filter(username=data['username']).exists():
            return Response(
                {'error': 'Username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(email=data['email']).exists():
            return Response(
                {'error': 'Email already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.create(
            username=data['username'],
            email=data['email'],
            password=make_password(data['password']),
        )
        
        preset_categories = ['工作', '个人', '学习', '其他']
        for cat_name in preset_categories:
            Category.objects.create(name=cat_name, user=user)
        
        refresh = RefreshToken.for_user(user)
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'createdAt': user.date_joined,
        }
        
        return Response({
            'user': user_data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request: HttpRequest) -> Response:
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    
    try:
        user = User.objects.filter(username=data['username']).first()
        
        if not user or not check_password(data['password'], user.password):
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        refresh = RefreshToken.for_user(user)
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'createdAt': user.date_joined,
        }
        
        return Response({
            'user': user_data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request: HttpRequest) -> Response:
    user = request.user
    
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'createdAt': user.date_joined,
    }
    return Response(user_data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def categories_list_create(request: HttpRequest) -> Response:
    user = request.user
    
    if request.method == 'GET':
        try:
            categories = Category.objects.filter(user=user).order_by('-created_at')
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        try:
            category = Category.objects.create(
                name=data['name'],
                color=data.get('color', '#1890ff'),
                user=user,
            )
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def categories_detail(request: HttpRequest, pk: str) -> Response:
    user = request.user
    
    try:
        category = Category.objects.filter(id=pk, user=user).first()
        if not category:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'PUT':
            serializer = CategorySerializer(data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            data = serializer.validated_data
            if 'name' in data:
                category.name = data['name']
            if 'color' in data:
                category.color = data['color']
            category.save()
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        
        elif request.method == 'DELETE':
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def tags_list_create(request: HttpRequest) -> Response:
    user = request.user
    
    if request.method == 'GET':
        try:
            tags = Tag.objects.filter(user=user).order_by('-created_at')
            serializer = TagSerializer(tags, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'POST':
        serializer = TagSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        try:
            tag = Tag.objects.create(
                name=data['name'],
                color=data.get('color', '#52c41a'),
                user=user,
            )
            serializer = TagSerializer(tag)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def tags_detail(request: HttpRequest, pk: str) -> Response:
    user = request.user
    
    try:
        tag = Tag.objects.filter(id=pk, user=user).first()
        if not tag:
            return Response({'error': 'Tag not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'PUT':
            serializer = TagSerializer(data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            data = serializer.validated_data
            if 'name' in data:
                tag.name = data['name']
            if 'color' in data:
                tag.color = data['color']
            tag.save()
            serializer = TagSerializer(tag)
            return Response(serializer.data)
        
        elif request.method == 'DELETE':
            tag.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def serialize_task_with_relations(task):
    category = None
    if task.category:
        category = {
            'id': task.category.id,
            'name': task.category.name,
            'color': task.category.color,
            'createdAt': task.category.created_at,
        }
    
    task_tags = task.task_tags.all()
    tags = []
    for tt in task_tags:
        tags.append({
            'id': tt.tag.id,
            'name': tt.tag.name,
            'color': tt.tag.color,
            'createdAt': tt.tag.created_at,
        })
    
    return {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'priority': task.priority,
        'dueDate': task.due_date,
        'completed': task.completed,
        'completedAt': task.completed_at,
        'createdAt': task.created_at,
        'updatedAt': task.updated_at,
        'categoryId': task.category_id,
        'category': category,
        'tags': tags,
    }


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def tasks_list_create(request: HttpRequest) -> Response:
    user = request.user
    
    if request.method == 'GET':
        try:
            queryset = Task.objects.filter(user=user)
            
            priority = request.query_params.get('priority')
            if priority:
                queryset = queryset.filter(priority=priority)
            
            category_id = request.query_params.get('categoryId')
            if category_id:
                queryset = queryset.filter(category_id=category_id)
            
            completed = request.query_params.get('completed')
            if completed is not None:
                queryset = queryset.filter(completed=completed.lower() == 'true')
            
            search = request.query_params.get('search')
            if search:
                queryset = queryset.filter(title__icontains=search)
            
            tasks = queryset.order_by('-created_at')
            
            result_tasks = [serialize_task_with_relations(t) for t in tasks]
            return Response(result_tasks)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        tag_ids = data.get('tag_ids', [])
        
        try:
            category = None
            if data.get('category_id'):
                category = Category.objects.filter(id=data['category_id'], user=user).first()
            
            task = Task.objects.create(
                title=data['title'],
                description=data.get('description'),
                priority=data.get('priority', 'MEDIUM'),
                due_date=data.get('due_date'),
                user=user,
                category=category,
            )
            
            if tag_ids:
                for tag_id in tag_ids:
                    tag = Tag.objects.filter(id=tag_id, user=user).first()
                    if tag:
                        task.tags.add(tag)
            
            # 同步到 RAG 知识库
            try:
                if RAG_AVAILABLE:
                    rag_service = get_rag_service(user.id)
                    rag_service.sync_task(task)
            except Exception:
                pass  # 静默失败，不影响主功能
            
            result_task = serialize_task_with_relations(task)
            return Response(result_task, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def tasks_detail(request: HttpRequest, pk: str) -> Response:
    user = request.user
    
    try:
        task = Task.objects.filter(id=pk, user=user).first()
        if not task:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            result_task = serialize_task_with_relations(task)
            return Response(result_task)
        
        elif request.method == 'PUT':
            serializer = TaskSerializer(data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            data = serializer.validated_data
            
            if 'title' in data:
                task.title = data['title']
            if 'description' in data:
                task.description = data['description']
            if 'priority' in data:
                task.priority = data['priority']
            if 'due_date' in data:
                task.due_date = data['due_date']
            if 'completed' in data:
                task.completed = data['completed']
                if task.completed:
                    task.completed_at = datetime.now()
                else:
                    task.completed_at = None
            if 'category_id' in data:
                if data['category_id']:
                    category = Category.objects.filter(id=data['category_id'], user=user).first()
                    task.category = category
                else:
                    task.category = None
            
            task.save()
            
            if 'tag_ids' in data:
                task.tags.clear()
                for tag_id in data['tag_ids']:
                    tag = Tag.objects.filter(id=tag_id, user=user).first()
                    if tag:
                        task.tags.add(tag)
            
            result_task = serialize_task_with_relations(task)
            return Response(result_task)
        
        elif request.method == 'DELETE':
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def tasks_toggle_complete(request: HttpRequest, pk: str) -> Response:
    user = request.user
    
    try:
        task = Task.objects.filter(id=pk, user=user).first()
        if not task:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        
        task.completed = not task.completed
        if task.completed:
            task.completed_at = datetime.now()
        else:
            task.completed_at = None
        task.save()
        
        result_task = serialize_task_with_relations(task)
        return Response(result_task)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_data(request: HttpRequest, format: str) -> Response:
    user = request.user
    
    try:
        categories = Category.objects.filter(user=user)
        tags = Tag.objects.filter(user=user)
        tasks = Task.objects.filter(user=user)
        
        data = {
            'categories': [{'id': c.id, 'name': c.name, 'color': c.color} for c in categories],
            'tags': [{'id': t.id, 'name': t.name, 'color': t.color} for t in tags],
            'tasks': [],
        }
        
        for task in tasks:
            tag_ids = [t.id for t in task.tags.all()]
            data['tasks'].append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'priority': task.priority,
                'dueDate': task.due_date,
                'completed': task.completed,
                'completedAt': task.completed_at,
                'categoryId': task.category_id,
                'tagIds': tag_ids,
            })
        
        if format == 'json':
            return Response(data, content_type='application/json')
        elif format == 'csv':
            import csv
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="todos_export.csv"'
            
            writer = csv.writer(response)
            writer.writerow(['Type', 'ID', 'Title', 'Description', 'Priority', 'Due Date', 'Completed', 'Category', 'Tags'])
            
            for task in data['tasks']:
                category_name = next((c['name'] for c in data['categories'] if c['id'] == task['categoryId']), '')
                tag_names = [t['name'] for t in data['tags'] if t['id'] in task['tagIds']]
                writer.writerow([
                    'Task',
                    task['id'],
                    task['title'],
                    task['description'] or '',
                    task['priority'],
                    task['dueDate'] or '',
                    task['completed'],
                    category_name,
                    ','.join(tag_names),
                ])
            
            return response
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def import_data(request: HttpRequest, format: str) -> Response:
    user = request.user
    
    try:
        if format == 'json':
            data = request.data
            
            category_map = {}
            for cat in data.get('categories', []):
                new_cat = Category.objects.create(
                    name=cat['name'],
                    color=cat.get('color', '#1890ff'),
                    user=user
                )
                category_map[cat['id']] = new_cat.id
            
            tag_map = {}
            for tag in data.get('tags', []):
                new_tag = Tag.objects.create(
                    name=tag['name'],
                    color=tag.get('color', '#52c41a'),
                    user=user
                )
                tag_map[tag['id']] = new_tag.id
            
            imported_tasks = []
            for task_data in data.get('tasks', []):
                category_id = category_map.get(task_data.get('categoryId'))
                category = None
                if category_id:
                    category = Category.objects.filter(id=category_id, user=user).first()
                
                task = Task.objects.create(
                    title=task_data['title'],
                    description=task_data.get('description'),
                    priority=task_data.get('priority', 'MEDIUM'),
                    due_date=task_data.get('dueDate'),
                    completed=task_data.get('completed', False),
                    completed_at=task_data.get('completedAt'),
                    user=user,
                    category=category,
                )
                
                for old_tag_id in task_data.get('tagIds', []):
                    if old_tag_id in tag_map:
                        tag = Tag.objects.filter(id=tag_map[old_tag_id], user=user).first()
                        if tag:
                            task.tags.add(tag)
                
                imported_tasks.append(task)
            
            return Response({'message': f'Imported {len(imported_tasks)} tasks'})
        else:
            return Response({'error': 'Unsupported format'}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ========================================
# RAG API Views
# ========================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rag_recommendations(request: HttpRequest) -> Response:
    """获取任务推荐"""
    if not RAG_AVAILABLE:
        return Response({
            'similar_tasks': [],
            'recommendations': {'suggestions': ['RAG 功能暂不可用']}
        })
    
    try:
        rag_service = get_rag_service(request.user.id)
        
        task_data = {
            'title': request.data.get('title', ''),
            'description': request.data.get('description', ''),
            'priority': request.data.get('priority', 'MEDIUM')
        }
        
        result = rag_service.get_task_recommendations(task_data, use_llm=False)
        return Response(result)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rag_query(request: HttpRequest) -> Response:
    """自然语言查询"""
    if not RAG_AVAILABLE:
        return Response({
            'answer': 'RAG 功能暂不可用',
            'related_tasks': []
        })
    
    try:
        rag_service = get_rag_service(request.user.id)
        query = request.data.get('query', '')
        
        result = rag_service.query_tasks(query, use_llm=False)
        return Response(result)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rag_chat(request: HttpRequest) -> Response:
    """AI 助手对话"""
    if not RAG_AVAILABLE:
        return Response({
            'answer': 'RAG 功能暂不可用',
            'context_used': 0
        })
    
    try:
        rag_service = get_rag_service(request.user.id)
        message = request.data.get('message', '')
        
        result = rag_service.chat(message, use_llm=False)
        return Response(result)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rag_sync(request: HttpRequest) -> Response:
    """同步用户的任务到知识库"""
    if not RAG_AVAILABLE:
        return Response({'message': 'RAG 功能暂不可用'})
    
    try:
        rag_service = get_rag_service(request.user.id)
        tasks = Task.objects.filter(user=request.user)
        
        count = 0
        for task in tasks:
            if rag_service.sync_task(task):
                count += 1
        
        status = rag_service.get_kb_status()
        
        return Response({
            'message': f'Synced {count} tasks',
            'status': status
        })
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rag_status(request: HttpRequest) -> Response:
    """获取 RAG 知识库状态"""
    if not RAG_AVAILABLE:
        return Response({
            'has_kb': False,
            'task_count': 0,
            'rag_available': False
        })
    
    try:
        rag_service = get_rag_service(request.user.id)
        status = rag_service.get_kb_status()
        status['rag_available'] = True
        return Response(status)
    
    except Exception as e:
        return Response({
            'has_kb': False,
            'task_count': 0,
            'rag_available': False,
            'error': str(e)
        })
