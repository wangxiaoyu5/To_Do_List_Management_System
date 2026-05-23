---
name: "backend-development"
description: "提供标准化后端开发规范和流程指导。Invoke when starting new backend features, implementing APIs, or following the standardized development workflow."
---

# 后端开发规范与流程

## 开发流程

### 阶段1: 需求分析
**目标**: 充分理解业务需求,明确技术边界

**执行步骤**:
1. **需求拆解**
   - 列出所有功能点
   - 识别核心业务逻辑
   - 标注技术难点和风险点
   - 确定依赖关系

2. **接口规划**
   - 确定需要的API端点
   - 定义请求/响应数据结构
   - 规划错误码和状态码
   - 考虑扩展性

3. **数据模型设计**
   - 设计核心数据类型
   - 定义接口契约
   - 考虑数据验证规则

**输出物**:
- 需求分析文档
- 接口清单
- 数据模型草图

---

### 阶段2: 制定计划
**目标**: 将需求转化为可执行的开发任务

**执行步骤**:
1. **任务分解**
   ```
   功能模块 -> 子任务 -> 具体实现步骤
   ```

2. **优先级排序**
   - P0: 核心功能,阻塞后续开发
   - P1: 重要功能,影响用户体验
   - P2: 优化功能,可延后

3. **时间估算**
   - 为每个任务估算开发时间
   - 预留20%缓冲时间
   - 识别依赖关系,确定执行顺序

4. **技术选型确认**
   - 确认使用的库/框架版本
   - 评估第三方服务依赖
   - 确定测试策略

**输出物**:
- 开发任务清单(Todo List)
- 时间规划表
- 技术方案文档

---

### 阶段3: 代码阅览
**目标**: 理解现有代码结构,确保新功能与现有架构兼容

**执行步骤**:
1. **架构理解**
   - 查看项目整体结构
   - 理解分层架构(Controller/Service/Repository)
   - 识别公共模块和工具函数

2. **相关代码审查**
   - 查找相似功能的实现
   - 理解现有API的设计模式
   - 查看错误处理方式
   - 学习现有的日志和监控实践

3. **依赖分析**
   - 查看package.json依赖
   - 理解配置管理方式
   - 识别需要复用的服务/工具

**输出物**:
- 代码结构笔记
- 可复用组件清单
- 实现参考案例

---

### 阶段4: 功能实现
**目标**: 按照规范高质量完成代码开发

#### 4.1 项目结构规范
```
server/
├── src/
│   ├── index.ts              # 入口文件
│   ├── routes/               # 路由层
│   │   └── [feature].ts      # 功能路由
│   ├── services/             # 业务逻辑层
│   │   └── [feature]Service.ts
│   ├── middlewares/          # 中间件
│   ├── utils/                # 工具函数
│   └── types/                # 类型定义
│       └── index.ts
├── uploads/                  # 临时上传目录
├── tests/                    # 测试文件
├── .env                      # 环境变量
└── package.json
```

#### 4.2 类型定义规范
```typescript
// types/index.ts

// 请求类型
export interface CreateUserRequest {
  username: string;
  email: string;
  password: string;
}

// 响应类型
export interface ApiResponse<T = unknown> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

// 业务类型
export interface User {
  id: string;
  username: string;
  email: string;
  createdAt: Date;
}
```

#### 4.3 路由层规范
```typescript
// routes/user.ts
import { Router } from 'express';
import { userService } from '../services/userService';
import type { CreateUserRequest, ApiResponse, User } from '../types';

const router = Router();

router.post('/create', async (req, res) => {
  try {
    const request: CreateUserRequest = req.body;
    
    // 参数验证
    if (!request.username || !request.email) {
      const response: ApiResponse = {
        success: false,
        error: '用户名和邮箱不能为空'
      };
      return res.status(400).json(response);
    }
    
    // 调用服务层
    const user = await userService.createUser(request);
    
    const response: ApiResponse<User> = {
      success: true,
      data: user,
      message: '用户创建成功'
    };
    res.json(response);
  } catch (error) {
    console.error('Create user error:', error);
    
    const response: ApiResponse = {
      success: false,
      error: error instanceof Error ? error.message : '服务器内部错误'
    };
    res.status(500).json(response);
  }
});

export default router;
```

