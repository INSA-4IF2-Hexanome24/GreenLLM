<template>
  <Card class="dashboard-card">
    <template #title>
      <div class="overview-header">
        <div>
          <span class="overview-title">Overview</span>
          <p class="overview-subtitle">
            <span class="overview-budget">$7,560 Budget</span>
            &amp;
            <span class="overview-expense">$5,420 Expended this month</span>
          </p>
        </div>
      </div>
    </template>
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
import { getOverviewChart } from '@/services/dashboardService'

const chartData = ref({})

const chartOptions = {
  plugins: {
    legend: {
      position: 'top',
      align: 'end',
      labels: { usePointStyle: true, pointStyle: 'circle' },
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: { color: '#f1f5f9' },
      ticks: {
        callback: (v: number) => `$${(v / 1000).toFixed(0)},000`,
      },
    },
    x: { grid: { display: false } },
  },
  responsive: true,
  maintainAspectRatio: false,
}

onMounted(async () => {
  const data = await getOverviewChart()
  chartData.value = {
    labels: data.labels,
    datasets: [
      {
        label: 'Expense',
        data: data.expense,
        backgroundColor: '#DEFE65',
        borderRadius: 6,
      },
      {
        label: 'Budget',
        data: data.budget,
        backgroundColor: '#343C6A',
        borderRadius: 6,
      },
    ],
  }
})
</script>

<style scoped src="@/assets/budget/OverviewChart.css" />