# 数据库和Prisma规范

## 1. Prisma Schema规范

### 1.1 基本结构
```prisma
generator client {
  provider = "prisma-client-py"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// 模型定义...
```

### 1.2 命名规范
- **模型名**：PascalCase，单数形式（如 `Task`）
- **字段名**：camelCase（如 `dueDate`）
- **枚举名**：PascalCase（如 `Priority`）
- **枚举值**：UPPER_SNAKE_CASE（如 `HIGH`）

### 1.3 完整示例
```prisma
generator client {
  provider = "prisma-client-py"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// ============================================
// 用户模型
// ============================================
model User {
  id       String  @id @default(uuid())
  username String  @unique
  email    String  @unique
  passwordHash String
  tasks    Task[]
  categories Category[]
  tags     Tag[]
  
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")

  @@map("users")
}

// ============================================
// 任务模型
// ============================================
enum Priority {
  HIGH
  MEDIUM
  LOW
}

model Task {
  id          String   @id @default(uuid())
  title       String
  description String   @default("")
  priority    Priority @default(MEDIUM)
  dueDate     DateTime?
  completed   Boolean  @default(false)
  completedAt DateTime?
  
  userId     String
  user       User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  
  categoryId String?
  category   Category? @relation(fields: [categoryId], references: [id], onDelete: SetNull)
  
  tags       Tag[]    @relation("TaskTags")
  
  createdAt   DateTime @default(now()) @map("created_at")
  updatedAt   DateTime @updatedAt @map("updated_at")

  @@index([userId])
  @@index([priority])
  @@index([completed])
  @@index([dueDate])
  @@map("tasks")
}

// ============================================
// 分类模型
// ============================================
model Category {
  id     String @id @default(uuid())
  name   String
  color  String @default("#1890ff")
  
  userId String
  user   User   @relation(fields: [userId], references: [id], onDelete: Cascade)
  
  tasks  Task[]
  
  createdAt DateTime @default(now()) @map("created_at")

  @@index([userId])
  @@map("categories")
}

// ============================================
// 标签模型
// ============================================
model Tag {
  id     String @id @default(uuid())
  name   String
  color  String @default("#52c41a")
  
  userId String
  user   User   @relation(fields: [userId], references: [id], onDelete: Cascade)
  
  tasks  Task[] @relation("TaskTags")
  
  createdAt DateTime @default(now()) @map("created_at")

  @@index([userId])
  @@map("tags")
}
```

## 2. 模型设计规范

### 2.1 时间戳字段
每个模型都应包含时间戳：
```prisma
createdAt DateTime @default(now()) @map("created_at")
updatedAt DateTime @updatedAt @map("updated_at")
```

### 2.2 关系定义
- 使用 `onDelete: Cascade` 删除级联（用户删除时删除其所有数据）
- 使用 `onDelete: SetNull` 可选关系（分类删除时任务分类设为null）
- 关系字段命名：`modelId` + `model`

### 2.3 索引策略
- 外键字段自动索引
- 经常查询的字段添加索引
- 复合索引用于多字段查询

```prisma
@@index([userId])
@@index([priority])
@@index([completed])
```

### 2.4 数据库映射
- 使用 `@map` 映射到蛇形命名的数据库列
- 使用 `@@map` 映射到复数表名
- 数据库表名使用snake_case

## 3. 迁移规范

### 3.1 迁移流程
```bash
# 1. 修改schema.prisma
# 2. 创建迁移
prisma migrate dev --name descriptive_migration_name

# 3. 应用迁移
prisma migrate deploy

# 4. 生成客户端
prisma generate
```

### 3.2 迁移命名规范
使用描述性名称：
- `add_user_model`
- `add_task_priority_field`
- `create_task_tags_relation`
- `add_completed_at_to_tasks`

### 3.3 迁移最佳实践
- 每个迁移只做一件事
- 破坏性迁移需要额外评审
- 先在开发环境测试迁移
- 保留所有迁移历史

## 4. Prisma Client使用规范

### 4.1 查询规范
```python
from prisma import Prisma
from typing import List, Optional

prisma = Prisma()

async def get_user_tasks(
    user_id: str,
    priority: Optional[str] = None,
    completed: Optional[bool] = None
) -> List[Task]:
    where = {"userId": user_id}
    
    if priority:
        where["priority"] = priority
    
    if completed is not None:
        where["completed"] = completed
    
    tasks = await prisma.task.find_many(
        where=where,
        include={"category": True, "tags": True},
        order=[{"createdAt": "desc"}]
    )
    return tasks

async def create_task(
    user_id: str,
    title: str,
    description: str = "",
    priority: str = "MEDIUM"
) -> Task:
    task = await prisma.task.create(
        data={
            "title": title,
            "description": description,
            "priority": priority,
            "userId": user_id
        }
    )
    return task
```

### 4.2 事务使用
```python
async def batch_update_tasks(
    task_updates: List[dict]
):
    async with prisma.tx() as tx:
        for update in task_updates:
            await tx.task.update(
                where={"id": update["id"]},
                data=update["data"]
            )
```

### 4.3 连接管理
```python
# 应用启动时连接
async def startup():
    await prisma.connect()

# 应用关闭时断开
async def shutdown():
    await prisma.disconnect()
```

## 5. 数据库安全规范

### 5.1 敏感数据
- 密码使用哈希存储（bcrypt）
- 不直接存储敏感信息
- 使用环境变量管理数据库连接

### 5.2 访问控制
- 应用用户只能访问自己的数据
- 使用数据库级别的行级安全（可选）
- 定期备份数据库

## 6. 性能优化规范

### 6.1 查询优化
- 使用 `include` 减少N+1查询
- 使用 `select` 只获取需要的字段
- 合理使用索引
- 大数据量使用分页

### 6.2 连接池
- 配置合理的连接池大小
- 复用数据库连接
- 及时释放不再使用的连接

## 7. 测试数据规范

### 7.1 Seed脚本
```python
# scripts/seed_data.py
import asyncio
from prisma import Prisma
from prisma.models import User, Task

async def seed():
    prisma = Prisma()
    await prisma.connect()
    
    # 创建测试用户
    user = await prisma.user.create(
        data={
            "username": "testuser",
            "email": "test@example.com",
            "passwordHash": "hashed_password_here"
        }
    )
    
    # 创建测试任务
    for i in range(10):
        await prisma.task.create(
            data={
                "title": f"Test Task {i + 1}",
                "description": f"Description for task {i + 1}",
                "priority": "MEDIUM" if i % 2 == 0 else "HIGH",
                "userId": user.id
            }
        )
    
    await prisma.disconnect()

if __name__ == "__main__":
    asyncio.run(seed())
```

## 8. Git提交规范

见 `git.md`
