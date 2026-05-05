<template>
  <Card class="dashboard-card">
    <template #title>{{ title }}</template>
    <template #content>
      <ul class="top-users">
        <li
          v-for="user in users"
          :key="user.name"
          class="top-users__item"
        >
          <img
            :src="user.avatar"
            :alt="user.name"
            class="top-users__avatar"
          />
          <div class="top-users__info">
            <span class="top-users__name">{{ user.name }}</span>
            <span class="top-users__time">{{ user.time }}</span>
          </div>
          <span class="top-users__value">{{ user.value }} kgCO2e</span>
        </li>
      </ul>
    </template>
  </Card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Card from 'primevue/card'

const props = defineProps<{
  title: string
  fetchData: () => Promise<
    { name: string; time: string; value: number; avatar: string }[]
  >
}>()

const users = ref<
  { name: string; time: string; value: number; avatar: string }[]
>([])

onMounted(async () => {
  users.value = await props.fetchData()
})
</script>

<style scoped src="@/assets/carbon/TopUsersList.css" />