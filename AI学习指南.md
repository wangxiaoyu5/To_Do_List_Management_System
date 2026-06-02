# AI 应用开发实战学习指南

> 基于你的待办事项管理系统项目，从零到一逐步掌握 AI 应用开发核心技能。
> 每个任务对应一个技能点，完成后即可确认你已掌握该能力。

---

## 📊 技能自测对照表

| 任务 | 对应技能 | 所属层级 |
|------|----------|----------|
| 任务 1 | Python + 大模型 API 调用 | 基础层 1、2 |
| 任务 2 | Prompt 工程 + 多轮对话 | 基础层 3 |
| 任务 3 | RAG 文档问答 | 基础层 4 |
| 任务 4 | Gradio/Streamlit 界面 | 基础层 5 |
| 任务 5 | Function Calling | 进阶层 1 |
| 任务 6 | 对话记忆管理 | 进阶层 2 |
| 任务 7 | LangChain 流程串联 | 进阶层 3 |
| 任务 8 | Agent 核心概念 | 进阶层 4 |
| 任务 9 | FastAPI 封装 + 部署 | 工程层 1 |
| 任务 10 | 异常/并发/日志/会话隔离 | 工程层 2 |

---

## 任务 1：大模型 API 调用 — 任务智能建议

### 🎯 目标
在你的待办系统中添加一个 AI 助手，用户输入自然语言，AI 返回结构化的任务建议。

### 📚 你需要学会的知识

1. **选择一个大模型平台并注册**
   - 国内推荐：通义千问（免费额度多）、文心一言
   - 国际推荐：OpenAI（需科学上网）
   - 注册后获取 API Key

2. **安装 Python SDK**
   ```bash
   # 通义千问
   pip install dashscope

   # OpenAI
   pip install openai

   # 文心一言
   pip install qianfan
   ```

3. **理解 API 调用的基本流程**
   ```
   你的代码 → 构造请求（API Key + Prompt） → 发送到大模型 → 接收响应 → 解析结果
   ```

### 🔨 分步实现

#### 第一步：独立测试 API 调用

先写一个独立的 Python 脚本，确认你能成功调用大模型：

```python
# test_api.py — 放在 backend/ 目录下
# 以通义千问为例，其他平台类似

import dashscope
from dashscope import Generation

dashscope.api_key = "你的API Key"

def call_llm(prompt: str) -> str:
    response = Generation.call(
        model='qwen-turbo',
        prompt=prompt,
    )
    return response.output.text

if __name__ == "__main__":
    result = call_llm("帮我生成3个学习任务的建议，每个包含标题和优先级")
    print(result)
```

**✅ 完成标准**：运行脚本后，能看到大模型返回的文字内容。

#### 第二步：设计结构化输出

让大模型返回 JSON 格式，方便前端使用：

```python
# 修改 prompt，要求返回 JSON
prompt = """
你是一个任务管理助手。用户会描述他们的需求，你需要生成任务建议。

请严格按以下 JSON 格式返回：
[
  {
    "title": "任务标题",
    "description": "任务描述",
    "priority": "high/medium/low",
    "due_date": "建议截止日期"
  }
]

用户需求：帮我安排下周的 Python 学习计划
"""
```

**✅ 完成标准**：大模型返回的内容可以被 `json.loads()` 解析。

#### 第三步：集成到 Django 后端

1. 在 `backend/api/` 下新建 `ai_service.py`：

```python
# ai_service.py — 封装 AI 调用逻辑
import json
import dashscope
from dashscope import Generation

dashscope.api_key = "你的API Key"

def suggest_tasks(user_input: str) -> list:
    prompt = f"""
你是一个任务管理助手。用户会描述他们的需求，你需要生成任务建议。

请严格按以下 JSON 数组格式返回，不要包含其他文字：
[
  {{
    "title": "任务标题",
    "description": "任务描述",
    "priority": "high/medium/low",
    "due_date": "建议截止日期，格式 YYYY-MM-DD"
  }}
]

用户需求：{user_input}
"""
    response = Generation.call(
        model='qwen-turbo',
        prompt=prompt,
    )
    text = response.output.text
    # 尝试解析 JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # 如果返回的不是纯 JSON，尝试提取
        start = text.find('[')
        end = text.rfind(']') + 1
        return json.loads(text[start:end])
```

