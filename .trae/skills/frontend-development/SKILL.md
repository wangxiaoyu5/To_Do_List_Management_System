---
name: "frontend-development"
description: "提供标准化前端开发规范和流程指导。Invoke when starting new frontend features, implementing React components, or following the standardized development workflow."
---

# 前端开发规范与流程

## 技术栈标准

### 1.1 核心依赖
```json
{
  "dependencies": {
    "react": "^18.2.x",
    "react-dom": "^18.2.x",
    "axios": "^1.6.x",
    "lucide-react": "^0.x.x"
  },
  "devDependencies": {
    "typescript": "^5.3.x",
    "vite": "^5.x.x",
    "@types/react": "^18.2.x",
    "@types/react-dom": "^18.2.x"
  }
}
```

### 1.2 TypeScript 配置
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

---

## 项目结构标准

### 2.1 强制目录结构
```
client/
├── src/
│   ├── components/              # 组件目录
│   │   ├── [ComponentName]/
│   │   │   ├── index.tsx        # 组件主体
│   │   │   ├── [ComponentName].css    # 组件样式
│   │   │   └── types.ts         # 组件类型（可选）
│   │   └── ...
│   ├── pages/                   # 页面组件
│   │   └── [PageName]/
│   ├── hooks/                   # 自定义Hooks
│   │   └── use[HookName].ts
│   ├── services/                # API服务层
│   │   └── [service].ts
│   ├── types/                   # 全局类型定义
│   │   └── index.ts
│   ├── utils/                   # 工具函数
│   │   └── [util].ts
│   ├── styles/                  # 全局样式
│   │   ├── variables.css        # CSS变量
│   │   └── mixins.css           # 混入样式
│   ├── App.tsx                  # 应用入口
│   ├── App.css                  # 应用样式
│   ├── main.tsx                 # 渲染入口
│   └── index.css                # 全局基础样式
├── public/                      # 静态资源
├── index.html
├── vite.config.ts
├── tsconfig.json
└── package.json
```

### 2.2 文件命名规范
| 类型 | 命名规则 | 示例 |
|------|----------|------|
| 组件文件 | PascalCase.tsx | `AnalysisForm.tsx` |
| 样式文件 | PascalCase.css | `AnalysisForm.css` |
| 工具函数 | camelCase.ts | `formatDate.ts` |
| 自定义Hook | use + PascalCase.ts | `useAnalysis.ts` |
| 类型定义 | camelCase.ts 或 types/index.ts | `analysis.ts` |
| 服务层 | camelCase.ts | `api.ts` |

---

## 代码规范

### 3.1 导入顺序（必须严格遵守）
```typescript
// 1. React相关
import { useState, useEffect, useCallback } from 'react';

// 2. 第三方库
import axios from 'axios';
import { Upload, File } from 'lucide-react';

// 3. 内部类型
import { ProposalAnalysis, AnalysisResponse } from '../types';

// 4. 内部服务/工具
import { analysisApi } from '../services/api';
import { formatDate } from '../utils/date';

// 5. 内部组件
import Sidebar from './Sidebar';
import FileUpload from './FileUpload';

// 6. 样式文件（最后）
import './App.css';
```

### 3.2 组件开发规范

#### 函数组件定义
```typescript
// ✅ 正确：使用默认导出，明确Props类型
interface FileUploadProps {
  onFileSelect: (file: File | null) => void;
  selectedFile: File | null;
}

export default function FileUpload({ onFileSelect, selectedFile }: FileUploadProps) {
  // 组件逻辑
}

// ❌ 避免：使用any或不定义Props类型
export default function FileUpload(props: any) {
  // ...
}
```

#### 状态管理
```typescript
// ✅ 正确：使用明确的类型，多个相关状态合并
const [selectedFile, setSelectedFile] = useState<File | null>(null);
const [fileContent, setFileContent] = useState<string>('');
const [isLoading, setIsLoading] = useState(false);

// ✅ 正确：复杂状态使用useReducer
interface AnalysisState {
  data: ProposalAnalysis | null;
  isLoading: boolean;
  error: string | null;
}

const [state, dispatch] = useReducer(analysisReducer, initialState);
```

#### 事件处理
```typescript
// ✅ 正确：使用useCallback缓存事件处理函数
const handleFileChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
  const files = e.target.files;
  if (files && files.length > 0) {
    onFileSelect(files[0]);
  }
}, [onFileSelect]);

// ✅ 正确：拖拽事件类型
const handleDrop = useCallback((e: React.DragEvent) => {
  e.preventDefault();
  const files = e.dataTransfer.files;
  if (files.length > 0) {
    onFileSelect(files[0]);
  }
}, [onFileSelect]);
```

### 3.3 类型定义规范

