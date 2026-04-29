<template>
  <Card class="dashboard-card">
    <template #title>Recent Usages</template>
    <template #content>
      <div class="recent-list">
        <div
          v-for="usage in recentUsages"
          :key="usage.id"
          class="recent-item"
        >
          <Avatar :label="usage.icon" shape="circle" size="normal" />
          <div class="recent-item__info">
            <span class="recent-item__name">{{ usage.name }}</span>
            <span class="recent-item__date">{{ usage.date }}</span>
          </div>
          <Tag
            :value="`${usage.amount < 0 ? '-' : '+'}$${Math.abs(usage.amount).toLocaleString()}`"
            :severity="usage.amount < 0 ? 'danger' : 'success'"
          />
        </div>
      </div>
    </template>
  </Card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Card from 'primevue/card'
import Avatar from 'primevue/avatar'
import Tag from 'primevue/tag'
import { getRecentUsages } from '@/services/dashboardService'

const recentUsages = ref<any[]>([])
onMounted(async () => {
  recentUsages.value = await getRecentUsages()
})
</script>

<style scoped src="@/assets/dashboard/RecentUsages.css" />