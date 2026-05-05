<template>
  <Card class="dashboard-card">
    <template #title>
      <div class="usage-header">
        <span>Recent Usage</span>
        <div class="usage-tabs">
          <button
            v-for="tab in tabs"
            :key="tab.value"
            class="usage-tab"
            :class="{ 'usage-tab--active': activeTab === tab.value }"
            @click="activeTab = tab.value"
          >
            {{ tab.label }}
          </button>
        </div>
      </div>
    </template>
    <template #content>
      <table class="usage-table">
        <thead>
          <tr>
            <th>Description</th>
            <th>Transaction ID</th>
            <th>Owner</th>
            <th>Card</th>
            <th>Date</th>
            <th>Amount</th>
            <th>Receipt</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="tx in filteredTransactions" :key="tx.id">
            <td class="usage-table__desc">
              <span
                class="usage-table__arrow"
                :class="tx.amount > 0 ? 'up' : 'down'"
              >
                <i :class="tx.amount > 0 ? 'pi pi-arrow-up' : 'pi pi-arrow-down'" />
              </span>
              {{ tx.description }}
            </td>
            <td class="usage-table__muted">{{ tx.transactionId }}</td>
            <td>{{ tx.owner }}</td>
            <td class="usage-table__muted">{{ tx.card }}</td>
            <td class="usage-table__muted">{{ tx.date }}</td>
            <td :class="tx.amount > 0 ? 'positive' : 'negative'">
              {{ tx.amount > 0 ? '+' : '' }}${{ tx.amount.toFixed(3) }}
            </td>
            <td>
              <Button label="Download" outlined rounded size="small" />
            </td>
          </tr>
        </tbody>
      </table>
    </template>
  </Card>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Card from 'primevue/card'
import Button from 'primevue/button'
import { getRecentTransactions } from '@/services/dashboardService'

const tabs = [
  { label: 'All Usages',      value: 'all'       },
  { label: 'Most Expensive',  value: 'expensive' },
  { label: 'This Month',      value: 'month'     },
]

const activeTab = ref('all')
const transactions = ref<any[]>([])

onMounted(async () => {
  transactions.value = await getRecentTransactions()
})

const filteredTransactions = computed(() => {
  if (activeTab.value === 'expensive') {
    return [...transactions.value].sort((a, b) => a.amount - b.amount)
  }
  if (activeTab.value === 'month') {
    // Mock: just return first 3 as "this month"
    return transactions.value.slice(0, 3)
  }
  return transactions.value
})
</script>

<style scoped src="@/assets/budget/RecentUsageTable.css" />