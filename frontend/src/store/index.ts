// 导入 Redux Toolkit 的核心函数和类型
import { configureStore, createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';
// 导入应用的类型定义
import type { User, Category, Tag, Task } from '../types';
// 导入 API 服务
import { authApi, categoriesApi, tagsApi, tasksApi } from '../services/api';

// 定义认证状态的接口类型
interface AuthState {
  user: User | null;          // 当前登录用户信息，未登录时为 null
  isAuthenticated: boolean;   // 用户是否已认证
  loading: boolean;           // 认证相关操作是否正在加载中
}

// 认证状态的初始值
const initialAuthState: AuthState = {
  user: null,
  isAuthenticated: false,
  loading: true,
};

// 创建登录的异步 thunk action
export const login = createAsyncThunk(
  'auth/login',
  async (data: { username: string; password: string }, { rejectWithValue }) => {
    try {
      // 调用登录 API
      const response = await authApi.login(data);
      // 将 access token 和 refresh token 存储到 localStorage
      localStorage.setItem('accessToken', response.data.access);
      localStorage.setItem('refreshToken', response.data.refresh);
      // 返回用户信息作为 action payload
      return response.data.user;
    } catch (error: any) {
      // 如果请求失败，返回错误信息
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);

// 创建注册的异步 thunk action
export const register = createAsyncThunk(
  'auth/register',
  async (data: { username: string; email: string; password: string }, { rejectWithValue }) => {
    try {
      // 调用注册 API
      const response = await authApi.register(data);
      // 将 access token 和 refresh token 存储到 localStorage
      localStorage.setItem('accessToken', response.data.access);
      localStorage.setItem('refreshToken', response.data.refresh);
      // 返回用户信息作为 action payload
      return response.data.user;
    } catch (error: any) {
      // 如果请求失败，返回错误信息
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);

// 创建获取当前用户信息的异步 thunk action
export const fetchCurrentUser = createAsyncThunk(
  'auth/fetchCurrentUser',
  async (_, { rejectWithValue }) => {
    try {
      // 调用获取当前用户 API
      const response = await authApi.getCurrentUser();
      // 返回用户信息作为 action payload
      return response.data;
    } catch (error: any) {
      // 如果请求失败，返回错误信息
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);

// 创建认证相关的 slice
const authSlice = createSlice({
  name: 'auth',              // slice 的名称
  initialState: initialAuthState,  // 初始状态
  reducers: {
    // 登出的同步 reducer
    logout: (state) => {
      state.user = null;
      state.isAuthenticated = false;
      // 从 localStorage 中移除 token
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
    },
  },
  // 处理异步 thunk action 的 reducer
  extraReducers: (builder) => {
    builder
      // 登录请求进行中
      .addCase(login.pending, (state) => {
        state.loading = true;
      })
      // 登录请求成功
      .addCase(login.fulfilled, (state, action: PayloadAction<User>) => {
        state.user = action.payload;
        state.isAuthenticated = true;
        state.loading = false;
      })
      // 登录请求失败
      .addCase(login.rejected, (state) => {
        state.loading = false;
      })
      // 注册请求进行中
      .addCase(register.pending, (state) => {
        state.loading = true;
      })
      // 注册请求成功
      .addCase(register.fulfilled, (state, action: PayloadAction<User>) => {
        state.user = action.payload;
        state.isAuthenticated = true;
        state.loading = false;
      })
      // 注册请求失败
      .addCase(register.rejected, (state) => {
        state.loading = false;
      })
      // 获取当前用户请求进行中
      .addCase(fetchCurrentUser.pending, (state) => {
        state.loading = true;
      })
      // 获取当前用户请求成功
      .addCase(fetchCurrentUser.fulfilled, (state, action: PayloadAction<User>) => {
        state.user = action.payload;
        state.isAuthenticated = true;
        state.loading = false;
      })
      // 获取当前用户请求失败
      .addCase(fetchCurrentUser.rejected, (state) => {
        state.loading = false;
      });
  },
});

// 定义数据状态的接口类型
interface DataState {
  categories: Category[];  // 分类列表
  tags: Tag[];             // 标签列表
  tasks: Task[];           // 任务列表
  loading: boolean;        // 数据加载状态
}

// 数据状态的初始值
const initialDataState: DataState = {
  categories: [],
  tags: [],
  tasks: [],
  loading: false,
};

// 创建获取分类列表的异步 thunk action
export const fetchCategories = createAsyncThunk(
  'data/fetchCategories',
  async () => {
    // 调用获取所有分类 API
    const response = await categoriesApi.getAll();
    // 返回分类列表作为 action payload
    return response.data;
  }
);

// 创建获取标签列表的异步 thunk action
export const fetchTags = createAsyncThunk(
  'data/fetchTags',
  async () => {
    // 调用获取所有标签 API
    const response = await tagsApi.getAll();
    // 返回标签列表作为 action payload
    return response.data;
  }
);

// 创建获取任务列表的异步 thunk action，支持筛选参数
export const fetchTasks = createAsyncThunk(
  'data/fetchTasks',
  async (params?: { priority?: string; categoryId?: string; completed?: string; search?: string }) => {
    // 调用获取所有任务 API，传入筛选参数
    const response = await tasksApi.getAll(params);
    // 返回任务列表作为 action payload
    return response.data;
  }
);

// 创建数据相关的 slice
const dataSlice = createSlice({
  name: 'data',                // slice 的名称
  initialState: initialDataState,  // 初始状态
  reducers: {
    // 添加任务的同步 reducer
    addTask: (state, action: PayloadAction<Task>) => {
      // 将新任务添加到列表开头
      state.tasks.unshift(action.payload);
    },
    // 更新任务的同步 reducer
    updateTask: (state, action: PayloadAction<Task>) => {
      // 找到任务在列表中的索引
      const index = state.tasks.findIndex(t => t.id === action.payload.id);
      if (index !== -1) {
        // 更新该任务
        state.tasks[index] = action.payload;
      }
    },
    // 删除任务的同步 reducer
    deleteTask: (state, action: PayloadAction<string>) => {
      // 过滤掉要删除的任务
      state.tasks = state.tasks.filter(t => t.id !== action.payload);
    },
    // 添加分类的同步 reducer
    addCategory: (state, action: PayloadAction<Category>) => {
      // 将新分类添加到列表开头
      state.categories.unshift(action.payload);
    },
    // 更新分类的同步 reducer
    updateCategory: (state, action: PayloadAction<Category>) => {
      // 找到分类在列表中的索引
      const index = state.categories.findIndex(c => c.id === action.payload.id);
      if (index !== -1) {
        // 更新该分类
        state.categories[index] = action.payload;
      }
    },
    // 删除分类的同步 reducer
    deleteCategory: (state, action: PayloadAction<string>) => {
      // 过滤掉要删除的分类
      state.categories = state.categories.filter(c => c.id !== action.payload);
    },
    // 添加标签的同步 reducer
    addTag: (state, action: PayloadAction<Tag>) => {
      // 将新标签添加到列表开头
      state.tags.unshift(action.payload);
    },
    // 更新标签的同步 reducer
    updateTag: (state, action: PayloadAction<Tag>) => {
      // 找到标签在列表中的索引
      const index = state.tags.findIndex(t => t.id === action.payload.id);
      if (index !== -1) {
        // 更新该标签
        state.tags[index] = action.payload;
      }
    },
    // 删除标签的同步 reducer
    deleteTag: (state, action: PayloadAction<string>) => {
      // 过滤掉要删除的标签
      state.tags = state.tags.filter(t => t.id !== action.payload);
    },
  },
  // 处理异步 thunk action 的 reducer
  extraReducers: (builder) => {
    builder
      // 获取分类列表成功
      .addCase(fetchCategories.fulfilled, (state, action) => {
        state.categories = action.payload;
      })
      // 获取标签列表成功
      .addCase(fetchTags.fulfilled, (state, action) => {
        state.tags = action.payload;
      })
      // 获取任务列表进行中
      .addCase(fetchTasks.pending, (state) => {
        state.loading = true;
      })
      // 获取任务列表成功
      .addCase(fetchTasks.fulfilled, (state, action) => {
        state.tasks = action.payload;
        state.loading = false;
      })
      // 获取任务列表失败
      .addCase(fetchTasks.rejected, (state) => {
        state.loading = false;
      });
  },
});

// 导出 authSlice 的 actions
export const { logout } = authSlice.actions;
// 导出 dataSlice 的 actions
export const {
  addTask, updateTask, deleteTask,
  addCategory, updateCategory, deleteCategory,
  addTag, updateTag, deleteTag,
} = dataSlice.actions;

// 创建并配置 Redux store
export const store = configureStore({
  reducer: {
    auth: authSlice.reducer,  // 认证相关的 reducer
    data: dataSlice.reducer,  // 数据相关的 reducer
  },
});

// 导出 RootState 类型，用于在组件中获取 state 时的类型提示
export type RootState = ReturnType<typeof store.getState>;
// 导出 AppDispatch 类型，用于在组件中使用 dispatch 时的类型提示
export type AppDispatch = typeof store.dispatch;
