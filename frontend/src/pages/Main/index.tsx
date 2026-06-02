import React, { useEffect } from 'react';
import { Layout, Menu, Button, message, ConfigProvider, theme, Dropdown, Avatar, Space } from 'antd';
import { useDispatch, useSelector } from 'react-redux';
import {
  LogoutOutlined,
  DownloadOutlined,
  UploadOutlined,
  UserOutlined,
  UnorderedListOutlined,
  FolderOutlined,
  TagsOutlined,
  RobotOutlined,
} from '@ant-design/icons';
import type { RootState, AppDispatch } from '../../store';
import { logout, fetchCategories, fetchTags } from '../../store';
import { exportApi } from '../../services/api';
import TaskList from '../../components/TaskList';
import TaskForm from '../../components/TaskForm';
import CategoryManager from '../../components/CategoryManager';
import TagManager from '../../components/TagManager';
import { AIAssistant } from '../../components/AIAssistant';

const { Header, Sider, Content } = Layout;

const MainPage: React.FC = () => {
  const [activeTab, setActiveTab] = React.useState('tasks');
  const [showTaskForm, setShowTaskForm] = React.useState(false);
  const { user } = useSelector((state: RootState) => state.auth);
  const dispatch = useDispatch<AppDispatch>();

  useEffect(() => {
    dispatch(fetchCategories());
    dispatch(fetchTags());
  }, [dispatch]);

  const handleLogout = () => {
    dispatch(logout());
    message.success('已退出登录');
  };

  const handleExportJSON = async () => {
    try {
      const response = await exportApi.exportJSON();
      const url = URL.createObjectURL(new Blob([response.data]));
      const a = document.createElement('a');
      a.href = url;
      a.download = 'todos_export.json';
      a.click();
      URL.revokeObjectURL(url);
      message.success('导出成功');
    } catch (error) {
      message.error('导出失败');
    }
  };

  const handleExportCSV = async () => {
    try {
      const response = await exportApi.exportCSV();
      const url = URL.createObjectURL(new Blob([response.data]));
      const a = document.createElement('a');
      a.href = url;
      a.download = 'todos_export.csv';
      a.click();
      URL.revokeObjectURL(url);
      message.success('导出成功');
    } catch (error) {
      message.error('导出失败');
    }
  };

  const handleImportJSON = (file: File) => {
    const reader = new FileReader();
    reader.onload = async (e) => {
      try {
        const data = JSON.parse(e.target?.result as string);
        await exportApi.importJSON(data);
        message.success('导入成功');
        dispatch(fetchCategories());
        dispatch(fetchTags());
      } catch (error) {
        message.error('导入失败');
      }
    };
    reader.readAsText(file);
    return false;
  };

  const menuItems = [
    { key: 'tasks', label: '任务列表', icon: <UnorderedListOutlined /> },
    { key: 'categories', label: '分类管理', icon: <FolderOutlined /> },
    { key: 'tags', label: '标签管理', icon: <TagsOutlined /> },
    { key: 'ai-assistant', label: 'AI 助手', icon: <RobotOutlined /> },
  ];

  const userMenuItems = [
    {
      key: 'logout',
      label: '退出登录',
      icon: <LogoutOutlined />,
      danger: true,
      onClick: handleLogout,
    },
  ];

  return (
    <ConfigProvider
      theme={{
        algorithm: theme.defaultAlgorithm,
        token: {
          colorPrimary: '#667eea',
          borderRadius: 8,
        },
      }}
    >
      <Layout style={{ minHeight: '100vh' }}>
        <Header style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          background: '#fff',
          padding: '0 32px',
          borderBottom: '1px solid #f0f0f0',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.04)',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <div style={{
              width: 40,
              height: 40,
              borderRadius: 10,
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}>
              <UnorderedListOutlined style={{ fontSize: 20, color: 'white' }} />
            </div>
            <span style={{
              fontSize: 20,
              fontWeight: 700,
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}>
              待办事项管理
            </span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <Space>
              <Button
                icon={<DownloadOutlined />}
                onClick={handleExportJSON}
              >
                导出 JSON
              </Button>
              <Button
                icon={<DownloadOutlined />}
                onClick={handleExportCSV}
              >
                导出 CSV
              </Button>
              <input
                type="file"
                accept=".json"
                style={{ display: 'none' }}
                id="import-input"
                onChange={(e) => {
                  const file = e.target.files?.[0];
                  if (file) {
                    handleImportJSON(file);
                  }
                }}
              />
              <Button
                type="primary"
                icon={<UploadOutlined />}
                onClick={() => document.getElementById('import-input')?.click()}
                style={{
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  border: 'none',
                }}
              >
                导入 JSON
              </Button>
            </Space>

            <div style={{
              width: 1,
              height: 32,
              background: '#f0f0f0',
              margin: '0 8px',
            }} />

            <Dropdown
              menu={{ items: userMenuItems }}
              placement="bottomRight"
            >
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: 12,
                cursor: 'pointer',
                padding: '4px 12px',
                borderRadius: 8,
                transition: 'background 0.2s',
              }}>
                <Avatar
                  style={{
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  }}
                  icon={<UserOutlined />}
                />
                <span style={{
                  color: '#262626',
                  fontWeight: 500,
                }}>
                  {user?.username}
                </span>
              </div>
            </Dropdown>
          </div>
        </Header>

        <Layout>
          <Sider
            width={240}
            style={{
              background: '#fff',
              borderRight: '1px solid #f0f0f0',
            }}
          >
            <Menu
              mode="inline"
              selectedKeys={[activeTab]}
              items={menuItems}
              onClick={({ key }) => setActiveTab(key)}
              className="main-menu"
              style={{
                height: '100%',
                borderRight: 0,
                paddingTop: 16,
              }}
            />
          </Sider>
          <Content style={{
            padding: '32px',
            background: '#f5f7fa',
          }}>
            {activeTab === 'tasks' && (
              <TaskList onAddTask={() => setShowTaskForm(true)} />
            )}
            {activeTab === 'categories' && <CategoryManager />}
            {activeTab === 'tags' && <TagManager />}
            {activeTab === 'ai-assistant' && <AIAssistant />}
          </Content>
        </Layout>

        <TaskForm
          open={showTaskForm}
          onClose={() => setShowTaskForm(false)}
        />
      </Layout>
    </ConfigProvider>
  );
};

export default MainPage;
