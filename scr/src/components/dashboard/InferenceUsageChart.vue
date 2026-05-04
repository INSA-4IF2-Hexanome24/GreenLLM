<template>
  <Card class="dashboard-card">
    <template #title>
      <div class="inference-header">
        <span>Inference Usage (Credits)</span>
        <div class="inference-stats">
          <Chip :label="`Total: ${totalCredits.toLocaleString()}`" />
        </div>
      </div>
    </template>
    <template #content>
      <Chart
        type="line"
        :data="chartData"
        :options="chartOptions"
        style="height: 160px"
      />
    </template>
  </Card>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Card from 'primevue/card'
import Chart from 'primevue/chart'
import Chip from 'primevue/chip'
import { getInferenceUsage } from '@/services/dashboardService'

const rawData = ref<{ labels: string[]; credits: number[] }>({
  labels: [],
  credits: [],
})
const chartData = ref({})

const totalCredits = computed(() =>
  rawData.value.credits.reduce((a, b) => a + b, 0),
)

const chartOptions = {
  plugins: {
    legend: { display: false },
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: { color: '#f1f5f9' },
    },
    x: {
      grid: { display: false },
    },
  },
  elements: {
    line: { tension: 0.4 },
    point: { radius: 3 },
  },
  responsive: true,
  maintainAspectRatio: false,
}

onMounted(async () => {
  rawData.value = await getInferenceUsage()
  chartData.value = {
    labels: rawData.value.labels,
    datasets: [
      {
        data: rawData.value.credits,
        borderColor: '#5D9628',
        backgroundColor: 'rgba(222, 254, 101, 0.15)',
        fill: true,
        pointBackgroundColor: '#5D9628',
      },
    ],
  }
})
</script>

<style scoped src="@/assets/dashboard/InferenceUsageChart.css" />