2. 在 `backend/api/views.py` 中添加视图：

```python
# 在 views.py 中添加
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .ai_service import suggest_tasks

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ai_task_suggestion(request):
    user_input = request.data.get('input', '')
    if not user_input:
        return Response(
            {'error': '请输入需求描述'},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        suggestions = suggest_tasks(user_input)
        return Response({'suggestions': suggestions})
    except Exception as e:
        return Response(
            {'error': f'AI 服务异常: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
```

3. 在 `backend/api/urls.py` 中添加路由：

```python
# 在 urls.py 的 urlpatterns 中添加
path('ai/task-suggestion/', ai_task_suggestion, name='ai-task-suggestion'),
```

**✅ 完成标准**：用 Postman 或 curl 调用 `/api/ai/task-suggestion/` 能返回任务建议。

#### 第四步：前端集成

1. 在 `frontend/src/services/api.ts` 中添加：

```typescript
aiTaskSuggestion: (input: string) =>
  api.post('/ai/task-suggestion/', { input }),
```

2. 在任务创建页面添加"AI 建议"按钮，点击后调用接口，将返回结果填充到表单。

**✅ 完成标准**：点击"AI 建议"按钮，输入需求后，表单自动填充 AI 建议的任务。

### 🧪 自测问题

- [ ] 你能独立写一个 Python 脚本调用大模型 API 吗？
- [ ] 你能让大模型返回结构化的 JSON 数据吗？
- [ ] 你能把 AI 功能集成到 Django 后端吗？

如果三个都是 ✅，恭喜你已掌握 **基础层 1、2**！

---

## 任务 2：Prompt 工程 — 智能任务分类

### 🎯 目标
让 AI 根据任务标题和描述，自动推荐最合适的分类和标签。

### 📚 你需要学会的知识

1. **Prompt 的核心要素**
   - **角色设定**：告诉 AI 它是谁
   - **任务描述**：告诉 AI 要做什么
   - **约束条件**：告诉 AI 不能做什么
   - **输出格式**：告诉 AI 按什么格式返回
   - **示例（Few-shot）**：给 AI 几个例子

2. **多轮上下文拼接**
   - 把系统的分类列表和标签列表拼接到 Prompt 中
   - 让 AI 只从已有选项中选择

### 🔨 分步实现

#### 第一步：理解 Prompt 设计模式

```python
# 一个好的 Prompt 结构
prompt = """
【角色】你是一个任务分类专家。

【任务】根据用户输入的任务信息，从给定的分类和标签中选择最合适的。

【可选分类】
{categories}

【可选标签】
{tags}

【输出格式】严格按以下 JSON 返回：
{{
  "category": "分类名称",
  "tags": ["标签1", "标签2"],
  "confidence": 0.9
}}

【示例】
输入：完成季度销售报告
输出：{{"category": "工作", "tags": ["报告", "紧急"], "confidence": 0.95}}

用户输入：{user_input}
"""
```

#### 第二步：实现分类服务

在 `backend/api/ai_service.py` 中添加：

```python
def classify_task(title: str, description: str, categories: list, tags: list) -> dict:
    category_names = [c['name'] for c in categories]
    tag_names = [t['name'] for t in tags]

    prompt = f"""
你是一个任务分类专家。根据任务信息，从给定的分类和标签中选择最合适的。

可选分类：{', '.join(category_names)}
可选标签：{', '.join(tag_names)}

严格按以下 JSON 格式返回：
{{"category": "分类名称", "tags": ["标签1", "标签2"]}}

任务标题：{title}
任务描述：{description}
"""
    response = Generation.call(model='qwen-turbo', prompt=prompt)
    text = response.output.text
    # 解析 JSON（同任务1的解析逻辑）
    ...
```

#### 第三步：添加 API 端点并集成前端