#### 接口命名
```typescript
// types/index.ts

// 基础类型使用具体业务名 + 后缀
export interface ProposalAnalysis {
  worldView: WorldViewSection;
  character: CharacterSection;
  scores?: AnalysisScores;
}

// 请求/响应类型
export interface AnalysisRequest {
  fileContent: string;
  fileName: string;
}

export interface AnalysisResponse {
  success: boolean;
  data?: ProposalAnalysis;
  error?: string;
}

// 联合类型使用type
export type FeasibilityLevel = 'excellent' | 'good' | 'average' | 'poor';

// 常量配置使用as const
export const SCORE_WEIGHTS = {
  worldView: 0.20,
  character: 0.25,
  highlights: 0.25,
  rules: 0.20,
  showHighlights: 0.10
} as const;
```

### 3.4 API服务层规范
```typescript
// services/api.ts
import axios from 'axios';
import { AnalysisResponse, SaveResponse, ProposalAnalysis } from '../types';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json'
  }
});

export const analysisApi = {
  // 文件解析
  parseFile: async (file: File): Promise<{ success: boolean; content?: string; error?: string }> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/analysis/parse', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return response.data;
  },

  // 文件分析
  analyzeFile: async (file: File): Promise<AnalysisResponse> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/analysis/analyze', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return response.data;
  },

  // 重新评估
  reEvaluate: async (analysis: ProposalAnalysis): Promise<ReEvaluateResponse> => {
    const response = await api.post('/analysis/reevaluate', analysis);
    return response.data;
  },

  // 保存分析
  saveAnalysis: async (analysis: ProposalAnalysis, fileName: string): Promise<SaveResponse> => {
    const response = await api.post('/analysis/save', { analysis, fileName });
    return response.data;
  }
};
```

### 3.5 错误处理规范
```typescript
// ✅ 正确：统一错误处理
const handleAnalyze = async () => {
  if (!selectedFile) return;

  setIsAnalyzing(true);
  setError(null);

  try {
    const response = await analysisApi.analyzeFile(selectedFile);
    
    if (response.success && response.data) {
      setAnalysis(response.data);
    } else {
      setError(response.error || '分析失败，请重试');
    }
  } catch (err) {
    setError(err instanceof Error ? err.message : '分析过程中发生错误');
  } finally {
    setIsAnalyzing(false);
  }
};

// ✅ 正确：组件内错误展示
{error && (
  <div className="error-message">
    <AlertCircle size={16} />
    <span>{error}</span>
  </div>
)}
```

---

## CSS样式规范

### 4.1 CSS文件组织
```css
/* ComponentName.css */

/* 1. 组件根元素 */
.component-name {
  /* 基础样式 */
}

/* 2. 头部区域 */
.component-header {
  /* ... */
}

.component-header-title {
  /* ... */
}

/* 3. 内容区域 */
.component-content {
  /* ... */
}

/* 4. 状态样式 */
.component-name.loading {
  /* ... */
}

.component-name.error {
  /* ... */
}

/* 5. 响应式 */
@media (max-width: 768px) {
  .component-name {
    /* ... */
  }
}

/* 6. 动画 */
@keyframes animationName {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

### 4.2 命名规范（BEM风格）
```css
/* Block */
.analysis-form { }

/* Element */
.analysis-form__header { }
.analysis-form__content { }
.analysis-form__footer { }

/* Modifier */
.analysis-form--loading { }
.analysis-form--collapsed { }

/* 或使用连字符风格 */
.analysis-form { }
.analysis-form-header { }
.analysis-form-content { }
```

### 4.3 颜色变量（推荐）
```css
/* styles/variables.css */
:root {
  /* 主色调 */
  --primary-color: #667eea;
  --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  
  /* 背景色 */
  --bg-primary: #ffffff;
  --bg-secondary: #f5f7fa;
  --bg-tertiary: #fafbfc;
  
  /* 文字色 */
  --text-primary: #1a1a2e;
  --text-secondary: #6b7280;
  --text-tertiary: #9ca3af;
  
  /* 边框 */
  --border-color: rgba(0, 0, 0, 0.06);
  
  /* 阴影 */
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.06);
  --shadow-md: 0 4px 24px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  
  /* 圆角 */
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 20px;
  
  /* 间距 */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
}
```

### 4.4 动画规范
```css
/* 过渡动画 */
.transition-base {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 旋转动画 */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.spin {
  animation: spin 1s linear infinite;
}

/* 淡入 */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.fade-in {
  animation: fadeIn 0.3s ease-out;
}
```

---

## 组件设计原则

### 5.1 单一职责
```typescript
// ✅ 正确：每个组件只做一件事
// FileUpload.tsx - 只处理文件上传
// FilePreview.tsx - 只显示文件内容
// AnalysisForm.tsx - 只处理分析表单

// ❌ 避免：一个组件做太多事情
function AnalysisPage() {
  // 处理文件上传
  // 处理文件预览
  // 处理AI分析
  // 处理表单编辑
  // 处理保存
  // ... 太臃肿
}
```

### 5.2 Props设计
```typescript
// ✅ 正确：Props接口清晰，有默认值
interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  onClick?: () => void;
}

