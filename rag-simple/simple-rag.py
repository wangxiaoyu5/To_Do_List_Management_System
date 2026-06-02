# ==========================================
# 最简单的 RAG 示例！
# 先不用向量数据库，用关键词搜索
# ==========================================

import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. 加载环境变量
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def load_knowledge():
    """加载知识库"""
    with open("my-knowledge.txt", "r", encoding="utf-8") as f:
        return f.read()


def simple_retrieve(question, knowledge):
    """
    简单的检索函数（用关键词匹配）
    实际 RAG 会用向量数据库，这里简化演示
    """
    # 把知识按任务分段
    tasks = knowledge.split("\n\n")
    
    # 找包含问题关键词的任务
    relevant_tasks = []
    for task in tasks:
        # 简单的关键词匹配
        if any(keyword in task for keyword in question.split()):
            relevant_tasks.append(task)
    
    # 如果没找到，返回前2个任务
    if not relevant_tasks:
        return "\n\n".join(tasks[:2])
    
    return "\n\n".join(relevant_tasks)


def generate_answer(question, context):
    """用 LLM 生成回答"""
    prompt = f"""你是一个任务管理助手。请根据以下参考资料回答用户的问题。

【参考资料】
{context}

【用户问题】
{question}

【要求】
1. 请根据参考资料回答
2. 如果参考资料中没有相关信息，请说"知识库中没有找到相关信息"
3. 回答要简洁

【回答】"""
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    
    return response.choices[0].message.content


def main():
    print("=" * 50)
    print("🤖 最简单的 RAG 系统")
    print("=" * 50)
    
    # 加载知识库
    print("\n📚 正在加载知识库...")
    knowledge = load_knowledge()
    print("✅ 知识库加载完成！")
    
    while True:
        question = input("\n❓ 问个问题（输入 quit 退出）：").strip()
        
        if question.lower() in ["quit", "exit"]:
            print("👋 再见！")
            break
        
        if not question:
            continue
        
        print("\n🔍 正在检索相关内容...")
        context = simple_retrieve(question, knowledge)
        
        print("🤖 正在生成回答...")
        answer = generate_answer(question, context)
        
        print(f"\n💡 回答：\n{answer}")
        print("-" * 50)


if __name__ == "__main__":
    main()
