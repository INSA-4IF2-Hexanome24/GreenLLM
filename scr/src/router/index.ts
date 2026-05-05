// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/login',
    },
    {
      path: '/login',
      component: () => import('@/views/auth/LoginView.vue'),
    },
    {
      path: '/register',
      component: () => import('@/views/auth/RegisterView.vue'),
    },
    {
      path: '/user',
      component: () => import('@/components/layout/AppLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        {
            path: 'dashboard',
            redirect: () => {
              const auth = useAuthStore()
              return auth.currentUser?.role === 'admin'
                ? '/user/dashboard/admin'
                : '/user/dashboard/employee'
            },
          },
        {
          path: 'dashboard/admin',
          component: () => import('@/views/dashboard/DashboardView.vue'),
          meta: { requiresAuth: true, role: 'admin' },
        },
        {
          path: 'dashboard/employee',
          component: () => import('@/views/dashboard/DashboardViewEMP.vue'),
          meta: { requiresAuth: true, role: 'employee' },
        },
        { path: 'routing',  component: () => import('@/views/RoutingView.vue') },
        { path: 'accounts', component: () => import('@/views/AccountsView.vue') },
        { path: 'budget',   component: () => import('@/views/BudgetView.vue') },
        { path: 'reports',  component: () => import('@/views/ReportsView.vue') },
        { path: 'carbon',   component: () => import('@/views/CarbonView.vue') },
        { path: 'models',   component: () => import('@/views/ModelsView.vue') },
        { path: 'settings', component: () => import('@/views/SettingsView.vue') },
      ],
    },
  ],
})

router.beforeEach((to) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return '/login'
  }

  if (to.meta.role === 'admin' && auth.currentUser?.role !== 'admin') {
    return '/user/dashboard'
  }
})

export default router