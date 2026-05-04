<template>
  <Card class="dashboard-card">
    <template #title>Expense Statistics</template>
    <template #content>
      <div class="expense-wrapper">
        <Chart
          type="pie"
          :data="chartData"
          :options="chartOptions"
          style="height: 160px"
        />
        <div class="expense-legend">
          <div
            v-for="item in expenses"
            :key="item.label"
            class="legend-item"
          >
            <span
              class="legend-dot"
              :style="{ backgroundColor: item.color }"
            />
            <span class="legend-label">{{ item.label }}</span>
            <span class="legend-value">{{ item.value }}%</span>
          </div>
        </div>
      </div>
    </template>
  </Card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Card from 'primevue/card'
import Chart from 'primevue/chart'
import { getExpenseStatistics } from '@/services/dashboardService'

const expenses = ref<any[]>([])
const chartData = ref({})
const chartOptions = {
  plugins: {
    legend: { display: false },
  },
  responsive: true,
  maintainAspectRatio: false,
}

onMounted(async () => {
  expenses.value = await getExpenseStatistics()
  chartData.value = {
    labels: expenses.value.map((e) => e.label),
    datasets: [
      {
        data: expenses.value.map((e) => e.value),
        backgroundColor: expenses.value.map((e) => e.color),
        borderWidth: 0,
      },
    ],
  }
})
</script>

<style scoped src="@/assets/dashboard/ExpenseStatistics.css" />