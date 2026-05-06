import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

export const allNavItems = [
  { label: 'Dashboard', icon: 'pi pi-home',         path: '/user/dashboard', roles: ['admin', 'employee'] },
  { label: 'Routing',   icon: 'pi pi-map',           path: '/user/routing',   roles: ['admin', 'employee'] },
  { label: 'Accounts',  icon: 'pi pi-user',          path: '/user/accounts',  roles: ['admin'] },
  { label: 'Budget',    icon: 'pi pi-wallet',        path: '/user/budget',    roles: ['admin'] },
  { label: 'Reports',   icon: 'pi pi-chart-bar',     path: '/user/reports',   roles: ['admin'] },
  { label: 'Carbon',    icon: 'pi pi-globe',         path: '/user/carbon',    roles: ['admin', 'employee'] },
  { label: 'Models',    icon: 'pi pi-microchip-ai',  path: '/user/models',    roles: ['admin', 'employee'] },
  { label: 'Settings',  icon: 'pi pi-cog',           path: '/user/settings',  roles: ['admin', 'employee'] },
]

export function useNavItems() {
  const auth = useAuthStore()

  const visibleNavItems = computed(() => {
    const role = auth.currentUser?.role ?? 'employee'
    return allNavItems.filter((item) => item.roles.includes(role))
  })

  return { visibleNavItems }
}