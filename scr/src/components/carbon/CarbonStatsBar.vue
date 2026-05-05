<template>
  <div class="carbon-stats">
    <Card
      v-for="stat in stats"
      :key="stat.label"
      class="dashboard-card carbon-stat"
    >
      <template #content>
        <div class="carbon-stat__inner">
          <div class="carbon-stat__icon">
            <i :class="stat.icon" />
          </div>
          <div class="carbon-stat__body">
            <span class="carbon-stat__label">{{ stat.label }}</span>
            <span class="carbon-stat__value">{{ stat.value }}</span>
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Card from 'primevue/card'
import { getCarbonStats } from '@/services/dashboardService'

const stats = ref<{ label: string; value: string; icon: string }[]>([])

onMounted(async () => {
  stats.value = await getCarbonStats()
})
</script>

<style scoped src="@/assets/carbon/CarbonStatsBar.css" />