# 工作流程管理

本目录包含Agent工作流程管理的所有规范和检查清单。

## 📁 目录结构

```
.trae/workflow/
├── README.md                      # 本文件 - 工作流程总览
├── permission-policy.md           # 权限策略
├── restart-protocol.md            # 重启协议
├── verify-checklist.md            # 验证检查清单
└── progress/
    └── current-task.md            # 当前任务追踪
```

## 📋 核心文档

| 文档 | 用途 |
|------|------|
| [permission-policy.md](./permission-policy.md) | 定义Agent权限边界、操作分类、决策流程 |
| [restart-protocol.md](./restart-protocol.md) | 重启时的检查流程、状态恢复、常见问题 |
| [verify-checklist.md](./verify-checklist.md) | 开发各阶段的验证检查清单 |
| [progress/current-task.md](./progress/current-task.md) | 当前任务进度追踪 |

## 🔄 工作流程

### 标准开发流程

```
1. 任务开始
   ↓
2. 修改前检查（verify-checklist）
   ↓
3. 开发实现
   ↓
4. 修改中检查（verify-checklist）
   ↓
5. 修改后检查（verify-checklist）
   ↓
6. 代码审查（TRAE-code-review）
   ↓
7. 用户确认 & 手动git提交
   ↓
8. 任务完成
   ↓
9. 下一个任务
```

### 重启流程

```
1. 读取必读文件（restart-protocol）
   ↓
2. 环境验证
   ↓
3. 检查当前任务（current-task.md）
   ↓
4. 与用户确认
   ↓
5. 继续或开始新任务
```

## ⚡ 快速参考

### 权限快速判断

```
🟢 自主执行 → 读取、检查、搜索
🟡 需要批准 → 创建、修改配置、删除
🔴 必须停止 → git操作、敏感操作
```

### 检查清单快速跳转

- [修改前检查](./verify-checklist.md#1-修改前检查)
- [修改中检查](./verify-checklist.md#2-修改中检查)
- [修改后检查](./verify-checklist.md#3-修改后检查)
- [提交前检查](./verify-checklist.md#4-提交前检查)

## 📝 任务管理

### 更新当前任务

每次开始或更新任务时，编辑：
```
.trae/workflow/progress/current-task.md
```

记录内容：
- 任务描述和时间
- 已完成/进行中/待处理事项
- 阻塞和问题
- 相关文件

### 完成任务后

任务完成后：
1. 更新 current-task.md 标记所有为完成
2. （可选）归档到历史记录
3. 准备开始下一个任务

## 🔐 关键原则

### 1. 单次单功能
- 一次只做一件事
- 完成后检查再继续
- 避免范围蔓延

### 2. Git操作完全手动
- Agent不执行任何git命令
- 所有git操作由用户手动执行
- 规范仅作参考

### 3. 安全第一
- 不确定时询问用户
- 提供明确选项
- 不猜测用户意图

### 4. 遵循规范
- 严格按照项目规范
- 使用检查清单
- 调用代码审查

## 🆘 需要帮助？

- 权限问题 → [permission-policy.md](./permission-policy.md)
- 重启问题 → [restart-protocol.md](./restart-protocol.md)
- 检查清单 → [verify-checklist.md](./verify-checklist.md)
- 规范参考 → [../rules/](../rules/)
- Agent行为 → [../agent/](../agent/)

---

**最后更新**：2024-01-15
