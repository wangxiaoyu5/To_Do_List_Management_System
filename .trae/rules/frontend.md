# 前端代码规范

## 1. 项目结构规范

```
frontend/
├── src/
│   ├── components/          # 通用组件（PascalCase命名）
│   │   ├── TaskForm/
│   │   │   ├── index.tsx
│   │   │   ├── TaskForm.tsx
│   │   │   └── TaskForm.module.css
│   │   └── ...
│   ├── pages/               # 页面组件
│   │   ├── Auth/
│   │   ├── TaskList/
│   │   └── ...
│   ├── store/               # Redux状态管理
│   │   ├── index.ts
│   │   └── api/
│   ├── services/            # API服务
│   ├── types/               # TypeScript类型定义
│   ├── utils/               # 工具函数
│   ├── hooks/               # 自定义Hooks
│   ├── constants/           # 常量定义
│   ├── assets/              # 静态资源
│   ├── App.tsx
│   └── main.tsx
```

## 2. 命名规范

### 2.1 文件和文件夹
- **组件文件夹**：PascalCase（如 `TaskForm`）
- **组件文件**：PascalCase（如 `TaskForm.tsx`）
- **工具函数文件**：camelCase（如 `dateUtils.ts`）
- **类型文件**：PascalCase（如 `types.ts`）
- **样式文件**：与组件同名（如 `TaskForm.module.css`）

### 2.2 变量和函数
- **变量**：camelCase（如 `taskList`）
- **常量**：UPPER_SNAKE_CASE（如 `MAX_TASKS`）
- **函数**：camelCase（如 `handleSubmit`）
- **组件**：PascalCase（如 `TaskForm`）
- **自定义Hook**：use前缀 + camelCase（如 `useTasks`）

### 2.3 CSS类名
- 使用CSS Modules
- 类名：camelCase或kebab-case（如 `taskItem` 或 `task-item`）

## 3. React组件规范

### 3.1 组件结构
```tsx
import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Button, Form } from 'antd';

import { useAppSelector, useAppDispatch } from '@/store/hooks';
import { fetchTasks } from '@/store/api/taskApi';
import { Task } from '@/types/task';
import styles from './TaskForm.module.css';

interface TaskFormProps {
  onSubmit: (data: Partial<Task>) => void;
  initialData?: Partial<Task>;
}

export const TaskForm: React.FC<TaskFormProps> = ({ 
  onSubmit, 
  initialData 
}) => {
  const [form] = Form.useForm();
  const dispatch = useAppDispatch();

  const handleSubmit = (values: any) => {
    onSubmit(values);
  };

  return (
    <div className={styles.formContainer}>
      <Form form={form} onFinish={handleSubmit}>
        {/* 表单内容 */}
      </Form>
    </div>
  );
};

export default TaskForm;
```

### 3.2 Props接口
- 使用 `TypeScript interface` 定义Props
- 接口名：`组件名Props`
- 必填属性在前，可选属性在后

### 3.3 State管理
- 本地状态使用 `useState`
- 全局状态使用 Redux Toolkit
- 服务端状态使用 RTK Query

## 4. TypeScript规范

### 4.1 类型定义
```typescript
// types/task.ts
export interface Task {
  id: string;
  title: string;
  description?: string;
  priority: 'high' | 'medium' | 'low';
  completed: boolean;
  dueDate: Date | null;
  createdAt: Date;
  updatedAt: Date;
}

export type TaskFormData = Partial<Task>;

export interface TaskListParams {
  page?: number;
  pageSize?: number;
  priority?: string;
  categoryId?: string;
}
```

### 4.2 类型使用
- 尽量避免使用 `any`
- 使用 `unknown` 代替 `any`
- 使用泛型提高复用性

## 5. 样式规范

### 5.1 CSS Modules
```css
/* TaskForm.module.css */
.formContainer {
  max-width: 600px;
  margin: 0 auto;
  padding: 24px;
}

.taskItem {
  display: flex;
  gap: 12px;
  padding: 16px;
  border-radius: 8px;
}

.taskItem--completed {
  opacity: 0.6;
  text-decoration: line-through;
}
```

### 5.2 Ant Design使用
- 使用Ant Design组件库
- 主题定制在 `theme` 配置中
- 统一使用Ant Design的栅格系统

