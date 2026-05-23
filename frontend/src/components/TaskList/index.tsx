import React, { useEffect, useState } from 'react';
import {
  List,
  Card,
  Button,
  Tag,
  Select,
  Input,
  Checkbox,
  Space,
  Popconfirm,
  message,
  Empty,
} from 'antd';
import {
  EditOutlined,
  DeleteOutlined,
  PlusOutlined,
  CalendarOutlined,
} from '@ant-design/icons';
import { useDispatch, useSelector } from 'react-redux';
import type { RootState, AppDispatch } from '../../store';
import {
  fetchTasks,
  updateTask,
  deleteTask,
} from '../../store';
import { tasksApi } from '../../services/api';
import type { Task, Priority } from '../../types';
import TaskForm from '../TaskForm';

const { Search } = Input;
const { Option } = Select;

interface TaskListProps {
  onAddTask: () => void;
}

const TaskList: React.FC<TaskListProps> = () => {
  const [filters, setFilters] = useState({
    priority: '' as string,
    categoryId: '' as string,
    completed: '' as string,
    search: '',
  });
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [showForm, setShowForm] = useState(false);

  const { tasks, categories } = useSelector((state: RootState) => state.data);
  const dispatch = useDispatch<AppDispatch>();

  useEffect(() => {
    loadTasks();
  }, [dispatch, filters]);

  const loadTasks = () => {
    const params: any = {};
    if (filters.priority) params.priority = filters.priority;
    if (filters.categoryId) params.categoryId = filters.categoryId;
    if (filters.completed) params.completed = filters.completed;
    if (filters.search) params.search = filters.search;
    dispatch(fetchTasks(params));
  };

  const handleToggleComplete = async (task: Task) => {
    try {
      const response = await tasksApi.toggle(task.id);
      dispatch(updateTask(response.data));
      message.success(task.completed ? '已标记为未完成' : '已标记为完成');
    } catch (error) {
      message.error('操作失败');
    }
  };

  const handleDelete = async (taskId: string) => {
    try {
      await tasksApi.delete(taskId);
      dispatch(deleteTask(taskId));
      message.success('删除成功');
    } catch (error) {
      message.error('删除失败');
    }
  };

  const getPriorityColor = (priority: Priority) => {
    switch (priority) {
      case 'HIGH': return '#ff4d4f';
      case 'MEDIUM': return '#faad14';
      case 'LOW': return '#52c41a';
      default: return '#d9d9d9';
    }
  };

  const getPriorityText = (priority: Priority) => {
    switch (priority) {
      case 'HIGH': return '高';
      case 'MEDIUM': return '中';
      case 'LOW': return '低';
      default: return '中';
    }
  };

  const renderTaskItem = (task: Task) => (
    <List.Item style={{ padding: '8px 0' }}>
      <Card
        hoverable
        style={{
          width: '100%',
          opacity: task.completed ? 0.7 : 1,
          borderRadius: 12,
          border: task.completed ? '1px solid #f0f0f0' : '1px solid #f0f0f0',
          boxShadow: task.completed ? 'none' : '0 2px 8px rgba(0, 0, 0, 0.04)',
          transition: 'all 0.2s',
        }}
        styles={{
          body: {
            padding: '20px 24px',
          },
        }}
      >
        <div style={{ display: 'flex', alignItems: 'flex-start', gap: 16 }}>
          <Checkbox
            checked={task.completed}
            onChange={() => handleToggleComplete(task)}
            style={{ marginTop: 4 }}
          />
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: 12,
              marginBottom: 12,
              flexWrap: 'wrap',
            }}>
              <h3 style={{
                margin: 0,
                fontSize: 16,
                fontWeight: 600,
                color: task.completed ? '#8c8c8c' : '#262626',
                textDecoration: task.completed ? 'line-through' : 'none',
              }}>
                {task.title}
              </h3>
              <Tag
                color={getPriorityColor(task.priority)}
                style={{
                  margin: 0,
                  borderRadius: 6,
                  fontWeight: 500,
                }}
              >
                {getPriorityText(task.priority)}优先级
              </Tag>
              {task.category && (
                <Tag
                  color={task.category.color}
                  style={{
                    margin: 0,
                    borderRadius: 6,
                  }}
                >
                  {task.category.name}
                </Tag>
              )}
            </div>

            {task.description && (
              <p style={{
                color: task.completed ? '#bfbfbf' : '#595959',
                marginBottom: 12,
                fontSize: 14,
                lineHeight: 1.6,
              }}>
                {task.description}
              </p>
            )}

            {task.tags.length > 0 && (
              <div style={{ marginBottom: 12, display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                {task.tags.map(tag => (
                  <Tag
                    key={tag.id}
                    color={tag.color}
                    style={{
                      borderRadius: 4,
                      fontSize: 12,
                    }}
                  >
                    {tag.name}
                  </Tag>
                ))}
              </div>
            )}

            <div style={{ display: 'flex', alignItems: 'center', gap: 16, flexWrap: 'wrap' }}>
              {task.dueDate && (
                <span style={{
                  color: '#8c8c8c',
                  fontSize: 13,
                  display: 'flex',
                  alignItems: 'center',
                  gap: 4,
                }}>
                  <CalendarOutlined />
                  {new Date(task.dueDate).toLocaleDateString()}
                </span>
              )}
            </div>
          </div>

          <Space>
            <Button
              type="text"
              icon={<EditOutlined />}
              onClick={() => {
                setEditingTask(task);
                setShowForm(true);
              }}
              style={{
                color: '#667eea',
              }}
            >
              编辑
            </Button>
            <Popconfirm
              title="确定要删除这个任务吗？"
              onConfirm={() => handleDelete(task.id)}
              okText="确定"
              cancelText="取消"
            >
              <Button type="text" danger icon={<DeleteOutlined />}>
                删除
              </Button>
            </Popconfirm>
          </Space>
        </div>
      </Card>
    </List.Item>
  );

  return (
    <div>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 24,
      }}>
        <h2 style={{
          margin: 0,
          fontSize: 24,
          fontWeight: 700,
          color: '#262626',
        }}>任务列表</h2>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={() => setShowForm(true)}
          size="large"
          style={{
            height: 44,
            padding: '0 24px',
            fontSize: 15,
            fontWeight: 500,
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            border: 'none',
            boxShadow: '0 4px 12px rgba(102, 126, 234, 0.4)',
          }}
        >
          添加任务
        </Button>
      </div>

      <Card
        style={{
          marginBottom: 24,
          borderRadius: 12,
          border: 'none',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.04)',
        }}
      >
        <Space wrap size="middle">
          <Search
            placeholder="搜索任务"
            style={{ width: 220 }}
            onSearch={(value) => setFilters(f => ({ ...f, search: value }))}
            allowClear
            size="large"
          />
          <Select
            placeholder="优先级"
            style={{ width: 130 }}
            allowClear
            onChange={(value) => setFilters(f => ({ ...f, priority: value }))}
            size="large"
          >
            <Option value="HIGH">高</Option>
            <Option value="MEDIUM">中</Option>
            <Option value="LOW">低</Option>
          </Select>
          <Select
            placeholder="分类"
            style={{ width: 160 }}
            allowClear
            onChange={(value) => setFilters(f => ({ ...f, categoryId: value }))}
            size="large"
          >
            {categories.map(category => (
              <Option key={category.id} value={category.id}>
                {category.name}
              </Option>
            ))}
          </Select>
          <Select
            placeholder="状态"
            style={{ width: 130 }}
            allowClear
            onChange={(value) => setFilters(f => ({ ...f, completed: value }))}
            size="large"
          >
            <Option value="true">已完成</Option>
            <Option value="false">未完成</Option>
          </Select>
        </Space>
      </Card>

      <List
        dataSource={tasks}
        renderItem={renderTaskItem}
        locale={{
          emptyText: (
            <Empty
              description="暂无任务"
              image={Empty.PRESENTED_IMAGE_SIMPLE}
            />
          ),
        }}
      />

      <TaskForm
        open={showForm}
        task={editingTask}
        onClose={() => {
          setShowForm(false);
          setEditingTask(null);
        }}
      />
    </div>
  );
};

export default TaskList;
