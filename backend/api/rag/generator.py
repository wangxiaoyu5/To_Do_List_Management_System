# 回答生成器模块
from typing import List, Dict, Any
from .config import RAGConfig

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AnswerGenerator:
    """LLM 回答生成器"""
    
    def __init__(self):
        """初始化生成器"""
        self.client = None
        
        if OPENAI_AVAILABLE and RAGConfig.OPENAI_API_KEY:
            try:
                self.client = OpenAI(api_key=RAGConfig.OPENAI_API_KEY)
            except Exception as e:
                print(f"[RAG] OpenAI 初始化失败: {e}")
    
    def _build_prompt_for_recommendations(
        self,
        new_task: Dict[str, str],
        similar_tasks: List[Dict[str, Any]]
    ) -> str:
        """构建任务推荐的提示词"""
        
        similar_text = "\n".join([
            f"【相似任务 {i+1}】\n{task.get('content', '')}"
            for i, task in enumerate(similar_tasks)
        ])
        
        prompt = f"""你是一个任务管理助手。用户正在创建一个新任务，请根据历史的相似任务给出建议。

新任务信息:
- 标题: {new_task.get('title', '')}
- 描述: {new_task.get('description', '')}
- 优先级: {new_task.get('priority', 'MEDIUM')}

历史相似任务:
{similar_text}

请给出以下方面的建议：
1. 根据历史经验，这个任务预计需要多长时间？
2. 有什么经验教训可以借鉴？
3. 其他建议

请用简洁的中文回答。"""
        
        return prompt
    
    def _build_prompt_for_query(
        self,
        query: str,
        related_tasks: List[Dict[str, Any]]
    ) -> str:
        """构建查询回答的提示词"""
        
        tasks_text = "\n".join([
            f"【相关任务 {i+1}】\n{task.get('content', '')}"
            for i, task in enumerate(related_tasks)
        ])
        
        prompt = f"""你是一个任务管理助手。请根据用户的问题和相关的任务信息，给出简洁的回答。

用户问题: {query}

相关任务信息:
{tasks_text}

请用简洁的中文回答用户的问题。"""
        
        return prompt
    
    def _build_prompt_for_chat(
        self,
        message: str,
        tasks_context: List[Dict[str, Any]]
    ) -> str:
        """构建对话的提示词"""
        
        context_text = "\n".join([
            f"【任务 {i+1}】\n{task.get('content', '')}"
            for i, task in enumerate(tasks_context)
        ])
        
        prompt = f"""你是一个友好的任务管理助手。请根据用户的消息和任务上下文，给出有用的回答。

用户消息: {message}

任务上下文:
{context_text}

请用友好、简洁的中文回答。"""
        
        return prompt
    
    def generate_recommendations(
        self,
        new_task: Dict[str, str],
        similar_tasks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """生成任务推荐"""
        
        if not similar_tasks:
            return {
                "suggestions": ["没有找到相似的历史任务"],
                "estimated_duration": {}
            }
        
        if not self.client:
            # 没有 LLM，返回简单的推荐
            return self._generate_simple_recommendations(similar_tasks)
        
        try:
            prompt = self._build_prompt_for_recommendations(new_task, similar_tasks)
            
            response = self.client.chat.completions.create(
                model=RAGConfig.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=RAGConfig.TEMPERATURE
            )
            
            answer = response.choices[0].message.content
            
            return {
                "suggestions": [answer],
                "similar_tasks_used": len(similar_tasks)
            }
            
        except Exception as e:
            print(f"[RAG] LLM 生成失败: {e}")
            return self._generate_simple_recommendations(similar_tasks)
    
    def _generate_simple_recommendations(
        self,
        similar_tasks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """简单的推荐（无 LLM）"""
        suggestions = []
        
        if similar_tasks:
            suggestions.append(f"找到了 {len(similar_tasks)} 个相似的历史任务")
            for task in similar_tasks[:2]:
                title = task.get("metadata", {}).get("title", "未知")
                suggestions.append(f"- 可以参考: {title}")
        
        return {
            "suggestions": suggestions,
            "similar_tasks_used": len(similar_tasks)
        }
    
    def generate_query_answer(
        self,
        query: str,
        related_tasks: List[Dict[str, Any]]
    ) -> str:
        """生成查询回答"""
        
        if not related_tasks:
            return "没有找到相关的任务。"
        
        if not self.client:
            # 简单回答
            return f"找到了 {len(related_tasks)} 个相关任务。"
        
        try:
            prompt = self._build_prompt_for_query(query, related_tasks)
            
            response = self.client.chat.completions.create(
                model=RAGConfig.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=RAGConfig.TEMPERATURE
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"[RAG] LLM 生成失败: {e}")
            return f"找到了 {len(related_tasks)} 个相关任务。"
    
    def generate_chat_answer(
        self,
        message: str,
        tasks_context: List[Dict[str, Any]]
    ) -> str:
        """生成对话回答"""
        
        if not tasks_context:
            return "我没有找到相关的任务信息。"
        
        if not self.client:
            return "我收到了你的消息，但 AI 功能需要配置 API Key。"
        
        try:
            prompt = self._build_prompt_for_chat(message, tasks_context)
            
            response = self.client.chat.completions.create(
                model=RAGConfig.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=RAGConfig.TEMPERATURE
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"[RAG] LLM 生成失败: {e}")
            return "抱歉，我遇到了一些问题。"
