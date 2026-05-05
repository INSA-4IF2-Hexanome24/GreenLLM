<template>
  <Card>
    <template #title>Recent Operations</template>
    <template #content>
      <div class="ops-table">
        <div class="ops-table__header">
          <span>Model</span>
          <span>Name</span>
          <span>Price</span>
          <span>CO2 Saved</span>
        </div>
        <div
          v-for="op in operations"
          :key="op.model + op.name"
          class="ops-table__row"
        >
          <span>{{ op.model }}</span>
          <span>{{ op.name }}</span>
          <span>{{ op.price }}</span>
          <span :class="op.co2.startsWith('+') ? 'positive' : 'negative'">
            {{ op.co2 }}
          </span>
        </div>
      </div>
    </template>
  </Card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Card from 'primevue/card'
import { getRecentOperations } from '@/services/dashboardService'

const operations = ref<
  { model: string; name: string; price: string; co2: string }[]
>([])

onMounted(async () => {
  operations.value = await getRecentOperations()
})
</script>

<style scoped src="@/assets/dashboard/RecentOperationsWidget.css" />