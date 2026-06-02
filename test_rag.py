#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RAG 模块测试脚本
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# 导入 RAG 模块
from api.rag import RAGConfig, RAGService, get_rag_service

print("=" * 60)
print("RAG 模块测试")
print("=" * 60)

# 测试 1: 检查配置
print("\n[1] 检查配置...")
print(f"  - ChromaDB 路径: {RAGConfig.CHROMA_PERSIST_DIR}")
print(f"  - OpenAI API Key: {'已配置' if RAGConfig.OPENAI_API_KEY else '未配置'}")

# 测试 2: 创建 RAG 服务
print("\n[2] 创建 RAG 服务...")
try:
    rag_service = get_rag_service("test_user_123")
    print("  OK RAG 服务创建成功")
    
    # 检查知识库状态
    status = rag_service.get_kb_status()
    print(f"  - 知识库状态: {'可用' if status['has_kb'] else '不可用'}")
    print(f"  - 任务数量: {status['task_count']}")
    
except Exception as e:
    print(f"  ERROR 失败: {e}")

# 测试 3: 测试推荐功能
print("\n[3] 测试推荐功能...")
try:
    test_task = {
        "title": "设计用户数据库表",
        "description": "设计用户表和任务表的结构",
        "priority": "HIGH"
    }
    
    result = rag_service.get_task_recommendations(test_task, use_llm=False)
    print(f"  OK 推荐功能调用成功")
    print(f"  - 找到相似任务: {len(result['similar_tasks'])}")
    print(f"  - 推荐建议: {result['recommendations']['suggestions'][:1]}")
    
except Exception as e:
    print(f"  ERROR 失败: {e}")

# 测试 4: 测试查询功能
print("\n[4] 测试查询功能...")
try:
    query = "我最近完成了什么高优先级任务？"
    result = rag_service.query_tasks(query, use_llm=False)
    print(f"  OK 查询功能调用成功")
    print(f"  - 回答: {result['answer']}")
    print(f"  - 相关任务: {len(result['related_tasks'])}")
    
except Exception as e:
    print(f"  ERROR 失败: {e}")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)
