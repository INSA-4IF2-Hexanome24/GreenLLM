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
  { path: 'dashboard', component: () => import('@/views/dashboard/DashboardView.vue') },
  { path: 'routing', component: () => import('@/views/RoutingView.vue') },
  { path: 'accounts', component: () => import('@/views/AccountsView.vue') },
  { path: 'budget', component: () => import('@/views/BudgetView.vue') },
  { path: 'reports', component: () => import('@/views/ReportsView.vue') },
  { path: 'carbon', component: () => import('@/views/CarbonView.vue') },
  { path: 'models', component: () => import('@/views/ModelsView.vue') },
  { path: 'settings', component: () => import('@/views/SettingsView.vue') },
      ],
    },
  ],
})

// Navigation guard
router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return '/login'
  }
})

export default router