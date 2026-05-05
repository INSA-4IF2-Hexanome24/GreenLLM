<template>
  <div class="accounts">
    <AccountStatsBar />
    <AccountsTable />
  </div>
</template>

<script setup lang="ts">
import AccountStatsBar from '@/components/accounts/AccountStatsBar.vue'
import AccountsTable from '@/components/accounts/AccountsTable.vue'
</script>

<style scoped src="@/assets/accounts/AccountsView.css" />