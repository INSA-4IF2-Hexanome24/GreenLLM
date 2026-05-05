<template>
  <Card class="routing-widget-card">
    <template #content>
      <div class="routing-tabs">
        <button
          :class="['routing-tab', { 'routing-tab--active': mode === 'router' }]"
          @click="mode = 'router'"
        >
          ROUTER MODE
        </button>
        <button
          :class="['routing-tab', { 'routing-tab--active': mode === 'chat' }]"
          @click="mode = 'chat'"
        >
          CHAT MODE
        </button>
        <div class="routing-quota">
          <span>Quota remaining: {{ quota.remaining.toLocaleString() }}</span>
          <i class="pi pi-circle-fill routing-quota__dot" />
        </div>
      </div>

      <Divider class="routing-divider" />

      <Textarea
        v-model="prompt"
        :placeholder="
          mode === 'router'
            ? 'Enter your prompt here...'
            : 'Chat with the model...'
        "
        class="routing-textarea"
        :autoResize="false"
        rows="4"
      />

      <div class="routing-bar">
        <div class="routing-bar__left">
          <span class="routing-mode-badge">
            <i class="pi pi-circle-fill routing-mode-badge__dot" />
            Carbon Routing
          </span>
          <Button
            label="Settings"
            text
            size="small"
            icon="pi pi-cog"
            class="routing-settings-btn"
          />
        </div>
        <div class="routing-bar__right">
          <span class="routing-char-count">{{ prompt.length }} / 5000</span>
          <Button
            label="Choose Model"
            class="routing-submit-btn"
            :disabled="prompt.trim().length === 0"
            @click="handleSubmit"
          />
        </div>
      </div>
    </template>
  </Card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Button from 'primevue/button'
import Divider from 'primevue/divider'
import Textarea from 'primevue/textarea'
import Card from 'primevue/card'
import { getQuota } from '@/services/routingService'
import { useRoutingStore } from '@/stores/routing'

const router = useRouter()
const routingStore = useRoutingStore()

const mode = ref<'router' | 'chat'>('router')
const prompt = ref('')
const quota = ref({ remaining: 10000, total: 10000 })

onMounted(async () => {
  quota.value = await getQuota()
})

function handleSubmit() {
  routingStore.setPrompt(prompt.value)
  router.push('/user/routing')
}
</script>

<style scoped src="@/assets/routing/RoutingView.css" />