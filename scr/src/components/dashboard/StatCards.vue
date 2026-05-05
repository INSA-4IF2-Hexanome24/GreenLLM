<template>
  <div class="stat-cards">
    <Card v-for="stat in stats" :key="stat.label" class="stat-card">
      <template #content>
        <div class="stat-card__inner">
          <div class="stat-card__icon">
            <i :class="stat.icon" />
          </div>
          <div class="stat-card__body">
            <span class="stat-card__label">{{ stat.label }}</span>
            <span class="stat-card__value">{{ stat.value }}</span>
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import Card from 'primevue/card'
import { getEmployeeStats } from '@/services/dashboardService'

const stats = ref<{ label: string; value: string; icon: string }[]>([])

onMounted(async () => {
  stats.value = await getEmployeeStats()
})
</script>

<style scoped src="@/assets/dashboard/StatCards.css" />