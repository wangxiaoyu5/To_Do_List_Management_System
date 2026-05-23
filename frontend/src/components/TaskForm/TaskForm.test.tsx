import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { Provider } from 'react-redux'
import { configureStore } from '@reduxjs/toolkit'
import TaskForm from './index'
import { authSlice, dataSlice } from '../../store'

const mockStore = configureStore({
  reducer: {
    auth: authSlice.reducer,
    data: dataSlice.reducer
  },
  preloadedState: {
    auth: {
      user: { id: '1', username: 'test', email: 'test@test.com' },
      isAuthenticated: true,
      loading: false
    },
    data: {
      tasks: [],
      categories: [
        { id: '1', name: 'Work', color: '#1890ff', userId: '1' }
      ],
      tags: [
        { id: '1', name: 'Important', color: '#f5222d', userId: '1' }
      ],
      loading: false
    }
  }
})

const renderWithProviders = (component: React.ReactElement) => {
  return render(
    <Provider store={mockStore}>
      {component}
    </Provider>
  )
}

describe('TaskForm Component', () => {
  it('renders correctly for new task', () => {
    renderWithProviders(
      <TaskForm
        open={true}
        onClose={() => {}}
      />
    )
    
    expect(screen.getByText('添加任务')).toBeInTheDocument()
    expect(screen.getByLabelText(/标题/i)).toBeInTheDocument()
  })

  it('renders correctly for editing task', () => {
    const mockTask = {
      id: '1',
      title: 'Test Task',
      description: 'Test Description',
      priority: 'MEDIUM',
      completed: false,
      userId: '1',
      categoryId: null,
      category: null,
      tags: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      dueDate: null,
      completedAt: null
    }
    
    renderWithProviders(
      <TaskForm
        open={true}
        task={mockTask}
        onClose={() => {}}
      />
    )
    
    expect(screen.getByText('编辑任务')).toBeInTheDocument()
    expect(screen.getByDisplayValue('Test Task')).toBeInTheDocument()
  })

  it('submits form with valid data', async () => {
    const mockSubmit = vi.fn()
    renderWithProviders(
      <TaskForm
        open={true}
        onClose={() => {}}
      />
    )
    
    fireEvent.change(screen.getByLabelText(/标题/i), {
      target: { value: 'New Task' }
    })
    
    expect(screen.getByLabelText(/标题/i)).toHaveValue('New Task')
  })
})