#### 4.4 服务层规范
```typescript
// services/userService.ts
import type { CreateUserRequest, User } from '../types';

export class UserService {
  /**
   * 创建用户
   * @param request 创建用户请求
   * @returns 创建的用户对象
   */
  async createUser(request: CreateUserRequest): Promise<User> {
    // 业务逻辑
    // 1. 验证邮箱格式
    // 2. 检查用户是否存在
    // 3. 密码加密
    // 4. 保存到数据库
    // 5. 返回用户信息
    
    return {
      id: 'generated-id',
      username: request.username,
      email: request.email,
      createdAt: new Date()
    };
  }
}

export const userService = new UserService();
```

#### 4.5 错误处理规范
```typescript
// 统一错误处理
class AppError extends Error {
  constructor(
    public code: string,
    message: string,
    public statusCode: number = 500
  ) {
    super(message);
    this.name = 'AppError';
  }
}

// 使用示例
if (!user) {
  throw new AppError('USER_NOT_FOUND', '用户不存在', 404);
}

// 全局错误处理中间件
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error('Error:', err);
  
  if (err instanceof AppError) {
    res.status(err.statusCode).json({
      success: false,
      error: err.message,
      code: err.code
    });
  } else {
    res.status(500).json({
      success: false,
      error: '服务器内部错误'
    });
  }
});
```

#### 4.6 环境变量管理规范
```typescript
// config/index.ts
import dotenv from 'dotenv';
import path from 'path';

// 加载环境变量
dotenv.config({
  path: path.resolve(__dirname, '../../.env')
});

// 配置对象(延迟读取)
export function getConfig() {
  return {
    port: parseInt(process.env.PORT || '3001'),
    nodeEnv: process.env.NODE_ENV || 'development',
    
    // 数据库配置
    database: {
      host: process.env.DB_HOST || 'localhost',
      port: parseInt(process.env.DB_PORT || '5432'),
      name: process.env.DB_NAME || '',
      user: process.env.DB_USER || '',
      password: process.env.DB_PASSWORD || ''
    },
    
    // AI服务配置
    ai: {
      apiKey: process.env.AI_API_KEY || '',
      baseUrl: process.env.AI_BASE_URL || '',
      model: process.env.AI_MODEL || '',
      timeout: parseInt(process.env.AI_TIMEOUT || '120000')
    },
    
    // 文件上传配置
    upload: {
      maxSize: parseInt(process.env.MAX_FILE_SIZE || '10485760'),
      allowedTypes: (process.env.ALLOWED_TYPES || 'pdf,doc,docx').split(',')
    }
  };
}

// 启动时验证配置
export function validateConfig() {
  const config = getConfig();
  
  console.log('🔧 配置检查:');
  console.log(`  PORT: ${config.port}`);
  console.log(`  NODE_ENV: ${config.nodeEnv}`);
  console.log(`  AI_API_KEY: ${config.ai.apiKey ? '已配置 ✓' : '未配置 ✗'}`);
  console.log(`  DB_HOST: ${config.database.host}`);
}
```

#### 4.7 日志规范
```typescript
// utils/logger.ts
export const logger = {
  info: (message: string, meta?: Record<string, unknown>) => {
    console.log(`[INFO] ${new Date().toISOString()} - ${message}`, meta || '');
  },
  
  error: (message: string, error?: Error, meta?: Record<string, unknown>) => {
    console.error(`[ERROR] ${new Date().toISOString()} - ${message}`);
    if (error) {
      console.error('  Error:', error.message);
      console.error('  Stack:', error.stack);
    }
    if (meta) {
      console.error('  Meta:', meta);
    }
  },
  
  warn: (message: string, meta?: Record<string, unknown>) => {
    console.warn(`[WARN] ${new Date().toISOString()} - ${message}`, meta || '');
  },
  
  debug: (message: string, meta?: Record<string, unknown>) => {
    if (process.env.NODE_ENV === 'development') {
      console.log(`[DEBUG] ${new Date().toISOString()} - ${message}`, meta || '');
    }
  }
};
```