流程同任务 1，添加 `/api/ai/classify-task/` 端点。

**✅ 完成标准**：输入任务标题后，AI 能准确推荐分类和标签。

### 🧪 自测问题

- [ ] 你能设计一个包含角色、任务、约束、格式的 Prompt 吗？
- [ ] 你能用 Few-shot 示例提高 AI 输出的准确性吗？
- [ ] 你能把动态数据（分类列表）拼接到 Prompt 中吗？

如果三个都是 ✅，恭喜你已掌握 **基础层 3**！

---

## 任务 3：RAG 基础 — 任务知识库

### 🎯 目标
将用户的历史任务向量化存储，创建新任务时自动检索相似任务作为参考。

### 📚 你需要学会的知识

1. **RAG 的核心流程**
   ```
   文档 → 分块 → 向量化 → 存入向量库
                              ↓
   查询 → 向量化 → 在向量库中检索相似内容 → 拼接到 Prompt → 大模型生成回答
   ```

2. **关键概念**
   - **Embedding**：把文字变成数字向量，语义相近的文字向量也相近
   - **分块（Chunking）**：把长文档切成小段
   - **向量库**：存储和检索向量的数据库

3. **安装依赖**
   ```bash
   pip install chromadb sentence-transformers
   ```

### 🔨 分步实现

#### 第一步：独立测试向量化和检索

```python
# test_rag.py
import chromadb

# 创建内存向量库
client = chromadb.Client()
collection = client.create_collection("tasks")

# 添加一些任务
collection.add(
    documents=["完成季度销售报告", "学习 Python 基础", "准备项目演示"],
    ids=["task1", "task2", "task3"]
)

# 检索相似任务
results = collection.query(
    query_texts=["写月度工作总结"],
    n_results=2
)
print(results['documents'])
# 预期输出：['完成季度销售报告', ...]（语义最相似）
```

**✅ 完成标准**：检索结果中，语义相似的任务排在前面。

#### 第二步：持久化向量库

```python
# 使用本地存储，重启后数据不丢失
client = chromadb.PersistentClient(path="./chroma_db")
```

#### 第三步：集成到待办系统

1. 创建任务时，同步写入向量库
2. 创建新任务前，先检索相似任务
3. 将相似任务信息返回给前端展示

**✅ 完成标准**：创建新任务时，能看到相关的历史任务参考。

### 🧪 自测问题

- [ ] 你理解 RAG 的完整流程吗？
- [ ] 你能用 ChromaDB 存储和检索向量吗？
- [ ] 你能把检索结果拼接到 Prompt 中让 AI 参考回答吗？

如果三个都是 ✅，恭喜你已掌握 **基础层 4**！

---

## 任务 4：Gradio/Streamlit 界面 — AI 助手面板

### 🎯 目标
用 Streamlit 快速搭建一个独立的 AI 助手界面，可以对话式管理任务。

### 📚 你需要学会的知识

1. **安装 Streamlit**
   ```bash
   pip install streamlit
   ```

2. **Streamlit 核心概念**
   - `st.text_input`：文本输入框
   - `st.button`：按钮
   - `st.write`：显示内容
   - `st.session_state`：会话状态管理

### 🔨 分步实现

#### 第一步：创建最简界面

```python
# ai_assistant_app.py
import streamlit as st

st.title("待办事项 AI 助手")

user_input = st.text_input("告诉我你想做什么：")
if st.button("生成任务建议"):
    if user_input:
        # 调用你在任务1中写的 AI 服务
        suggestions = suggest_tasks(user_input)
        st.write(suggestions)
    else:
        st.warning("请输入需求描述")
```

#### 第二步：运行

```bash
streamlit run ai_assistant_app.py
```

#### 第三步：增加对话功能

使用 `st.session_state` 保存对话历史，实现多轮对话。

**✅ 完成标准**：打开浏览器能看到界面，输入需求能返回任务建议。

### 🧪 自测问题

- [ ] 你能用 Streamlit 搭建一个简单的 AI 交互界面吗？
- [ ] 你能用 session_state 管理对话状态吗？

