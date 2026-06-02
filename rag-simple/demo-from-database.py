# ==========================================
# RAG 演示 - 从数据库读取任务
# 展示如何集成到你的待办事项系统
# ==========================================

# 模拟你的数据库任务数据（实际上会从 Django/Prisma 读取）
def get_tasks_from_database():
    """
    模拟从数据库读取任务
    在真实项目中，这里会调用 Django ORM 或 Prisma Client
    """
    return [
        {
            "id": "task_001",
            "title": "完成项目需求文档",
            "description": "编写详细的项目需求分析文档",
            "priority": "HIGH",
            "completed": True,
            "created_at": "2024-01-10",
            "completed_at": "2024-01-15",
            "category": "工作",
            "tags": ["文档", "需求"],
            "notes": "花了5天完成，主要难点是理清用户需求"
        },
        {
            "id": "task_002",
            "title": "数据库表结构设计",
            "description": "设计用户表、任务表、分类表",
            "priority": "HIGH",
            "completed": True,
            "created_at": "2024-01-18",
            "completed_at": "2024-01-20",
            "category": "工作",
            "tags": ["数据库", "设计"],
            "notes": "一开始设计太复杂，后来简化了"
        },
        {
            "id": "task_003",
            "title": "学习 React Hooks",
            "description": "深入学习 useState、useEffect",
            "priority": "MEDIUM",
            "completed": True,
            "created_at": "2024-01-25",
            "completed_at": "2024-02-01",
            "category": "学习",
            "tags": ["React", "前端"],
            "notes": "边学边练效果最好"
        },
        {
            "id": "task_004",
            "title": "开发 RAG 功能",
            "description": "为待办事项系统添加 RAG 智能推荐",
            "priority": "HIGH",
            "completed": False,
            "created_at": "2024-06-01",
            "category": "学习",
            "tags": ["AI", "RAG"],
            "notes": "正在学习中..."
        }
    ]


def format_task_for_rag(task):
    """把任务数据格式化成 RAG 能用的文本"""
    status = "已完成" if task["completed"] else "进行中"
    completed_at = task.get("completed_at", "未完成") or "未完成"
    return f"""
任务: {task['title']}
描述: {task['description'] or '无'}
优先级: {task['priority']}
状态: {status}
分类: {task['category']}
标签: {', '.join(task['tags'])}
创建时间: {task['created_at']}
完成时间: {completed_at}
备注: {task['notes'] or '无'}
""".strip()


def load_knowledge_from_db():
    """从数据库加载知识库"""
    print("[DB] 正在从数据库读取任务...")
    tasks = get_tasks_from_database()
    print(f"[OK] 从数据库读取了 {len(tasks)} 个任务")
    
    # 格式化成 RAG 文本
    formatted_tasks = [format_task_for_rag(task) for task in tasks]
    return tasks, formatted_tasks


def simple_retrieve(question, tasks, formatted_tasks):
    """
    从数据库任务中检索相关内容
    """
    print(f"\n[SEARCH] 正在检索与问题相关的任务...")
    print(f"   问题: {question}")
    
    # 关键词提取
    keywords = []
    question_lower = question.lower()
    
    if "数据库" in question or "database" in question_lower:
        keywords.append("数据库")
    if "文档" in question or "document" in question_lower:
        keywords.append("文档")
    if "react" in question_lower:
        keywords.append("React")
    if "RAG" in question or "rag" in question_lower:
        keywords.append("RAG")
    if "学习" in question:
        keywords.append("学习")
    if "完成" in question:
        keywords.append("已完成")
    
    # 找匹配的任务
    relevant_tasks = []
    for i, (task, formatted) in enumerate(zip(tasks, formatted_tasks)):
        match_count = 0
        
        # 检查关键词
        for kw in keywords:
            if kw in formatted:
                match_count += 1
        
        # 检查标题中的词
        title_words = task["title"].split()
        for word in title_words:
            if word in question:
                match_count += 1
        
        if match_count > 0:
            print(f"   [OK] 找到相关任务: {task['title']} (匹配度: {match_count})")
            relevant_tasks.append((match_count, task, formatted))
    
    # 按匹配度排序
    relevant_tasks.sort(reverse=True, key=lambda x: x[0])
    
    if not relevant_tasks:
        print(f"   [WARN] 没找到相关任务")
        return None
    
    # 返回最相关的
    return relevant_tasks[:2]


def demo():
    """演示从数据库读取的 RAG"""
    print("=" * 60)
    print("RAG 演示 - 从数据库读取任务")
    print("=" * 60)
    print("\n这个程序展示如何把 RAG 集成到你的待办事项系统\n")
    
    # 从数据库加载
    tasks, formatted_tasks = load_knowledge_from_db()
    
    # 演示问题
    test_questions = [
        "我做过数据库设计吗？",
        "学习 React 的任务是什么？",
        "RAG 相关的任务有哪些？",
        "已完成的高优先级任务有哪些？"
    ]
    
    for question in test_questions:
        print("\n" + "-"*60)
        print(f"问题: {question}")
        print("-"*60)
        
        # 检索
        results = simple_retrieve(question, tasks, formatted_tasks)
        
        if results:
            print(f"\n[OK] 找到 {len(results)} 个相关任务:\n")
            for i, (score, task, formatted) in enumerate(results):
                print(f"--- 任务 {i+1} (匹配度: {score}) ---")
                print(formatted)
                print()
        else:
            print("\n[INFO] 没找到相关任务")
    
    print("="*60)
    print("\n[INFO] 在真实项目中，这就是 RAG 的工作方式！")
    print("   1. 从你的数据库读取任务")
    print("   2. 用户问问题")
    print("   3. 检索相关历史任务")
    print("   4. 传给 LLM 生成智能回答")
    print("="*60)


if __name__ == "__main__":
    demo()