#### 4.8 HTTP客户端规范
```typescript
// utils/httpClient.ts
import axios, { AxiosError, AxiosRequestConfig } from 'axios';
import { logger } from './logger';

export async function httpPost<T>(
  url: string,
  data: unknown,
  config?: AxiosRequestConfig
): Promise<T> {
  try {
    logger.debug(`HTTP POST ${url}`, { data });
    
    const response = await axios.post<T>(url, data, {
      timeout: 30000,
      ...config
    });
    
    logger.debug(`HTTP POST ${url} success`, { status: response.status });
    return response.data;
  } catch (error) {
    logger.error(`HTTP POST ${url} failed`, error as Error);
    
    if (axios.isAxiosError(error)) {
      const axiosError = error as AxiosError;
      throw new Error(
        `HTTP请求失败: ${axiosError.response?.status} - ${
          axiosError.response?.data?.message || axiosError.message
        }`
      );
    }
    throw error;
  }
}
```

#### 4.9 文件处理规范
```typescript
// middlewares/upload.ts
import multer from 'multer';
import path from 'path';
import { getConfig } from '../config';

const config = getConfig();

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = `${Date.now()}-${Math.round(Math.random() * 1e9)}`;
    cb(null, `${uniqueSuffix}-${file.originalname}`);
  }
});

const fileFilter = (
  req: Express.Request,
  file: Express.Multer.File,
  cb: multer.FileFilterCallback
) => {
  const allowedTypes = ['application/pdf', 'application/msword'];
  
  if (allowedTypes.includes(file.mimetype)) {
    cb(null, true);
  } else {
    cb(new Error('不支持的文件类型'));
  }
};

export const upload = multer({
  storage,
  fileFilter,
  limits: {
    fileSize: config.upload.maxSize
  }
});

// 清理临时文件
import fs from 'fs';

export function cleanupFile(filePath: string): void {
  try {
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
      logger.debug(`Cleaned up file: ${filePath}`);
    }
  } catch (error) {
    logger.error(`Failed to cleanup file: ${filePath}`, error as Error);
  }
}
```

#### 4.10 AI服务集成规范
```typescript
// services/aiService.ts
import { getConfig } from '../config';
import { httpPost } from '../utils/httpClient';
import { logger } from '../utils/logger';

interface AIRequest {
  model: string;
  messages: Array<{ role: string; content: string }>;
  temperature?: number;
  response_format?: { type: string };
}

interface AIResponse {
  choices: Array<{
    message: {
      content: string;
    };
  }>;
}

export class AIService {
  private config = getConfig();
  
  /**
   * 调用AI服务
   * @param prompt 提示词
   * @param options 可选配置
   */
  async callAI(
    prompt: string,
    options: { jsonMode?: boolean; temperature?: number } = {}
  ): Promise<string> {
    const { jsonMode = false, temperature = 0.7 } = options;
    
    const request: AIRequest = {
      model: this.config.ai.model,
      messages: [
        { role: 'system', content: '你是一个专业的助手' },
        { role: 'user', content: prompt }
      ],
      temperature,
      ...(jsonMode && { response_format: { type: 'json_object' } })
    };
    
    try {
      logger.info('Calling AI service', { model: request.model });
      
      const response = await httpPost<AIResponse>(
        `${this.config.ai.baseUrl}/chat/completions`,
        request,
        {
          headers: {
            Authorization: `Bearer ${this.config.ai.apiKey}`,
            'Content-Type': 'application/json'
          },
          timeout: this.config.ai.timeout
        }
      );
      
      const content = response.choices[0]?.message?.content;
      
      if (!content) {
        throw new Error('AI返回内容为空');
      }
      
      logger.info('AI service responded successfully');
      return content;
    } catch (error) {
      logger.error('AI service call failed', error as Error);
      throw new Error(`AI服务调用失败: ${(error as Error).message}`);
    }
  }
}

export const aiService = new AIService();
```

**输出物**:
- 功能代码
- 单元测试
- 代码注释

---

### 阶段5: 生成接口文档
**目标**: 自动生成API文档,确保前后端协作顺畅

**执行步骤**:
1. **文档生成**
   - 使用工具从代码生成文档(如TypeDoc + 自定义模板)
   - 或手动维护Markdown文档

