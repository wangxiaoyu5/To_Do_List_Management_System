# 代码规范

本目录包含待办事项管理系统的所有代码规范。

## 📋 规范列表

| 规范文件 | 描述 |
|---------|------|
| [frontend.md](./frontend.md) | 前端开发规范（React, TypeScript, Ant Design） |
| [backend.md](./backend.md) | 后端开发规范（Python, Django, DRF） |
| [database.md](./database.md) | 数据库和Prisma规范 |
| [git.md](./git.md) | Git提交和分支管理规范 |

## 🤖 Agent规范

同时，请查看 [Agent规范](../agent/) 了解Agent在本项目中的行为准则和权限边界。

## 🎯 技术栈

### 前端
- **框架**：React 18+
- **UI组件**：Ant Design 5.x
- **状态管理**：Redux Toolkit + RTK Query
- **路由**：React Router 6
- **构建工具**：Vite
- **语言**：TypeScript

### 后端
- **框架**：Django 4.x + Django REST Framework
- **数据库**：PostgreSQL
- **ORM**：Prisma
- **认证**：JWT
- **语言**：Python

## 📁 项目结构

```
待办事项管理系统/
├── .trae/
│   └── rules/              # 代码规范
│       ├── frontend.md
│       ├── backend.md
│       ├── database.md
│       ├── git.md
│       └── README.md
├── frontend/               # 前端项目
├── backend/                # 后端项目
├── docs/                   # 项目文档
├── 需求文档.md
├── 开发进度计划.md
└── README.md
```

## 🚀 快速开始

### 开发前必读
1. 阅读 [frontend.md](./frontend.md) - 前端规范
2. 阅读 [backend.md](./backend.md) - 后端规范
3. 阅读 [database.md](./database.md) - 数据库规范
4. 阅读 [git.md](./git.md) - Git工作流

### 提交代码前检查
- [ ] 代码符合对应规范
- [ ] 有适当的测试覆盖
- [ ] 提交信息符合规范
- [ ] 文档已更新

## 📚 相关文档

- [需求文档](../../需求文档.md)
- [开发进度计划](../../开发进度计划.md)

---

**最后更新**：2024-01-15
