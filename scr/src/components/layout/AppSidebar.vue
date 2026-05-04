<template>
  <aside class="sidebar">
    <!-- Logo -->
    <div class="sidebar__logo">
      <img src="/logo.png" alt="GreenLLM" class="sidebar__logo-img" />
      <span class="sidebar__logo-text">GreenLLM</span>
    </div>

    <!-- Nav Items -->
    <nav class="sidebar__nav">
      <RouterLink
        v-for="item in navItems"
        :key="item.path"
        :to="item.path"
        class="sidebar__item"
        :class="{ 'sidebar__item--active': isActive(item.path) }"
      >
        <i :class="['sidebar__icon', item.icon]" />
        <span class="sidebar__label">{{ item.label }}</span>
      </RouterLink>
    </nav>
  </aside>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()

const navItems = [
  { label: 'Dashboard', icon: 'pi pi-home', path: '/user/dashboard' },
  { label: 'Routing', icon: 'pi pi-map', path: '/user/routing' },
  { label: 'Accounts', icon: 'pi pi-user', path: '/user/accounts' },
  { label: 'Budget', icon: 'pi pi-wallet', path: '/user/budget' },
  { label: 'Reports', icon: 'pi pi-chart-bar', path: '/user/reports' },
  { label: 'Carbon', icon: 'pi pi-globe', path: '/user/carbon' },
  { label: 'Models', icon: 'pi pi-wrench', path: '/user/models' },
  { label: 'Settings', icon: 'pi pi-cog', path: '/user/settings' },
]

function isActive(path: string) {
  return route.path === path
}
</script>

<style scoped src="@/assets/layout/AppSidebar.css" />