如果都是 ✅，恭喜你已掌握 **基础层 5**！

---

## 任务 5：Function Calling — AI 直接操作任务

### 🎯 目标
用户用自然语言说"帮我创建一个明天截止的高优先级任务"，AI 自动调用你的 API 完成操作。

### 📚 你需要学会的知识

1. **Function Calling 是什么**
   - 你预先定义一组"工具"（函数），告诉 AI 有哪些工具可用
   - AI 判断用户意图后，返回要调用的工具名和参数
   - 你的代码执行工具，把结果返回给 AI
   - AI 根据结果生成最终回答

2. **流程图**
   ```
   用户输入 → AI 判断需要调用工具 → 返回工具名+参数
                                        ↓
   最终回答 ← AI 根据结果生成 ← 你的代码执行工具
   ```

### 🔨 分步实现

#### 第一步：定义工具

```python
# tools.py
tools = [
    {
        "name": "create_task",
        "description": "创建一个新的待办任务",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "任务标题"},
                "priority": {"type": "string", "enum": ["high", "medium", "low"]},
                "due_date": {"type": "string", "description": "截止日期 YYYY-MM-DD"}
            },
            "required": ["title"]
        }
    },
    {
        "name": "list_tasks",
        "description": "获取用户的任务列表",
        "parameters": {
            "type": "object",
            "properties": {
                "completed": {"type": "boolean", "description": "是否只看已完成任务"}
            }
        }
    }
]
```

#### 第二步：实现工具执行逻辑

```python
def execute_tool(tool_name: str, parameters: dict) -> dict:
    if tool_name == "create_task":
        # 调用你的 Django API 创建任务
        return tasksApi.create(parameters)
    elif tool_name == "list_tasks":
        return tasksApi.getAll(parameters)
    else:
        return {"error": f"未知工具: {tool_name}"}
```

#### 第三步：实现 Function Calling 循环

```python
def chat_with_tools(user_message: str) -> str:
    # 1. 把用户消息和工具定义发给大模型
    # 2. 如果大模型返回工具调用，执行工具
    # 3. 把工具结果发回大模型
    # 4. 大模型生成最终回答
    pass  # 具体实现取决于你选择的模型平台
```

**✅ 完成标准**：用户说"帮我创建一个任务"，AI 能自动调用 create_task 工具。

### 🧪 自测问题

- [ ] 你理解 Function Calling 的完整流程吗？
- [ ] 你能定义工具并让 AI 正确选择调用吗？
- [ ] 你能处理工具调用的结果并返回给用户吗？

如果三个都是 ✅，恭喜你已掌握 **进阶层 1**！

---

## 任务 6：对话记忆管理

### 🎯 目标
实现短期记忆（当前对话上下文）和长期记忆（跨会话的用户偏好）。

### 📚 你需要学会的知识

1. **记忆分类**
   - **短期记忆**：当前对话的历史消息，每次请求都带上
   - **长期记忆**：用户的偏好、习惯，存储在数据库中

2. **上下文窗口限制**
   - 大模型有 token 上限（如 8K、32K）
   - 需要策略：滑动窗口、摘要压缩、只保留关键信息

### 🔨 分步实现

#### 第一步：实现短期记忆

```python
# 用列表保存对话历史
conversation_history = []

def chat_with_memory(user_message: str) -> str:
    # 把历史消息拼接到请求中
    messages = conversation_history + [
        {"role": "user", "content": user_message}
    ]

    response = call_llm(messages)

    # 保存到历史
    conversation_history.append({"role": "user", "content": user_message})
    conversation_history.append({"role": "assistant", "content": response})

    return response
```

#### 第二步：实现长期记忆

```python
# 在 Django 模型中存储用户偏好
class UserPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    value = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
```

#### 第三步：实现滑动窗口

```python
# 只保留最近 N 轮对话
MAX_HISTORY = 10

if len(conversation_history) > MAX_HISTORY * 2:
    conversation_history = conversation_history[-(MAX_HISTORY * 2):]
```

**✅ 完成标准**：AI 能记住对话上下文，且不会因为历史过长而报错。

