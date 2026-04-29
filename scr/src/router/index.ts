// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/user/dashboard',
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
      children: [
        {
          path: 'dashboard',
          component: () => import('@/views/dashboard/DashboardView.vue'),
        },
        {
          path: 'routing',
          component: () => import('@/views/RoutingView.vue'),
        },
        {
          path: 'budget',
          component: () => import('@/views/BudgetView.vue'),
        },
      ],
    },
    {
      path: '/company',
      component: () => import('@/components/layout/AppLayout.vue'),
      children: [
        {
          path: 'dashboard',
          component: () => import('@/views/dashboard/DashboardView.vue'),
        },
      ],
    },
  ],
})

export default router