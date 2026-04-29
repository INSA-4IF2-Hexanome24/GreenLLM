<template>
  <div class="dashboard">
    <h1 class="dashboard__title">Overview</h1>
    <div class="dashboard__grid">
      <BudgetCards class="area-budget" />
      <RecentUsages class="area-recent" />
      <WeeklyCO2Chart class="area-co2" />
      <ExpenseStatistics class="area-expense" />
      <CreditTransfer class="area-credit" />
      <InferenceUsageChart class="area-inference" />
    </div>
  </div>
</template>

<script setup lang="ts">
import BudgetCards from '@/components/dashboard/BudgetCards.vue'
import RecentUsages from '@/components/dashboard/RecentUsages.vue'
import WeeklyCO2Chart from '@/components/dashboard/WeeklyCO2Chart.vue'
import ExpenseStatistics from '@/components/dashboard/ExpenseStatistics.vue'
import CreditTransfer from '@/components/dashboard/CreditTransfer.vue'
import InferenceUsageChart from '@/components/dashboard/InferenceUsageChart.vue'
</script>

<style scoped src="@/assets/dashboard/DashboardView.css" />