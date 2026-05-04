<template>
  <Card class="dashboard-card">
    <template #title>
      <div class="card-header">
        <span>My Budgets</span>
        <Button label="See All" link size="small" />
      </div>
    </template>
    <template #content>
      <div class="budget-grid">
        <div
          v-for="budget in budgets"
          :key="budget.id"
          :class="['budget-item', { 'budget-item--active': budget.active }]"
        >
          <div class="budget-item__top">
            <span>Balance</span>
            <span>VALID THRU {{ budget.validThru }}</span>
          </div>
          <div class="budget-item__balance">
            ${{ budget.balance.toLocaleString() }}
          </div>
          <div class="budget-item__holder">
            CARD HOLDER: {{ budget.cardHolder }}
          </div>
        </div>
      </div>
    </template>
  </Card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Card from 'primevue/card'
import Button from 'primevue/button'
import { getBudgets } from '@/services/dashboardService'

const budgets = ref<any[]>([])
onMounted(async () => {
  budgets.value = await getBudgets()
})
</script>

<style scoped src="@/assets/dashboard/BudgetCards.css" />