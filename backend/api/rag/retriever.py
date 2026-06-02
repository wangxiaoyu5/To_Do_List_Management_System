# 检索器模块
from typing import List, Dict, Any
from .config import RAGConfig
from .knowledge_base import KnowledgeBase


class Retriever:
    """任务检索器"""
    
    def __init__(self, knowledge_base: KnowledgeBase):
        """初始化检索器"""
        self.kb = knowledge_base
        self.top_k = RAGConfig.TOP_K_RESULTS
    
    def retrieve_similar_tasks(
        self, 
        query: str, 
        top_k: int = None, 
        filters: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """检索相似任务"""
        top_k = top_k or self.top_k
        
        if not self.kb.collection:
            # 如果没有向量数据库，返回空结果
            return []
        
        try:
            result = self.kb.collection.query(
                query_texts=[query],
                n_results=top_k,
                where=filters
            )
            
            # 格式化结果
            retrieved = []
            if result.get("documents") and result["documents"][0]:
                for i in range(len(result["documents"][0])):
                    doc = {
                        "content": result["documents"][0][i],
                        "metadata": result["metadatas"][0][i] if result.get("metadatas") else {},
                        "distance": result["distances"][0][i] if result.get("distances") else 0.0,
                        "task_id": result["ids"][0][i]
                    }
                    retrieved.append(doc)
            
            return retrieved
            
        except Exception as e:
            print(f"[RAG] 检索失败: {e}")
            return []
    
    def retrieve_by_keywords(
        self,
        keywords: List[str],
        tasks: List[Any],
        top_k: int = None
    ) -> List[Dict[str, Any]]:
        """基于关键词的简单检索（备用方案）"""
        top_k = top_k or self.top_k
        
        if not keywords or not tasks:
            return []
        
        keyword_list = [kw.lower() for kw in keywords]
        
        results = []
        for task in tasks:
            title = getattr(task, 'title', '').lower()
            description = getattr(task, 'description', '').lower()
            
            # 简单的关键词匹配
            score = 0
            for kw in keyword_list:
                if kw in title:
                    score += 3
                if kw in description:
                    score += 1
            
            if score > 0:
                results.append({
                    "task": task,
                    "score": score
                })
        
        # 按分数排序
        results.sort(key=lambda x: x["score"], reverse=True)
        
        # 格式化返回
        formatted = []
        for r in results[:top_k]:
            formatted.append({
                "task_id": str(r["task"].id),
                "title": getattr(r["task"], 'title', ''),
                "description": getattr(r["task"], 'description', ''),
                "score": r["score"]
            })
        
        return formatted
    
    def retrieve_completed_similar(
        self,
        query: str,
        top_k: int = None
    ) -> List[Dict[str, Any]]:
        """检索已完成的相似任务"""
        filters = {"completed": True}
        return self.retrieve_similar_tasks(query, top_k, filters)
    
    def retrieve_high_priority(
        self,
        query: str,
        top_k: int = None
    ) -> List[Dict[str, Any]]:
        """检索高优先级相似任务"""
        filters = {"priority": "HIGH"}
        return self.retrieve_similar_tasks(query, top_k, filters)
