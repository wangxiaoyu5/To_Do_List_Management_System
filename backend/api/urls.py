from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path('auth/register/', views.register, name='auth-register'),
    path('auth/login/', views.login, name='auth-login'),
    path('auth/user/', views.get_current_user, name='auth-user'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    path('categories/', views.categories_list_create, name='categories-list'),
    path('categories/<str:pk>/', views.categories_detail, name='categories-detail'),
    
    path('tags/', views.tags_list_create, name='tags-list'),
    path('tags/<str:pk>/', views.tags_detail, name='tags-detail'),
    
    path('tasks/', views.tasks_list_create, name='tasks-list'),
    path('tasks/<str:pk>/', views.tasks_detail, name='tasks-detail'),
    path('tasks/<str:pk>/toggle/', views.tasks_toggle_complete, name='tasks-toggle'),
    
    path('export/<str:format>/', views.export_data, name='export-data'),
    path('import/<str:format>/', views.import_data, name='import-data'),
    
    # RAG API
    path('rag/recommendations/', views.rag_recommendations, name='rag-recommendations'),
    path('rag/query/', views.rag_query, name='rag-query'),
    path('rag/chat/', views.rag_chat, name='rag-chat'),
    path('rag/sync/', views.rag_sync, name='rag-sync'),
    path('rag/status/', views.rag_status, name='rag-status'),
]
