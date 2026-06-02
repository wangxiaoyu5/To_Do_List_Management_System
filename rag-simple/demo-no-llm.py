# ==========================================
# RAG 演示 - 不需要 LLM 的版本
# 只演示检索部分，让你理解 RAG 的核心
# ==========================================

def load_knowledge():
    """加载知识库"""
    with open("my-knowledge.txt", "r", encoding="utf-8") as f:
        content = f.read()
        # 跳过第一行标题，只保留任务部分
        tasks = content.split("\n\n")[1:]  # 跳过第一行
        return tasks


def simple_retrieve(question, tasks):
    """
    简单的检索函数（用关键词匹配）
    这就是 RAG 中的 "R" - Retrieval（检索）
    """
    print("\n[SEARCH] 正在检索与问题相关的内容...")
    print(f"   问题: {question}")
    
    # 简化的关键词，找核心词
    keywords = []
    question_lower = question.lower()
    
    if "数据库" in question or "database" in question_lower:
        keywords.append("数据库")
    if "文档" in question or "document" in question_lower:
        keywords.append("文档")
    if "react" in question_lower or "react" in question:
        keywords.append("React")
    if "时间" in question or "time" in question_lower:
        keywords.append("时间")
    if "经验" in question or "lesson" in question_lower:
        keywords.append("经验")
    if "学习" in question or "learn" in question_lower:
        keywords.append("学习")
    
    # 找匹配的任务
    relevant_tasks = []
    for i, task in enumerate(tasks):
        match_count = 0
        for kw in keywords:
            if kw in task:
                match_count += 1
        if match_count > 0:
            print(f"   [OK] 找到相关内容: 任务{i+1} (匹配度: {match_count})")
            relevant_tasks.append((match_count, task))
    
    # 按匹配度排序
    relevant_tasks.sort(reverse=True, key=lambda x: x[0])
    
    # 如果没找到，返回前2个任务
    if not relevant_tasks:
        print(f"   [WARN] 没找到完全匹配的，返回前2个任务")
        return "\n\n".join(tasks[:2])
    
    # 返回最相关的
    return "\n\n".join([task for (score, task) in relevant_tasks[:2]])


def demo():
    """演示 RAG 的检索部分"""
    print("=" * 60)
    print("RAG 检索演示（不需要 API Key）")
    print("=" * 60)
    print("\n这个程序演示 RAG 的核心：先找资料，再回答（这里只演示找资料）\n")
    
    # 加载知识库
    print("[LOAD] 正在加载知识库...")
    tasks = load_knowledge()
    print(f"[OK] 知识库加载完成！共 {len(tasks)} 个任务\n")
    
    # 演示问题
    test_questions = [
        "我做数据库设计花了多长时间？",
        "写文档有什么经验教训？",
        "学习React用了多久？",
        "如何管理时间？"
    ]
    
    for question in test_questions:
        print("\n" + "-"*60)
        print(f"问题: {question}")
        print("-"*60)
        
        # 检索
        context = simple_retrieve(question, tasks)
        
        print(f"\n检索到的内容:\n")
        print(context)
        print("\n[INFO] 这就是 RAG 中的 '检索' 步骤！")
        print("   然后这些内容会被传给 LLM 来生成最终回答\n")
    
    print("="*60)
    print("演示完成！")
    print("="*60)


if __name__ == "__main__":
    demo()
