import React, { useEffect, useState, useCallback } from 'react';
import {
  Modal,
  Form,
  Input,
  Select,
  DatePicker,
  Button,
  message,
  Card,
  Typography,
  Badge,
} from 'antd';
import { useDispatch, useSelector } from 'react-redux';
import type { RootState, AppDispatch } from '../../store';
import { addTask, updateTask } from '../../store';
import { tasksApi, ragApi } from '../../services/api';
import type { Task, TaskFormData } from '../../types';

const { TextArea } = Input;
const { Option } = Select;
const { Text, Paragraph } = Typography;

interface TaskFormProps {
  open: boolean;
  task?: Task | null;
  onClose: () => void;
}

const TaskForm: React.FC<TaskFormProps> = ({ open, task, onClose }) => {
  const [form] = Form.useForm();
  const { categories, tags } = useSelector((state: RootState) => state.data);
  const dispatch = useDispatch<AppDispatch>();
  const [recommendations, setRecommendations] = useState<string[]>([]);
  const [isLoadingRecommendations, setIsLoadingRecommendations] = useState(false);
  const [showRecommendations, setShowRecommendations] = useState(false);

  useEffect(() => {
    if (open) {
      setRecommendations([]);
      setShowRecommendations(false);
      if (task) {
        form.setFieldsValue({
          title: task.title,
          description: task.description,
          priority: task.priority,
          categoryId: task.categoryId,
          tagIds: task.tags.map(t => t.id),
          dueDate: task.dueDate ? new Date(task.dueDate) : null,
        });
      } else {
        form.resetFields();
      }
    }
  }, [open, task, form]);

  const fetchRecommendations = useCallback(async () => {
    const values = form.getFieldsValue();
    if (!values.title?.trim()) return;

    setIsLoadingRecommendations(true);
    setShowRecommendations(true);
    try {
      const response = await ragApi.getRecommendations({
        title: values.title,
        description: values.description || '',
        priority: values.priority || 'MEDIUM',
      });
      setRecommendations(response.data.recommendations.suggestions);
    } catch (error) {
      console.error('Failed to get recommendations:', error);
    } finally {
      setIsLoadingRecommendations(false);
    }
  }, [form]);

  const handleTitleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    // 简单的防抖逻辑
    if (e.target.value.length > 3) {
      fetchRecommendations();
    }
  };

  const handleSubmit = async (values: any) => {
    try {
      const formData: TaskFormData = {
        title: values.title,
        description: values.description,
        priority: values.priority || 'MEDIUM',
        categoryId: values.categoryId,
        tagIds: values.tagIds || [],
        dueDate: values.dueDate ? values.dueDate.toISOString() : undefined,
      };

      if (task) {
        const response = await tasksApi.update(task.id, formData);
        dispatch(updateTask(response.data));
        message.success('更新成功');
      } else {
        const response = await tasksApi.create(formData);
        dispatch(addTask(response.data));
        message.success('创建成功');
      }
      onClose();
    } catch (error) {
      message.error('操作失败');
    }
  };

  return (
    <Modal
      title={task ? '编辑任务' : '添加任务'}
      open={open}
      onCancel={onClose}
      footer={null}
      destroyOnHidden
      centered
      styles={{
        header: {
          fontSize: 18,
          fontWeight: 600,
        },
      }}
    >
      <Form
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        style={{ marginTop: 16 }}
      >
        <Form.Item
          name="title"
          label="标题"
          rules={[{ required: true, message: '请输入标题' }]}
        >
          <Input 
            placeholder="请输入任务标题" 
            size="large" 
            onChange={handleTitleChange}
          />
        </Form.Item>

        {showRecommendations && (
          <div style={{ marginBottom: 16 }}>
            <Card 
              size="small" 
              title={
                <span>
                  <Badge status="processing" text="AI 建议" />
                </span>
              }
              style={{ background: '#f6ffed', borderColor: '#b7eb8f' }}
            >
              {isLoadingRecommendations ? (
                <Paragraph type="secondary">正在思考中...</Paragraph>
              ) : recommendations.length > 0 ? (
                <ul style={{ margin: 0, paddingLeft: 16 }}>
                  {recommendations.map((suggestion, index) => (
                    <li key={index} style={{ marginBottom: 8 }}>
                      <Text type="success">{suggestion}</Text>
                    </li>
                  ))}
                </ul>
              ) : (
                <Paragraph type="secondary">暂无建议</Paragraph>
              )}
            </Card>
          </div>
        )}

        <Form.Item
          name="description"
          label="描述"
        >
          <TextArea rows={4} placeholder="请输入任务描述" size="large" />
        </Form.Item>

        <Form.Item
          name="priority"
          label="优先级"
          initialValue="MEDIUM"
        >
          <Select size="large">
            <Option value="HIGH">高</Option>
            <Option value="MEDIUM">中</Option>
            <Option value="LOW">低</Option>
          </Select>
        </Form.Item>

        <Form.Item
          name="categoryId"
          label="分类"
        >
          <Select placeholder="请选择分类" allowClear size="large">
            {categories.map(category => (
              <Option key={category.id} value={category.id}>
                {category.name}
              </Option>
            ))}
          </Select>
        </Form.Item>

        <Form.Item
          name="tagIds"
          label="标签"
        >
          <Select mode="multiple" placeholder="请选择标签" allowClear size="large">
            {tags.map(tag => (
              <Option key={tag.id} value={tag.id}>
                {tag.name}
              </Option>
            ))}
          </Select>
        </Form.Item>

        <Form.Item
          name="dueDate"
          label="截止日期"
        >
          <DatePicker showTime style={{ width: '100%' }} size="large" />
        </Form.Item>

        <Form.Item style={{ textAlign: 'right', marginBottom: 0, marginTop: 24 }}>
          <Button onClick={onClose} style={{ marginRight: 8, height: 40 }} size="large">
            取消
          </Button>
          <Button
            type="primary"
            htmlType="submit"
            size="large"
            style={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              border: 'none',
              height: 40,
              padding: '0 24px',
            }}
          >
            {task ? '保存' : '创建'}
          </Button>
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default TaskForm;
