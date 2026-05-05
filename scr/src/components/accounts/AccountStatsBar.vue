<template>
  <div class="account-stats">
    <div class="account-stat">
      <span class="account-stat__label">Total Members</span>
      <span class="account-stat__value">{{ stats.totalMembers }}</span>
    </div>
    <div class="account-stat__divider" />
    <div class="account-stat">
      <span class="account-stat__label">Total Budget</span>
      <span class="account-stat__value">{{ stats.totalBudget }}</span>
    </div>
    <div class="account-stat__divider" />
    <div class="account-stat">
      <span class="account-stat__label">Total Spent</span>
      <span class="account-stat__value">{{ stats.totalSpent }}</span>
    </div>
    <div class="account-stat__divider" />
    <div class="account-stat">
      <span class="account-stat__label">Over Budget</span>
      <span class="account-stat__value account-stat__value--danger">
        {{ stats.overBudget }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getAccountsStats } from '@/services/dashboardService'

const stats = ref({
  totalMembers: 0,
  totalBudget: '',
  totalSpent: '',
  overBudget: 0,
})

onMounted(async () => {
  stats.value = await getAccountsStats()
})
</script>

<style scoped src="@/assets/accounts/AccountStatsBar.css" />