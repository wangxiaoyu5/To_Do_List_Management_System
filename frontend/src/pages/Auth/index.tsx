import React, { useState } from 'react';
import { Form, Input, Button, Card, message, Tabs, ConfigProvider, theme } from 'antd';
import { UserOutlined, LockOutlined, MailOutlined, CheckCircleOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import type { AppDispatch } from '../../store';
import { login, register } from '../../store';

const AuthPage: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const dispatch = useDispatch<AppDispatch>();

  const handleLogin = async (values: { username: string; password: string }) => {
    setLoading(true);
    try {
      await dispatch(login(values)).unwrap();
      message.success('登录成功！');
      navigate('/');
    } catch (error: any) {
      message.error(error.error || '登录失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (values: { username: string; email: string; password: string }) => {
    setLoading(true);
    try {
      await dispatch(register(values)).unwrap();
      message.success('注册成功！');
      navigate('/');
    } catch (error: any) {
      message.error(error.error || '注册失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  const loginForm = (
    <Form
      name="login"
      onFinish={handleLogin}
      autoComplete="off"
      size="large"
    >
      <Form.Item
        name="username"
        rules={[{ required: true, message: '请输入用户名！' }]}
      >
        <Input
          prefix={<UserOutlined style={{ color: '#8c8c8c' }} />}
          placeholder="用户名"
          style={{
            borderRadius: 8,
            height: 48,
          }}
        />
      </Form.Item>

      <Form.Item
        name="password"
        rules={[{ required: true, message: '请输入密码！' }]}
      >
        <Input.Password
          prefix={<LockOutlined style={{ color: '#8c8c8c' }} />}
          placeholder="密码"
          style={{
            borderRadius: 8,
            height: 48,
          }}
        />
      </Form.Item>

      <Form.Item>
        <Button
          type="primary"
          htmlType="submit"
          loading={loading}
          block
          style={{
            height: 48,
            borderRadius: 8,
            fontSize: 16,
            fontWeight: 500,
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            border: 'none',
            boxShadow: '0 4px 12px rgba(102, 126, 234, 0.4)',
          }}
        >
          登录
        </Button>
      </Form.Item>
    </Form>
  );

  const registerForm = (
    <Form
      name="register"
      onFinish={handleRegister}
      autoComplete="off"
      size="large"
    >
      <Form.Item
        name="username"
        rules={[
          { required: true, message: '请输入用户名！' },
          { min: 3, message: '用户名至少3个字符' },
        ]}
      >
        <Input
          prefix={<UserOutlined style={{ color: '#8c8c8c' }} />}
          placeholder="用户名"
          style={{
            borderRadius: 8,
            height: 48,
          }}
        />
      </Form.Item>

      <Form.Item
        name="email"
        rules={[
          { required: true, message: '请输入邮箱！' },
          { type: 'email', message: '请输入有效的邮箱地址' },
        ]}
      >
        <Input
          prefix={<MailOutlined style={{ color: '#8c8c8c' }} />}
          placeholder="邮箱"
          style={{
            borderRadius: 8,
            height: 48,
          }}
        />
      </Form.Item>

      <Form.Item
        name="password"
        rules={[
          { required: true, message: '请输入密码！' },
          { min: 6, message: '密码至少6个字符' },
        ]}
      >
        <Input.Password
          prefix={<LockOutlined style={{ color: '#8c8c8c' }} />}
          placeholder="密码"
          style={{
            borderRadius: 8,
            height: 48,
          }}
        />
      </Form.Item>

      <Form.Item>
        <Button
          type="primary"
          htmlType="submit"
          loading={loading}
          block
          style={{
            height: 48,
            borderRadius: 8,
            fontSize: 16,
            fontWeight: 500,
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            border: 'none',
            boxShadow: '0 4px 12px rgba(102, 126, 234, 0.4)',
          }}
        >
          注册
        </Button>
      </Form.Item>
    </Form>
  );

  const items = [
    { key: 'login', label: '登录', children: loginForm },
    { key: 'register', label: '注册', children: registerForm },
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
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)',
        position: 'relative',
        overflow: 'hidden',
      }}>
        <div style={{
          position: 'absolute',
          width: 400,
          height: 400,
          borderRadius: '50%',
          background: 'rgba(255, 255, 255, 0.1)',
          top: -100,
          left: -100,
          filter: 'blur(40px)',
        }} />
        <div style={{
          position: 'absolute',
          width: 300,
          height: 300,
          borderRadius: '50%',
          background: 'rgba(255, 255, 255, 0.1)',
          bottom: -50,
          right: -50,
          filter: 'blur(40px)',
        }} />

        <Card
          style={{
            width: 420,
            boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)',
            borderRadius: 16,
            border: 'none',
            position: 'relative',
            zIndex: 1,
          }}
        >
          <div style={{ textAlign: 'center', marginBottom: 32 }}>
            <div style={{
              width: 64,
              height: 64,
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto 16px',
              boxShadow: '0 8px 24px rgba(102, 126, 234, 0.4)',
            }}>
              <CheckCircleOutlined style={{ fontSize: 32, color: 'white' }} />
            </div>
            <h1 style={{
              fontSize: 28,
              fontWeight: 700,
              marginBottom: 8,
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}>待办事项管理</h1>
            <p style={{ color: '#8c8c8c', fontSize: 14, margin: 0 }}>管理您的日常任务，提升效率</p>
          </div>
          <Tabs
            items={items}
            defaultActiveKey="login"
            centered
            size="large"
            className="auth-tabs"
          />
        </Card>
      </div>
    </ConfigProvider>
  );
};

export default AuthPage;
