<template>
  <div class="balance-stats">
    <Card
      v-for="stat in stats"
      :key="stat.label"
      class="dashboard-card balance-stat"
    >
      <template #content>
        <div class="balance-stat__inner">
          <div class="balance-stat__icon">
            <i :class="stat.icon" />
          </div>
          <div class="balance-stat__body">
            <span class="balance-stat__label">{{ stat.label }}</span>
            <span class="balance-stat__value">{{ stat.value }}</span>
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Card from 'primevue/card'
import { getBalanceStats } from '@/services/dashboardService'

const stats = ref<{ label: string; value: string; icon: string }[]>([])

onMounted(async () => {
  stats.value = await getBalanceStats()
})
</script>

<style scoped src="@/assets/budget/BalanceStats.css" />