export default function Button({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  onClick
}: ButtonProps) {
  // ...
}
```

### 5.3 状态提升
```typescript
// ✅ 正确：共享状态提升到父组件
// App.tsx
function App() {
  const [analysis, setAnalysis] = useState<ProposalAnalysis>(defaultAnalysis);
  
  return (
    <>
      <Sidebar />
      <FileUpload onFileSelect={handleFileSelect} />
      <AnalysisForm 
        analysis={analysis} 
        onChange={setAnalysis}
        onReEvaluate={handleReEvaluate}
      />
    </>
  );
}
```

---

## 开发流程

### 阶段1: 需求分析
**目标**: 理解UI/UX需求，确定组件拆分

**执行步骤**:
1. 查看设计稿或需求文档
2. 识别可复用组件
3. 确定状态管理方案
4. 规划API接口调用

**输出物**:
- 组件清单
- 状态设计图
- API调用规划

---

### 阶段2: 类型定义
**目标**: 先定义类型，再写实现

**执行步骤**:
1. 定义数据模型类型
2. 定义API请求/响应类型
3. 定义组件Props类型
4. 定义状态类型

**示例**:
```typescript
// types/index.ts
export interface ProposalAnalysis {
  worldView: WorldViewSection;
  character: CharacterSection;
  // ...
}

export interface AnalysisResponse {
  success: boolean;
  data?: ProposalAnalysis;
  error?: string;
}
```

---

### 阶段3: API服务层
**目标**: 封装所有后端交互

**执行步骤**:
1. 配置axios实例
2. 定义API函数
3. 统一错误处理
4. 添加类型标注

---

### 阶段4: 组件实现
**目标**: 按优先级实现组件

**实现顺序**:
1. 基础UI组件（Button, Input, Card等）
2. 业务组件（FileUpload, FilePreview）
3. 复杂组件（AnalysisForm）
4. 页面组件（App）

**每个组件开发步骤**:
1. 定义Props接口
2. 实现组件逻辑
3. 编写组件样式
4. 添加加载/错误状态

---

### 阶段5: 状态集成
**目标**: 连接组件，实现数据流

**执行步骤**:
1. 在父组件定义共享状态
2. 通过Props传递数据和回调
3. 实现事件处理函数
4. 添加错误边界

---

### 阶段6: 样式优化

**目标**: 完善视觉效果

**执行步骤**:
1. 实现基础布局
2. 添加过渡动画
3. 优化响应式
4. 完善空状态/加载状态

---

### 阶段7: 代码质量检查

**目标**: 确保代码符合规范

**必须运行代码质量检查：**

```bash
# 运行代码质量检查（必须）
npm run check

# 如果检查未通过，必须修复错误后才能继续
```

**检查项目：**
- [ ] TypeScript 类型检查通过
- [ ] ESLint 规范检查通过
- [ ] 无硬编码 CSS 颜色（必须使用 Design Tokens）
- [ ] 无硬编码 CSS 间距（必须使用 spacing system）
- [ ] 无硬编码中文文本（必须使用 i18n）
- [ ] 无 console.log/debug
- [ ] 导入顺序符合规范
- [ ] 无 any 类型使用
- [ ] 文件命名符合 PascalCase 规范

---

### 阶段8: 测试验证
**目标**: 确保功能完整可用

**检查清单**:
- [ ] 文件上传功能正常
- [ ] 文件预览显示正确
- [ ] AI分析接口调用成功
- [ ] 表单编辑功能正常
- [ ] 重新评估功能正常
- [ ] 保存功能正常
- [ ] 错误提示清晰
- [ ] 加载状态显示
- [ ] 响应式布局正常

---

## 常用命令

```bash
# 开发
npm run dev              # 启动开发服务器
npm run build            # 生产构建
npm run preview          # 预览生产构建

# 代码质量
npm run lint             # ESLint检查
npm run lint:fix         # 自动修复
npm run typecheck        # TypeScript类型检查

# 测试
npm run test             # 运行测试
npm run test:watch       # 监视模式
```

---

## 最佳实践

1. **类型优先**
   - 先定义类型，再写实现
   - 避免使用any
   - 充分利用TypeScript推断

2. **组件拆分**
   - 单一职责原则
   - 识别可复用逻辑提取为Hook
   - 复杂组件拆分为子组件

3. **性能优化**
   - 使用useCallback缓存函数
   - 使用useMemo缓存计算结果
   - 使用React.memo避免不必要渲染
   - 图片懒加载

4. **错误处理**
   - 统一API错误处理
   - 组件内错误边界
   - 用户友好的错误提示

5. **用户体验**
   - 加载状态反馈
   - 操作成功/失败提示
   - 表单验证即时反馈
   - 键盘可访问性

6. **代码规范**
   - 统一的导入顺序
   - 一致的命名规范
   - 清晰的注释
   - 避免魔法数字

---

## 安全检查清单

- [ ] 用户输入都经过验证
- [ ] XSS防护措施（不直接使用dangerouslySetInnerHTML）
- [ ] 敏感信息不存储在本地存储
- [ ] API错误不暴露敏感信息
- [ ] 文件上传限制类型和大小
- [ ] 防止CSRF攻击
