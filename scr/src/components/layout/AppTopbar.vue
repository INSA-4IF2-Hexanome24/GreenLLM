<template>
  <header class="topbar">
    <h2 class="topbar__title">{{ pageTitle }}</h2>

    <div class="topbar__right">
      <!-- Search -->
      <div class="topbar__search-wrap" ref="searchWrapRef">
        <IconField>
          <InputIcon class="pi pi-search" />
          <InputText
            v-model="searchQuery"
            placeholder="Search for something"
            class="topbar__search"
            @focus="showResults = true"
            @input="showResults = true"
          />
        </IconField>
        <div v-if="showResults && filteredRoutes.length" class="topbar__search-results">
          <button
            v-for="item in filteredRoutes"
            :key="item.path"
            class="topbar__search-item"
            @click="navigateTo(item.path)"
          >
            <i :class="item.icon" class="topbar__search-item-icon" />
            <span>{{ item.label }}</span>
          </button>
        </div>
        <div v-else-if="showResults && searchQuery.length > 0" class="topbar__search-results">
          <span class="topbar__search-empty">No results found</span>
        </div>
      </div>

      <!-- Settings -->
      <Button
        icon="pi pi-cog"
        text
        rounded
        class="topbar__icon-btn"
        :class="{ 'topbar__icon-btn--active': route.path === '/user/settings' }"
        @click="router.push('/user/settings')"
      />

      <!-- Notifications -->
      <Button
        icon="pi pi-bell"
        text
        rounded
        class="topbar__icon-btn"
        @click="router.push('/user/settings')"
      />

      <!-- Avatar -->
      <Avatar
        image="/ProfilePic.png"
        shape="circle"
        size="normal"
        class="topbar__avatar"
      />
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Avatar from 'primevue/avatar'
import Button from 'primevue/button'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'
import { useNavItems } from '@/composables/useNavItems'

const route = useRoute()
const router = useRouter()

const pageTitles: Record<string, string> = {
  '/user/dashboard': 'Dashboard',
  '/user/routing':   'Routing',
  '/user/accounts':  'Accounts',
  '/user/budget':    'Budget',
  '/user/reports':   'Reports',
  '/user/carbon':    'Carbon',
  '/user/models':    'Models',
  '/user/settings':  'Settings',
}

const { visibleNavItems } = useNavItems()

const pageTitle = computed(() => pageTitles[route.path] ?? 'Dashboard')

const searchQuery = ref('')
const showResults = ref(false)
const searchWrapRef = ref<HTMLElement | null>(null)

const filteredRoutes = computed(() => {
  if (!searchQuery.value.trim()) return visibleNavItems.value
  const q = searchQuery.value.toLowerCase()
  return visibleNavItems.value.filter((r) => r.label.toLowerCase().includes(q))
})

function navigateTo(path: string) {
  router.push(path)
  searchQuery.value = ''
  showResults.value = false
}

function handleClickOutside(e: MouseEvent) {
  if (searchWrapRef.value && !searchWrapRef.value.contains(e.target as Node)) {
    showResults.value = false
  }
}

onMounted(() => document.addEventListener('click', handleClickOutside))
onUnmounted(() => document.removeEventListener('click', handleClickOutside))
</script>

<style scoped src="@/assets/layout/AppTopbar.css" />