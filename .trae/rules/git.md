# Git提交规范

> ⚠️ **重要说明**：所有git操作均需用户手动执行，本规范仅作为参考指南。

## 1. 分支管理规范

### 1.1 分支类型
```
main                # 主分支，稳定可发布
├── develop         # 开发分支
│   ├── feature/*   # 功能分支
│   ├── bugfix/*    # Bug修复分支
│   └── refactor/*  # 重构分支
```

### 1.2 分支命名规范
- **功能分支**：`feature/descriptive-name`
- **Bug修复**：`bugfix/issue-id-description`
- **重构分支**：`refactor/what-is-refactored`
- **发布分支**：`release/v1.0.0`
- **热修复**：`hotfix/urgent-fix-description`

### 1.3 分支工作流
```bash
# 1. 从develop创建功能分支
git checkout develop
git checkout -b feature/task-completion

# 2. 开发并提交
git add .
git commit -m "feat: add task completion status tracking"

# 3. 推送到远程
git push origin feature/task-completion

# 4. 创建Pull Request进行代码审查

# 5. 合并后删除分支
git checkout develop
git branch -d feature/task-completion
```

## 2. 提交信息规范

### 2.1 提交信息格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

### 2.2 Type类型
| 类型 | 描述 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat: add user login` |
| `fix` | 修复bug | `fix: correct task due date` |
| `docs` | 文档更新 | `docs: update API documentation` |
| `style` | 代码格式调整 | `style: format code with black` |
| `refactor` | 重构 | `refactor: simplify task query` |
| `perf` | 性能优化 | `perf: optimize database queries` |
| `test` | 测试相关 | `test: add task CRUD tests` |
| `chore` | 构建/工具变更 | `chore: update dependencies` |
| `db` | 数据库相关 | `db: add task priority field` |

### 2.3 Subject主题
- 使用动词开头（add, fix, update, remove...）
- 不超过50个字符
- 首字母小写
- 结尾不加句号
- 使用现在时

### 2.4 Body正文（可选）
- 详细说明变更的内容和原因
- 每行不超过72个字符
- 说明与之前行为的差异

### 2.5 Footer页脚（可选）
- 关联Issue：`Closes #123` 或 `Fixes #456`
- 破坏性变更：`BREAKING CHANGE: description`

### 2.6 提交示例

#### 新功能
```
feat: add task completion status tracking

- Add completed field to Task model
- Add mark_completed method to Task model
- Update API endpoint for completing tasks
- Add frontend checkbox for task completion

Closes #42
```

#### Bug修复
```
fix: resolve task due date validation error

The due date validation was incorrectly checking against
current time instead of allowing future dates.

Fixes #78
```

#### 数据库变更
```
db: add priority field to tasks

- Add priority column with HIGH/MEDIUM/LOW options
- Create database migration
- Update Prisma schema

Closes #15
```

#### 文档
```
docs: update README with setup instructions

Add detailed setup guide for both frontend and backend.
Include database setup and environment configuration.
```

#### 重构
```
refactor: simplify task query logic

Extract task filtering logic into separate function
for better reusability and testability.

No functional changes.
```

## 3. 提交频率规范

### 3.1 原子提交
- 每个提交只做一件事
- 保持提交粒度小而集中
- 便于代码审查和回滚

### 3.2 提交时机
- 完成一个独立的功能点
- 修复一个bug
- 重构完成一部分
- 重要的中间里程碑

## 4. 代码审查规范

### 4.1 PR标题格式
```
<type>: <description>
```
示例：`feat: add user authentication`

### 4.2 PR描述模板
```markdown
## Description
Brief description of the changes.

## Changes Made
- Change 1
- Change 2
- Change 3

## How to Test
1. Step 1
2. Step 2

## Related Issues
Closes #123, Fixes #456

## Screenshots (if applicable)
```

### 4.3 审查要点
- 代码符合项目规范
- 有适当的测试覆盖
- 没有安全问题
- 性能影响评估
- 文档是否更新

## 5. 提交历史规范

### 5.1 保持历史整洁
- 使用 `rebase` 代替 `merge` 更新分支
- 合并且清理提交历史（squash/fixup）
- 避免 "WIP"、"Fix typo" 等无意义提交

### 5.2 Rebase流程
```bash
# 更新本地develop
git checkout develop
git pull origin develop

# 切换到功能分支
git checkout feature/task-completion

# Rebase
git rebase develop

# 解决冲突后继续
git add .
git rebase --continue

# 强制推送（谨慎使用）
git push origin feature/task-completion --force-with-lease
```

## 6. 忽略文件规范

### 6.1 .gitignore
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Prisma
prisma/migrations/dev.db

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
```

## 7. 发布规范

### 7.1 版本号
遵循语义化版本（Semantic Versioning）：
- `MAJOR`：不兼容的API修改
- `MINOR`：向下兼容的功能性新增
- `PATCH`：向下兼容的问题修正

### 7.2 发布流程
```bash
# 1. 更新版本号
# 2. 更新CHANGELOG
# 3. 创建发布提交
git add package.json CHANGELOG.md
git commit -m "chore: release v1.0.0"

# 4. 创建标签
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# 5. 部署到生产环境
```

## 8. CHANGELOG维护规范

### 8.1 CHANGELOG格式
```markdown
# Changelog

## [1.0.0] - 2024-01-15

### Added
- User authentication system
- Task CRUD operations
- Category and tag management

### Fixed
- Task due date validation
- Mobile responsive layout

### Changed
- Improved task list performance
```

## 9. 紧急修复规范

### 9.1 Hotfix流程
```bash
# 1. 从main创建hotfix分支
git checkout main
git checkout -b hotfix/urgent-fix

# 2. 修复并提交
git commit -m "fix: urgent fix for task deletion"

# 3. 直接合并到main
git checkout main
git merge --no-ff hotfix/urgent-fix

# 4. 创建patch版本
git tag -a v1.0.1 -m "Release version 1.0.1"

# 5. 同步到develop
git checkout develop
git merge main

# 6. 部署修复
```
