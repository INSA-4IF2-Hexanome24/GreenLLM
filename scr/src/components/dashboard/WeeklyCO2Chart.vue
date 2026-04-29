<template>
  <Card class="dashboard-card">
    <template #title>Weekly CO2 Savings</template>
    <template #content>
      <Chart
        type="bar"
        :data="chartData"
        :options="chartOptions"
        style="height: 220px"
      />
    </template>
  </Card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Card from 'primevue/card'
import Chart from 'primevue/chart'
import { getWeeklyCO2 } from '@/services/dashboardService'

const chartData = ref({})
const chartOptions = {
  plugins: { legend: { position: 'top' } },
  scales: { y: { beginAtZero: true } },
  responsive: true,
  maintainAspectRatio: false,
}

onMounted(async () => {
  const co2 = await getWeeklyCO2()
  chartData.value = {
    labels: co2.labels,
    datasets: [
      {
        label: 'Actually Used',
        data: co2.actualUsed,
        backgroundColor: '#22d3ee',
        borderRadius: 6,
      },
      {
        label: 'Estimated Use',
        data: co2.estimatedUse,
        backgroundColor: '#3b82f6',
        borderRadius: 6,
      },
    ],
  }
})
</script>