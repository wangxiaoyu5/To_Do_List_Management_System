# 知识库管理模块
from typing import List, Dict, Any
from django.conf import settings
from .config import RAGConfig

try:
    import chromadb
    from chromadb.utils import embedding_functions
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False


class KnowledgeBase:
    """任务知识库管理类"""
    
    def __init__(self, user_id: str):
        """初始化知识库"""
        self.user_id = str(user_id)
        self.collection_name = RAGConfig.get_collection_name(user_id)
        self.client = None
        self.collection = None
        self.embedding_function = None
        
        if CHROMA_AVAILABLE:
            self._init_chroma()
    
    def _init_chroma(self):
        """初始化 ChromaDB"""
        try:
            self.client = chromadb.PersistentClient(
                path=RAGConfig.CHROMA_PERSIST_DIR
            )
            
            # 初始化 Embedding 函数
            if RAGConfig.USE_OPENAI_EMBEDDING and RAGConfig.OPENAI_API_KEY:
                self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
                    api_key=RAGConfig.OPENAI_API_KEY,
                    model_name=RAGConfig.OPENAI_EMBEDDING_MODEL
                )
            else:
                # 使用本地 Embedding（如果可用）
                try:
                    self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
                        model_name=RAGConfig.LOCAL_EMBEDDING_MODEL
                    )
                except Exception:
                    # 如果本地 Embedding 不可用，使用默认
                    pass
            
            # 获取或创建集合
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function
            )
        except Exception as e:
            print(f"[RAG] ChromaDB 初始化失败: {e}")
    
    def format_task_for_rag(self, task: Any) -> str:
        """将任务格式化为 RAG 可用的文本"""
        # 获取任务的基本信息
        title = getattr(task, 'title', '')
        description = getattr(task, 'description', '') or ''
        priority = getattr(task, 'priority', 'MEDIUM')
        status = "已完成" if getattr(task, 'completed', False) else "进行中"
        
        # 获取分类
        category_name = ''
        category = getattr(task, 'category', None)
        if category:
            category_name = getattr(category, 'name', '')
        
        # 获取标签
        tag_names = []
        tags = getattr(task, 'tags', None)
        if tags:
            for tag in tags.all():
                tag_names.append(getattr(tag, 'name', ''))
        
        # 格式化文本
        content = f"""
任务标题: {title}
任务描述: {description}
优先级: {priority}
状态: {status}
分类: {category_name}
标签: {', '.join(tag_names)}
""".strip()
        
        return content
    
    def add_task(self, task: Any) -> bool:
        """添加任务到知识库"""
        if not self.collection:
            return False
        
        try:
            doc_id = str(task.id)
            content = self.format_task_for_rag(task)
            
            # 准备元数据
            metadata = {
                "task_id": doc_id,
                "title": getattr(task, 'title', ''),
                "priority": getattr(task, 'priority', 'MEDIUM'),
                "completed": getattr(task, 'completed', False),
            }
            
            # 添加到向量数据库
            self.collection.add(
                documents=[content],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
            print(f"[RAG] 任务已添加到知识库: {task.title}")
            return True
            
        except Exception as e:
            print(f"[RAG] 添加任务失败: {e}")
            return False
    
    def add_tasks(self, tasks: List[Any]) -> int:
        """批量添加任务到知识库"""
        count = 0
        for task in tasks:
            if self.add_task(task):
                count += 1
        return count
    
    def update_task(self, task: Any) -> bool:
        """更新知识库中的任务"""
        if not self.collection:
            return False
        
        try:
            doc_id = str(task.id)
            content = self.format_task_for_rag(task)
            metadata = {
                "task_id": doc_id,
                "title": getattr(task, 'title', ''),
                "priority": getattr(task, 'priority', 'MEDIUM'),
                "completed": getattr(task, 'completed', False),
            }
            
            # 更新文档
            self.collection.update(
                documents=[content],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
            print(f"[RAG] 任务已更新: {task.title}")
            return True
            
        except Exception as e:
            print(f"[RAG] 更新任务失败: {e}")
            return False
    
    def delete_task(self, task_id: str) -> bool:
        """从知识库中删除任务"""
        if not self.collection:
            return False
        
        try:
            self.collection.delete(ids=[str(task_id)])
            print(f"[RAG] 任务已删除: {task_id}")
            return True
        except Exception as e:
            print(f"[RAG] 删除任务失败: {e}")
            return False
    
    def sync_user_tasks(self, tasks: List[Any]) -> int:
        """同步用户的所有任务到知识库"""
        count = 0
        for task in tasks:
            self.add_task(task)
            count += 1
        return count
    
    def get_task_count(self) -> int:
        """获取知识库中的任务数量"""
        if not self.collection:
            return 0
        try:
            return self.collection.count()
        except Exception:
            return 0
