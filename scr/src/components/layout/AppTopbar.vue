<template>
  <header class="topbar">
    <!-- Page Title -->
    <h2 class="topbar__title">{{ pageTitle }}</h2>

    <!-- Right side -->
    <div class="topbar__right">
      <!-- Search -->
      <IconField>
        <InputIcon class="pi pi-search" />
        <InputText placeholder="Search for something" class="topbar__search" />
      </IconField>

      <!-- Settings -->
      <Button
        icon="pi pi-cog"
        text
        rounded
        class="topbar__icon-btn"
      />

      <!-- Notifications -->
      <Button
        icon="pi pi-bell"
        text
        rounded
        class="topbar__icon-btn"
      />

      <!-- Avatar -->
      <Avatar
        image="https://i.pravatar.cc/150?img=5"
        shape="circle"
        size="normal"
        class="topbar__avatar"
      />
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Avatar from 'primevue/avatar'
import Button from 'primevue/button'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'

const route = useRoute()

const pageTitles: Record<string, string> = {
  '/user/dashboard': 'Dashboard',
  '/user/routing': 'Routing',
  '/user/accounts': 'Accounts',
  '/user/budget': 'Budget',
  '/user/reports': 'Reports',
  '/user/carbon': 'Carbon',
  '/user/models': 'Models',
  '/user/settings': 'Settings',
}

const pageTitle = computed(() => pageTitles[route.path] ?? 'Dashboard')
</script>

<style scoped src="@/assets/layout/AppTopbar.css" />