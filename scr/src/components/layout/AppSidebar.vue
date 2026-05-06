<template>
  <aside class="sidebar">
    <div class="sidebar__logo">
      <img src="/logo.png" alt="GreenLLM" class="sidebar__logo-img" />
      <span class="sidebar__logo-text">GreenLLM</span>
    </div>

    <nav class="sidebar__nav">
      <RouterLink
        v-for="item in visibleNavItems"
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
import { useNavItems } from '@/composables/useNavItems'

const route = useRoute()
const { visibleNavItems } = useNavItems()

function isActive(path: string) {
  return route.path === path
}
</script>

<style scoped src="@/assets/layout/AppSidebar.css" />