# 🚀 最简单的 RAG 示例！

## 📦 这里有什么文件？

```
rag-simple/
├── requirements.txt    # 需要安装的 Python 库
├── my-knowledge.txt   # 你的知识库（历史任务记录）
├── simple-rag.py      # 最简单的 RAG 代码
├── .env              # 配置文件（放 API Key）
└── README.md         # 就是这个文件啦！
```

## 🏃 怎么运行？

### 第一步：安装依赖

打开终端，进入这个文件夹，运行：

```bash
cd rag-simple
pip install -r requirements.txt
```

### 第二步：配置 API Key

打开 `.env` 文件，把你的 OpenAI API Key 填进去：

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

### 第三步：运行！

```bash
python simple-rag.py
```

然后就可以问问题了！

## ❓ 可以问什么问题？

试试这些：
- "我做数据库设计花了多长时间？"
- "写文档有什么经验教训？"
- "学习React用了多久？"

## 🤔 这个代码在做什么？

1. **加载知识库**：读取 `my-knowledge.txt`
2. **检索相关内容**：用简单的关键词找相关任务
3. **生成回答**：把找到的内容 + 问题发给 LLM，让它回答

这就是 RAG 的核心思想！先找资料，再回答！
