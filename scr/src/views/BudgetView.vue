<template>
  <div class="budget">
    <BalanceStats />

    <!-- Top row: Overview chart + Credit Transfer -->
    <div class="budget__top">
      <div class="budget__overview">
        <OverviewChart />
      </div>
      <CreditTransfer />
    </div>

    <RecentUsageTable />
  </div>
</template>

<script setup lang="ts">
import OverviewChart from '@/components/budget/OverviewChart.vue'
import BalanceStats from '@/components/budget/BalanceStats.vue'
import CreditTransfer from '@/components/budget/CreditTransfer.vue'
import RecentUsageTable from '@/components/budget/RecentUsageTable.vue'
</script>

<style scoped src="@/assets/budget/BudgetView.css" />