### 🧪 自测问题

- [ ] 你能实现多轮对话的上下文保持吗？
- [ ] 你能区分短期记忆和长期记忆吗？
- [ ] 你能处理上下文窗口溢出的情况吗？

如果三个都是 ✅，恭喜你已掌握 **进阶层 2**！

---

## 任务 7：LangChain 流程串联

### 🎯 目标
用 LangChain 串联"用户输入 → 检索相似任务 → AI 生成建议 → 创建任务"的完整流程。

### 📚 你需要学会的知识

1. **安装 LangChain**
   ```bash
   pip install langchain langchain-community
   ```

2. **LangChain 核心概念**
   - **Chain**：把多个步骤串联成一条链
   - **Retriever**：从向量库检索相关文档
   - **Tool**：封装外部工具供 AI 调用
   - **Agent**：让 AI 自主决定调用哪些工具

3. **简单 Chain 示例**
   ```python
   from langchain.chains import LLMChain
   from langchain.prompts import PromptTemplate
   from langchain_community.llms import Tongyi

   llm = Tongyi(model_name="qwen-turbo")

   prompt = PromptTemplate(
       input_variables=["user_input"],
       template="根据用户需求生成任务建议：{user_input}"
   )

   chain = LLMChain(llm=llm, prompt=prompt)
   result = chain.run("帮我安排学习计划")
   ```

### 🔨 分步实现

#### 第一步：用 LangChain 重写任务 1 的 AI 建议

#### 第二步：用 LangChain 的 Retriever 替代手写检索

#### 第三步：用 LangChain 的 Tool 封装任务操作

**✅ 完成标准**：用 LangChain 串联起检索 + 生成 + 工具调用的完整流程。

### 🧪 自测问题

- [ ] 你能用 LangChain 创建一个 Chain 吗？
- [ ] 你能用 LangChain 的 Retriever 检索文档吗？
- [ ] 你能用 LangChain 的 Tool 封装自定义工具吗？

如果三个都是 ✅，恭喜你已掌握 **进阶层 3**！

---

## 任务 8：Agent 核心概念 — 任务规划助手

### 🎯 目标
实现一个能自动规划和分解任务的 Agent，输入大目标，自动创建子任务列表。

### 📚 你需要学会的知识

1. **ReAct 模式**
   ```
   Thought: 我需要先了解用户的目标
   Action: list_tasks
   Observation: 用户已有3个任务
   Thought: 我现在可以分解目标了
   Action: create_task
   Observation: 任务创建成功
   Thought: 我已经完成了任务分解
   Answer: 我已经为你创建了5个子任务
   ```

2. **任务规划**
   - 将大目标拆解为可执行的小步骤
   - 为每个步骤设定优先级和依赖关系

3. **状态管理**
   - Agent 需要记住当前执行到哪一步
   - 需要处理执行失败的情况

### 🔨 分步实现

#### 第一步：用 LangChain 创建 Agent

```python
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool

tools = [
    Tool(name="create_task", func=create_task, description="创建任务"),
    Tool(name="list_tasks", func=list_tasks, description="查看任务列表"),
]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

result = agent.run("帮我规划一个 Python 学习计划，并创建对应的任务")
```

#### 第二步：优化 Agent 的 Prompt

让 Agent 更好地理解任务分解的逻辑。

#### 第三步：添加反思机制

让 Agent 在创建任务后，检查是否合理，是否遗漏。

**✅ 完成标准**：输入一个大目标，Agent 能自动分解并创建任务列表。

### 🧪 自测问题

- [ ] 你理解 ReAct 模式的 Thought-Action-Observation 循环吗？
- [ ] 你能用 LangChain 创建一个能调用工具的 Agent 吗？
- [ ] 你能让 Agent 自动规划和分解任务吗？

如果三个都是 ✅，恭喜你已掌握 **进阶层 4**！

---

## 任务 9：FastAPI 封装 + 部署

### 🎯 目标
将 AI 功能用 FastAPI 封装为独立服务，与 Django 后端分离部署。

### 📚 你需要学会的知识

