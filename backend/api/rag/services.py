# RAG 服务模块
from typing import List, Dict, Any
from .config import RAGConfig
from .knowledge_base import KnowledgeBase
from .retriever import Retriever
from .generator import AnswerGenerator


class RAGService:
    """RAG 服务主类"""
    
    def __init__(self, user_id: str):
        """初始化 RAG 服务"""
        self.user_id = str(user_id)
        self.knowledge_base = KnowledgeBase(user_id)
        self.retriever = Retriever(self.knowledge_base)
        self.generator = AnswerGenerator()
    
    def sync_task(self, task: Any, is_update: bool = False) -> bool:
        """同步单个任务到知识库"""
        if is_update:
            return self.knowledge_base.update_task(task)
        else:
            return self.knowledge_base.add_task(task)
    
    def delete_task_from_kb(self, task_id: str) -> bool:
        """从知识库删除任务"""
        return self.knowledge_base.delete_task(task_id)
    
    def sync_all_user_tasks(self, tasks: List[Any]) -> int:
        """同步用户所有任务"""
        return self.knowledge_base.sync_user_tasks(tasks)
    
    def get_task_recommendations(
        self,
        task_data: Dict[str, str],
        use_llm: bool = True
    ) -> Dict[str, Any]:
        """获取任务推荐"""
        # 构建查询
        query = f"{task_data.get('title', '')} {task_data.get('description', '')}"
        
        # 检索相似任务
        similar_tasks = self.retriever.retrieve_completed_similar(
            query,
            top_k=RAGConfig.TOP_K_RESULTS
        )
        
        # 生成推荐
        if use_llm:
            recommendations = self.generator.generate_recommendations(
                task_data,
                similar_tasks
            )
        else:
            recommendations = self.generator._generate_simple_recommendations(
                similar_tasks
            )
        
        return {
            "similar_tasks": similar_tasks,
            "recommendations": recommendations,
            "has_kb": self.knowledge_base.collection is not None
        }
    
    def query_tasks(
        self,
        query: str,
        use_llm: bool = True
    ) -> Dict[str, Any]:
        """自然语言查询任务"""
        # 检索相关任务
        related_tasks = self.retriever.retrieve_similar_tasks(
            query,
            top_k=RAGConfig.TOP_K_RESULTS
        )
        
        # 生成回答
        if use_llm and related_tasks:
            answer = self.generator.generate_query_answer(query, related_tasks)
        else:
            answer = f"找到了 {len(related_tasks)} 个相关任务"
        
        return {
            "answer": answer,
            "related_tasks": related_tasks,
            "has_kb": self.knowledge_base.collection is not None
        }
    
    def chat(
        self,
        message: str,
        tasks_context: List[Any] = None,
        use_llm: bool = True
    ) -> Dict[str, Any]:
        """AI 助手对话"""
        # 检索相关任务作为上下文
        if tasks_context:
            # 如果传入了任务，格式化它们
            formatted_tasks = []
            for task in tasks_context:
                content = self.knowledge_base.format_task_for_rag(task)
                formatted_tasks.append({"content": content})
            context_tasks = formatted_tasks
        else:
            # 否则从知识库检索
            context_tasks = self.retriever.retrieve_similar_tasks(
                message,
                top_k=RAGConfig.TOP_K_RESULTS
            )
        
        # 生成回答
        if use_llm:
            answer = self.generator.generate_chat_answer(message, context_tasks)
        else:
            answer = "我收到了你的消息！AI 功能需要配置 API Key。"
        
        return {
            "answer": answer,
            "context_used": len(context_tasks),
            "has_kb": self.knowledge_base.collection is not None
        }
    
    def estimate_duration(
        self,
        task_data: Dict[str, str],
        use_llm: bool = True
    ) -> Dict[str, Any]:
        """估算任务时长"""
        query = f"{task_data.get('title', '')} {task_data.get('description', '')}"
        
        # 检索相似任务
        similar_tasks = self.retriever.retrieve_completed_similar(
            query,
            top_k=5
        )
        
        # 简单估算
        estimation = {
            "min_days": 1,
            "max_days": 7,
            "avg_days": 3,
            "recommended_days": 3,
            "confidence": 0.5
        }
        
        if similar_tasks:
            estimation["confidence"] = 0.8
            estimation["based_on"] = len(similar_tasks)
        
        return {
            "estimation": estimation,
            "similar_tasks": similar_tasks
        }
    
    def get_kb_status(self) -> Dict[str, Any]:
        """获取知识库状态"""
        return {
            "has_kb": self.knowledge_base.collection is not None,
            "task_count": self.knowledge_base.get_task_count(),
            "collection_name": self.knowledge_base.collection_name,
            "use_openai": bool(RAGConfig.OPENAI_API_KEY)
        }


# 快捷函数
def get_rag_service(user_id: str) -> RAGService:
    """获取 RAG 服务实例"""
    return RAGService(user_id)
