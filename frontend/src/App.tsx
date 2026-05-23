import React, { useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import type { RootState, AppDispatch } from './store';
import { fetchCurrentUser } from './store';
import AuthPage from './pages/Auth';
import MainPage from './pages/Main';

const App: React.FC = () => {
  const { isAuthenticated, loading } = useSelector((state: RootState) => state.auth);
  const dispatch = useDispatch<AppDispatch>();

  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    if (token && !isAuthenticated) {
      dispatch(fetchCurrentUser());
    }
  }, [dispatch, isAuthenticated]);

  // 如果还在加载但没有token，直接显示登录页面
  if (loading && !localStorage.getItem('accessToken')) {
    return <AuthPage />;
  }

  if (loading) {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
      }}>
        加载中...
      </div>
    );
  }

  return (
    <Routes>
      <Route path="/login" element={!isAuthenticated ? <AuthPage /> : <Navigate to="/" />} />
      <Route path="/*" element={isAuthenticated ? <MainPage /> : <Navigate to="/login" />} />
    </Routes>
  );
};

export default App;
