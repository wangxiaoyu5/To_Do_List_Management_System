import React, { useState } from 'react';
import {
  List,
  Card,
  Button,
  Input,
  ColorPicker,
  Space,
  Popconfirm,
  message,
  Empty,
  Modal,
  Form,
} from 'antd';
import { EditOutlined, DeleteOutlined, PlusOutlined } from '@ant-design/icons';
import { useDispatch, useSelector } from 'react-redux';
import type { RootState, AppDispatch } from '../../store';
import {
  addTag,
  updateTag,
  deleteTag,
} from '../../store';
import { tagsApi } from '../../services/api';
import type { Tag } from '../../types';
import type { Color } from 'antd/es/color-picker';

const TagManager: React.FC = () => {
  const [editingTag, setEditingTag] = useState<Tag | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [form] = Form.useForm();

  const { tags } = useSelector((state: RootState) => state.data);
  const dispatch = useDispatch<AppDispatch>();

  const handleAdd = async (values: { name: string; color: Color }) => {
    try {
      const response = await tagsApi.create({
        name: values.name,
        color: typeof values.color === 'string' ? values.color : values.color.toHexString(),
      });
      dispatch(addTag(response.data));
      message.success('创建成功');
      setShowModal(false);
      form.resetFields();
    } catch (error) {
      message.error('创建失败');
    }
  };

  const handleEdit = async (values: { name: string; color: Color }) => {
    if (!editingTag) return;
    try {
      const response = await tagsApi.update(editingTag.id, {
        name: values.name,
        color: typeof values.color === 'string' ? values.color : values.color.toHexString(),
      });
      dispatch(updateTag(response.data));
      message.success('更新成功');
      setShowModal(false);
      setEditingTag(null);
      form.resetFields();
    } catch (error) {
      message.error('更新失败');
    }
  };

  const handleDelete = async (tagId: string) => {
    try {
      await tagsApi.delete(tagId);
      dispatch(deleteTag(tagId));
      message.success('删除成功');
    } catch (error) {
      message.error('删除失败');
    }
  };

  const openEditModal = (tag: Tag) => {
    setEditingTag(tag);
    form.setFieldsValue({
      name: tag.name,
      color: tag.color,
    });
    setShowModal(true);
  };

  const openAddModal = () => {
    setEditingTag(null);
    form.resetFields();
    setShowModal(true);
  };

  const handleSubmit = (values: any) => {
    if (editingTag) {
      handleEdit(values);
    } else {
      handleAdd(values);
    }
  };

  const renderItem = (tag: Tag) => (
    <List.Item style={{ padding: '8px 0' }}>
      <Card
        hoverable
        style={{
          width: '100%',
          borderRadius: 12,
          border: '1px solid #f0f0f0',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.04)',
          transition: 'all 0.2s',
        }}
        styles={{
          body: {
            padding: '20px 24px',
          },
        }}
      >
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: 12,
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <div style={{
              width: 28,
              height: 28,
              borderRadius: 8,
              backgroundColor: tag.color,
              boxShadow: '0 2px 6px rgba(0, 0, 0, 0.1)',
            }} />
            <span style={{
              fontWeight: 600,
              fontSize: 15,
              color: '#262626',
            }}>
              {tag.name}
            </span>
          </div>

          <Space>
            <Button
              type="text"
              icon={<EditOutlined />}
              onClick={() => openEditModal(tag)}
              style={{
                color: '#667eea',
              }}
            >
              编辑
            </Button>
            <Popconfirm
              title="确定要删除这个标签吗？"
              onConfirm={() => handleDelete(tag.id)}
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
        }}>标签管理</h2>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={openAddModal}
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
          添加标签
        </Button>
      </div>

      <List
        dataSource={tags}
        renderItem={renderItem}
        locale={{
          emptyText: (
            <Empty
              description="暂无标签"
              image={Empty.PRESENTED_IMAGE_SIMPLE}
            />
          ),
        }}
      />

      <Modal
        title={editingTag ? '编辑标签' : '添加标签'}
        open={showModal}
        onCancel={() => {
          setShowModal(false);
          setEditingTag(null);
        }}
        footer={null}
        destroyOnClose
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
            name="name"
            label="名称"
            rules={[{ required: true, message: '请输入标签名称' }]}
          >
            <Input placeholder="请输入标签名称" size="large" />
          </Form.Item>

          <Form.Item
            name="color"
            label="颜色"
            initialValue="#667eea"
          >
            <ColorPicker showText format="hex" size="large" />
          </Form.Item>

          <Form.Item style={{ textAlign: 'right', marginBottom: 0, marginTop: 24 }}>
            <Button
              onClick={() => {
                setShowModal(false);
                setEditingTag(null);
              }}
              style={{ marginRight: 8, height: 40 }}
              size="large"
            >
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
              {editingTag ? '保存' : '创建'}
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default TagManager;
