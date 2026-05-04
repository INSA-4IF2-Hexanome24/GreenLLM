<template>
  <div class="dashboard">
    <div class="dashboard__grid">
      <InferenceUsageChart class="area-inference" />
      <RecentUsages class="area-recent" />
      <WeeklyCO2Chart class="area-co2" />
      <ExpenseStatistics class="area-expense" />
<!--       <CreditTransfer class="area-credit" />
      <BudgetCards class="area-budget" /> -->
    </div>
  </div>
</template>

<script setup lang="ts">
//import BudgetCards from '@/components/dashboard/BudgetCards.vue'
import RecentUsages from '@/components/dashboard/RecentUsages.vue'
import WeeklyCO2Chart from '@/components/dashboard/WeeklyCO2Chart.vue'
import ExpenseStatistics from '@/components/dashboard/ExpenseStatistics.vue'
//import CreditTransfer from '@/components/dashboard/CreditTransfer.vue'
import InferenceUsageChart from '@/components/dashboard/InferenceUsageChart.vue'
</script>

<style scoped src="@/assets/dashboard/DashboardView.css" />