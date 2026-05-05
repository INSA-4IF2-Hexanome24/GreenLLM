<template>
  <div class="employee-dashboard">
    <StatCards />

    <div class="employee-dashboard__middle">
      <div class="employee-dashboard__section">
        <RoutingWidget />
      </div>
      <div class="employee-dashboard__section">
        <UsageChart />
      </div>
    </div>

    <div class="employee-dashboard__middle">
      <TeamWidget />
      <RecentOperationsWidget />
    </div>
  </div>
</template>

<script setup lang="ts">
import StatCards from '@/components/dashboard/StatCards.vue'
import RoutingWidget from '@/components/routing/RoutingWidget.vue'
import UsageChart from '@/components/dashboard/UsageChart.vue'
import TeamWidget from '@/components/dashboard/TeamWidget.vue'
import RecentOperationsWidget from '@/components/dashboard/RecentOperationsWidget.vue'
</script>

<style scoped src="@/assets/dashboard/EmployeeDashboardView.css" />