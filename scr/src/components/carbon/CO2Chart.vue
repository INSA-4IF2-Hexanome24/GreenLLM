<template>
  <Card class="dashboard-card">
    <template #title>{{ title }}</template>
    <template #content>
      <Chart
        :type="type"
        :data="chartData"
        :options="resolvedOptions"
        style="height: 220px"
      />
    </template>
  </Card>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Card from 'primevue/card'
import Chart from 'primevue/chart'

const props = defineProps<{
  title: string
  type: 'bar' | 'line' | 'pie' | 'doughnut'
  fetchData: () => Promise<any>
  buildLabels: (data: any) => string[]
  buildDatasets: (data: any) => object[]
  options?: object
}>()

const chartData = ref({})

const defaultOptions = computed(() => {
  const isRound = props.type === 'pie' || props.type === 'doughnut'
  return {
    plugins: {
      legend: {
        position: isRound ? 'bottom' : 'top',
        labels: { usePointStyle: true, pointStyle: 'circle' },
      },
    },
    ...(isRound
      ? {}
      : {
          scales: {
            y: {
              beginAtZero: true,
              grid: { color: '#f1f5f9' },
              ticks: {
                callback: (v: number) => `${v}Kg`,
              },
            },
            x: { grid: { display: false } },
          },
        }),
    responsive: true,
    maintainAspectRatio: false,
  }
})

const resolvedOptions = computed(() => ({
  ...defaultOptions.value,
  ...props.options,
}))

onMounted(async () => {
  const data = await props.fetchData()
  chartData.value = {
    labels: props.buildLabels(data),
    datasets: props.buildDatasets(data),
  }
})
</script>