1. **安装 FastAPI**
   ```bash
   pip install fastapi uvicorn
   ```

2. **FastAPI 基础**
   ```python
   from fastapi import FastAPI

   app = FastAPI()

   @app.post("/ai/suggest")
   async def suggest(input: str):
       return {"suggestions": suggest_tasks(input)}
   ```

3. **运行服务**
   ```bash
   uvicorn main:app --reload --port 8001
   ```

### 🔨 分步实现

#### 第一步：创建独立的 AI 服务项目

```
ai_service/
├── main.py          # FastAPI 入口
├── config.py        # 配置管理
├── routers/
│   ├── suggest.py   # 任务建议路由
│   ├── classify.py  # 任务分类路由
│   └── chat.py      # 对话路由
├── services/
│   ├── llm.py       # 大模型调用封装
│   ├── rag.py       # RAG 服务
│   └── agent.py     # Agent 服务
└── requirements.txt
```

#### 第二步：实现 API Key 管理和限流

```python
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != "your-secret-key":
        raise HTTPException(status_code=403)
    return api_key
```

#### 第三步：Docker 部署

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

**✅ 完成标准**：AI 服务独立运行，Django 通过 HTTP 调用它。

### 🧪 自测问题

- [ ] 你能用 FastAPI 创建一个 REST API 吗？
- [ ] 你能实现 API Key 认证和限流吗？
- [ ] 你能用 Docker 部署 AI 服务吗？

如果三个都是 ✅，恭喜你已掌握 **工程层 1**！

---

## 任务 10：异常/并发/日志/会话隔离

### 🎯 目标
让 AI 服务在生产环境下稳定运行。

### 📚 你需要学会的知识

1. **异常处理**：大模型 API 超时、返回格式错误、额度用尽
2. **并发控制**：多个用户同时请求，避免资源竞争
3. **日志记录**：记录每次 AI 调用的输入输出，方便排查
4. **会话隔离**：不同用户的对话上下文互不干扰

### 🔨 分步实现

#### 第一步：异常处理

```python
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def call_llm_with_retry(prompt: str) -> str:
    try:
        response = Generation.call(model='qwen-turbo', prompt=prompt)
        return response.output.text
    except Exception as e:
        logger.error(f"LLM 调用失败: {e}")
        raise
```

#### 第二步：会话隔离

```python
# 每个用户独立的对话历史
from collections import defaultdict

user_sessions = defaultdict(list)

def get_user_session(user_id: str) -> list:
    return user_sessions[user_id]

def clear_user_session(user_id: str):
    user_sessions.pop(user_id, None)
```

#### 第三步：日志配置

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_service.log'),
        logging.StreamHandler()
    ]
)
```

**✅ 完成标准**：AI 服务有完善的异常处理、日志记录和会话隔离。

### 🧪 自测问题

- [ ] 你能处理大模型 API 调用失败的情况吗？
- [ ] 你能实现不同用户的会话隔离吗？
- [ ] 你能记录完整的 AI 调用日志吗？

如果三个都是 ✅，恭喜你已掌握 **工程层 2**！

---

## 📌 学习节奏建议

不管你在哪个任务，统一按这个节奏执行：

| 比例 | 活动 | 说明 |
|------|------|------|
| 20% | 学理论 | 看概念、文档、知识点 |
| 60% | 写代码 | 优先动手，遇到问题再查资料 |
| 20% | 复盘优化 | 改 bug、优化现有功能 |

> **核心原则**：学一个知识点，就做一个对应小 Demo，只学不写很快就忘。

---

## 🗺️ 学习路径总结

```
任务1(API调用) → 任务2(Prompt) → 任务3(RAG) → 任务4(Streamlit)
                                                        ↓
任务5(Function Calling) → 任务6(记忆) → 任务7(LangChain) → 任务8(Agent)
                                                        ↓
                              任务9(FastAPI) → 任务10(工程化)
```

**建议**：严格按顺序完成，每个任务都是下一个任务的基础。完成一个任务的自测问题全部 ✅ 后，再进入下一个任务。
