<template>
  <Card class="team-widget">
    <template #title>My Team</template>
    <template #content>
      <div
        v-for="member in team"
        :key="member.name"
        class="team-member"
      >
        <img :src="member.avatar" :alt="member.name" class="team-member__avatar" />
        <div class="team-member__info">
          <span class="team-member__name">{{ member.name }}</span>
          <span class="team-member__role">{{ member.role }}</span>
        </div>
        <div class="team-member__stat">
          <span class="team-member__amount">{{ member.usage }}</span>
          <span class="team-member__sublabel">Usage</span>
        </div>
        <div class="team-member__stat">
          <span
            class="team-member__savings"
            :class="member.savings.startsWith('+') ? 'positive' : 'negative'"
          >
            {{ member.savings }}
          </span>
          <span class="team-member__sublabel">Savings</span>
        </div>
      </div>
    </template>
  </Card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Card from 'primevue/card'
import { getTeamMembers } from '@/services/dashboardService'

const team = ref<
  { name: string; role: string; usage: string; savings: string; avatar: string }[]
>([])

onMounted(async () => {
  team.value = await getTeamMembers()
})
</script>

<style scoped src="@/assets/dashboard/TeamWidget.css" />