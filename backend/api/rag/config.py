# RAG 模块配置
import os
from pathlib import Path

# 基础路径
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ChromaDB 数据存储路径
CHROMA_PERSIST_DIR = BASE_DIR / "data" / "chroma_db"
CHROMA_PERSIST_DIR.mkdir(parents=True, exist_ok=True)

# RAG 配置
class RAGConfig:
    # 向量数据库配置
    CHROMA_PERSIST_DIR = str(CHROMA_PERSIST_DIR)
    COLLECTION_NAME_PREFIX = "user_tasks_"
    
    # Embedding 配置
    USE_OPENAI_EMBEDDING = False  # 默认使用本地 Embedding
    OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
    LOCAL_EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    
    # LLM 配置
    USE_OPENAI_LLM = True
    OPENAI_MODEL = "gpt-3.5-turbo"
    TEMPERATURE = 0.7
    
    # 检索配置
    TOP_K_RESULTS = 3
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    
    # API 配置
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    @classmethod
    def get_collection_name(cls, user_id: str) -> str:
        """获取用户的向量集合名称"""
        return f"{cls.COLLECTION_NAME_PREFIX}{user_id}"
