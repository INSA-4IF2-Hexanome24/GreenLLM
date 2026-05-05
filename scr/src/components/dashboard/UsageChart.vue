<template>
  <Card>
    <template #title>
      <div class="inference-header">
        <span>Usage Per Month</span>
      </div>
    </template>
    <template #content>
      <Chart
        type="line"
        :data="chartData"
        :options="chartOptions"
        style="height: 180px"
      />
    </template>
  </Card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Card from 'primevue/card'
import Chart from 'primevue/chart'
import { getMonthlyUsage } from '@/services/dashboardService'

const chartData = ref({})

const chartOptions = {
  plugins: { legend: { display: false } },
  scales: {
    y: {
      beginAtZero: true,
      grid: { color: '#f1f5f9' },
      ticks: {
        callback: (v: number) => `$${(v / 1000).toFixed(0)}k`,
      },
    },
    x: { grid: { display: false } },
  },
  elements: {
    line: { tension: 0.4 },
    point: { radius: 4, backgroundColor: '#ffffff', borderColor: '#a3e635' },
  },
  responsive: true,
  maintainAspectRatio: false,
}

onMounted(async () => {
  const data = await getMonthlyUsage()
  chartData.value = {
    labels: data.labels,
    datasets: [
      {
        data: data.credits,
        borderColor: '#a3e635',
        backgroundColor: 'rgba(163, 230, 53, 0.1)',
        fill: true,
        pointBackgroundColor: '#ffffff',
        pointBorderColor: '#a3e635',
      },
    ],
  }
})
</script>

<style scoped src="@/assets/dashboard/InferenceUsageChart.css" />