2. **文档内容规范**
   ```markdown
   # API文档

   ## 基础信息
   - Base URL: `http://localhost:3001/api`
   - Content-Type: `application/json`

   ## 接口列表

   ### POST /users/create
   创建新用户

   #### 请求参数
   | 字段 | 类型 | 必填 | 说明 |
   |------|------|------|------|
   | username | string | 是 | 用户名 |
   | email | string | 是 | 邮箱 |
   | password | string | 是 | 密码 |

   #### 响应示例
   ```json
   {
     "success": true,
     "data": {
       "id": "123",
       "username": "john",
       "email": "john@example.com",
       "createdAt": "2024-01-01T00:00:00Z"
     },
     "message": "用户创建成功"
   }
   ```

   #### 错误码
   | 状态码 | 说明 |
   |--------|------|
   | 400 | 参数错误 |
   | 409 | 用户已存在 |
   | 500 | 服务器内部错误 |
   ```

3. **文档验证**
   - 确保所有接口都有文档
   - 验证请求/响应示例可运行
   - 检查错误码完整性

**输出物**:
- API_DOCUMENTATION.md
- 接口变更日志

---

### 阶段6: 运行项目
**目标**: 确保项目可正常运行,功能验证通过

**执行步骤**:
1. **环境准备**
   ```bash
   # 安装依赖
   npm install
   
   # 配置环境变量
   cp .env.example .env
   # 编辑 .env 文件
   ```

2. **开发模式启动**
   ```bash
   # 热重载模式
   npm run dev
   
   # 验证服务启动
   curl http://localhost:3001/health
   ```

3. **接口测试**
   ```bash
   # 使用curl或Postman测试
   curl -X POST http://localhost:3001/api/users/create \
     -H "Content-Type: application/json" \
     -d '{"username":"test","email":"test@example.com","password":"123456"}'
   ```

4. **生产构建**
   ```bash
   # 编译TypeScript
   npm run build
   
   # 生产环境运行
   npm start
   ```

5. **健康检查清单**
   - [ ] 服务正常启动无报错
   - [ ] 数据库连接正常
   - [ ] 所有接口可访问
   - [ ] 文件上传功能正常
   - [ ] 错误处理正常工作
   - [ ] 日志输出正常

**输出物**:
- 运行验证报告
- 部署指南

---

## 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 接口 | PascalCase + 后缀 | `UserRequest`, `CreateOrderResponse` |
| 类 | PascalCase | `UserService`, `OrderController` |
| 函数 | camelCase | `createUser`, `validateInput` |
| 常量 | UPPER_SNAKE_CASE | `MAX_FILE_SIZE`, `DEFAULT_TIMEOUT` |
| 文件 | camelCase.ts | `userService.ts`, `orderController.ts` |
| 路由 | kebab-case | `/api/users`, `/orders/create` |
| 环境变量 | UPPER_SNAKE_CASE | `PORT`, `DATABASE_URL` |

---

## 代码质量检查清单

### 提交前检查
- [ ] 代码通过TypeScript编译(`tsc --noEmit`)
- [ ] 代码通过Lint检查(`npm run lint`)
- [ ] 所有测试通过(`npm test`)
- [ ] 没有console.log调试代码(使用logger)
- [ ] 敏感信息未硬编码
- [ ] 错误处理完善

### 代码审查要点
- [ ] 类型定义完整
- [ ] 函数职责单一
- [ ] 错误处理覆盖所有分支
- [ ] 日志记录适当
- [ ] 性能考虑(如避免N+1查询)
- [ ] 安全性(输入验证、SQL注入防护)

---

## 常用命令

```bash
# 开发
npm run dev              # 热重载开发模式
npm run build            # 编译TypeScript
npm start                # 生产模式运行

# 代码质量
npm run lint             # ESLint检查
npm run lint:fix         # 自动修复Lint问题
npm run typecheck        # TypeScript类型检查
npm run test             # 运行测试
npm run test:watch       # 测试监视模式

# 数据库
npm run db:migrate       # 执行迁移
npm run db:seed          # 填充种子数据

# 文档
npm run docs:generate    # 生成API文档
```

---

## 最佳实践

1. **单一职责原则**
   - 每个函数只做一件事
   - 每个服务只负责一个业务领域

2. **依赖注入**
   - 使用构造函数注入依赖
   - 便于测试和解耦

3. **防御性编程**
   - 验证所有输入
   - 处理所有可能的错误情况

4. **日志记录**
   - 记录关键业务操作
   - 记录错误详情
   - 避免记录敏感信息

5. **性能优化**
   - 使用连接池
   - 实现缓存策略
   - 异步处理耗时操作

6. **安全性**
   - 使用HTTPS
   - 验证和清理输入
   - 使用参数化查询
   - 设置适当的CORS策略