## 6. Git提交规范

见 `git.md`

## 7. 性能优化规范

- 使用 `React.memo` 优化组件渲染
- 使用 `useMemo` 和 `useCallback` 缓存值和函数
- 列表使用唯一的 `key`
- 懒加载路由和组件
- 避免在渲染中创建函数

## 8. 开发流程规范

### 8.1 单功能开发原则
每次只开发一个功能，完成一个功能后再开发下一个功能。

#### 开发流程
1. 选择一个功能（例如：任务列表页面）
2. 编写该功能的完整实现
3. 调用相关skill检查代码（如 `frontend-development`、`TRAE-code-review`）
4. 确认无错误后，提交该功能
5. 再继续下一个功能

#### 错误示例
```tsx
// ❌ 错误：同时开发多个功能
// components/TaskItem.tsx
export const TaskItem: React.FC<{ task: Task }> = ({ task }) => {
  // 同时实现：显示任务、标记完成、删除任务、编辑任务
  const handleComplete = () => { /* 标记完成 */ }
  const handleDelete = () => { /* 删除任务 */ }
  const handleEdit = () => { /* 编辑任务 */ }
  
  return (
    <div>
      <input type="checkbox" onChange={handleComplete} checked={task.completed} />
      <span>{task.title}</span>
      <button onClick={handleDelete}>删除</button>
      <button onClick={handleEdit}>编辑</button>
    </div>
  );
};
```

#### 正确示例
```tsx
// ✅ 正确：一个功能一个功能开发
// components/TaskItem.tsx
export const TaskItem: React.FC<{ task: Task; onComplete: (id: string) => void }> = ({ task, onComplete }) => {
  // 第一步：先实现基本显示和标记完成
  return (
    <div>
      <input 
        type="checkbox" 
        onChange={() => onComplete(task.id)} 
        checked={task.completed} 
      />
      <span>{task.title}</span>
    </div>
  );
};
```

### 8.2 单路由单功能原则
每个页面/路由只负责一个主要功能，不要在一个页面中实现多个功能。

#### 错误示例
```tsx
// ❌ 错误：一个页面做太多事情
// pages/TaskList.tsx
export const TaskList: React.FC = () => {
  // 同一个页面同时包含：任务列表、任务创建、分类管理、标签管理
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [showCategoryManager, setShowCategoryManager] = useState(false);
  const [showTagManager, setShowTagManager] = useState(false);

  return (
    <div>
      {/* 任务列表 */}
      <TaskListContainer />
      {/* 创建任务表单 */}
      {showCreateForm && <TaskCreateForm />}
      {/* 分类管理 */}
      {showCategoryManager && <CategoryManager />}
      {/* 标签管理 */}
      {showTagManager && <TagManager />}
    </div>
  );
};

// 对应路由：/tasks
```

#### 正确示例
```tsx
// ✅ 正确：每个路由一个功能
// pages/TaskList.tsx
export const TaskList: React.FC = () => {
  // 单个功能：只显示任务列表
  return <TaskListContainer />;
};

// pages/TaskCreate.tsx
export const TaskCreate: React.FC = () => {
  // 单个功能：创建任务
  return <TaskForm onSubmit={createTask} />;
};

// pages/CategoryManager.tsx
export const CategoryManager: React.FC = () => {
  // 单个功能：分类管理
  return <CategoryList />;
};
```

#### 正确的路由配置示例
```tsx
// App.tsx
<Routes>
  <Route path="/tasks" element={<TaskList />} />              {/* 任务列表 */}
  <Route path="/tasks/create" element={<TaskCreate />} />       {/* 创建任务 */}
  <Route path="/categories" element={<CategoryManager />} />    {/* 分类管理 */}
  <Route path="/tags" element={<TagManager />} />               {/* 标签管理 */}
</Routes>
```

### 8.3 功能验证流程
1. 完成功能编写
2. 运行相关检查（如 `npm run type-check`、`npm run lint`）
3. 调用skill进行代码审查
4. 确认无错误后，**用户手动执行git提交**
5. 再开始下一个功能

## 9. 测试规范

- 单元测试使用 `Vitest`
- 组件测试使用 `React Testing Library`
- 测试文件命名：`组件名.test.tsx`
- 测试覆盖率目标：60%+
