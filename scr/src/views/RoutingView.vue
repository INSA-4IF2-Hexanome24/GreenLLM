<!-- src/views/RoutingView.vue -->
<template>
  <div class="routing">
    <div class="routing-card">
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
        rows="5"
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
            :loading="loading"
            :disabled="prompt.trim().length === 0"
            @click="handleSubmit"
          />
        </div>
      </div>
    </div>

    <div v-if="models.length > 0" class="routing-results">
      <h2 class="routing-results__title">Results</h2>
      <div class="routing-results__list">
        <div v-for="model in models" :key="model.id" class="model-card">
          <div class="model-card__identity">
            <img
              :src="model.icon"
              :alt="model.name"
              class="model-card__icon"
              @error="onImgError"
            />
            <div class="model-card__info">
              <span class="model-card__name">{{ model.name }}</span>
              <span class="model-card__tag">{{ model.tag }}</span>
            </div>
          </div>
          <div class="model-card__stat">
            <span class="model-card__stat-label">CO2</span>
            <span class="model-card__stat-value">{{ model.co2 }}kg</span>
          </div>
          <div class="model-card__stat">
            <span class="model-card__stat-label">Power</span>
            <span
              :class="[
                'model-card__stat-value',
                `model-card__stat-value--${model.power.toLowerCase()}`,
              ]"
              >{{ model.power }}</span
            >
          </div>
          <div class="model-card__stat">
            <span class="model-card__stat-label">Cost</span>
            <span class="model-card__stat-value model-card__stat-value--cost">
              {{ model.cost }}$
            </span>
          </div>
          <Button
            label="Use"
            outlined
            rounded
            class="model-card__btn"
            :loading="usingModelId === model.id"
            @click="handleUseModel(model)"
          />
        </div>
      </div>
    </div>

    <!-- Web Search Results -->
  <div v-if="webSearch" class="routing-results">
    <h2 class="routing-results__title">
      <i class="pi pi-globe" style="margin-right: 0.5rem" />
      Web Search Results
    </h2>
    <p class="routing-results__subtitle">
      This query was answered directly from the web.
    </p>
    <div class="routing-results__list">
      <div
        v-for="(answer, index) in webAnswers"
        :key="index"
        class="web-answer-card"
      >
        <p class="web-answer-card__text">{{ answer.answer }}</p>
        <a
          :href="answer.source"
          target="_blank"
          rel="noopener noreferrer"
          class="web-answer-card__source"
        >
          <i class="pi pi-external-link" />
          {{ answer.source }}
        </a>
      </div>
    </div>
  </div>

    <!-- Response Dialog -->
    <Dialog
      v-model:visible="responseDialog.visible"
      :header="responseDialog.modelName"
      :style="{ width: '600px' }"
      :modal="true"
      :draggable="false"
    >
      <div class="response-dialog">
        <div class="response-dialog__meta">
          <img
            :src="responseDialog.modelIcon"
            :alt="responseDialog.modelName"
            class="response-dialog__icon"
          />
          <div class="response-dialog__info">
            <span class="response-dialog__label">Response from</span>
            <span class="response-dialog__name">{{
              responseDialog.modelName
            }}</span>
          </div>
        </div>
        <Divider />
        <div class="response-dialog__prompt">
          <span class="response-dialog__section-label">Your prompt</span>
          <p>{{ responseDialog.prompt }}</p>
        </div>
        <Divider />
        <div class="response-dialog__response">
          <span class="response-dialog__section-label">Answer</span>
          <p>{{ responseDialog.response }}</p>
        </div>
      </div>

      <template #footer>
        <Button label="Close" text @click="responseDialog.visible = false" />
        <Button label="Copy" icon="pi pi-copy" @click="copyResponse" />
      </template>
    </Dialog>

    <Toast />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import Button from 'primevue/button'
import Divider from 'primevue/divider'
import Textarea from 'primevue/textarea'
import Toast from 'primevue/toast'
import Dialog from 'primevue/dialog'
import { useToast } from 'primevue/usetoast'
import { getQuota, submitPrompt, useModel } from '@/services/routingService'
import { useRoutingStore } from '@/stores/routing'
import type { ModelResult , WebSearchAnswer } from '@/services/routingService'

const toast = useToast()
const routingStore = useRoutingStore()

const mode = ref<'router' | 'chat'>('router')
const prompt = ref('')
const loading = ref(false)
const usingModelId = ref<string | null>(null)
const models = ref<ModelResult[]>([])
const quota = ref({ remaining: 10000, total: 10000 })

const responseDialog = reactive({
  visible: false,
  modelName: '',
  modelIcon: '',
  prompt: '',
  response: '',
})

onMounted(async () => {
  quota.value = await getQuota()

  if (routingStore.pendingPrompt) {
    prompt.value = routingStore.pendingPrompt
    routingStore.clearPrompt()
    await handleSubmit()
  }
})

const webSearch = ref(false)
const webAnswers = ref<WebSearchAnswer[]>([])

async function handleSubmit() {
  loading.value = true
  webSearch.value = false
  webAnswers.value = []
  models.value = []
  try {
    const result = await submitPrompt(prompt.value, mode.value)
    if (result.webSearch) {
      webSearch.value = true
      webAnswers.value = result.answers
    } else {
      models.value = result.models
    }
  } catch (err) {
    toast.add({
      severity: 'error',
      summary: 'Request failed',
      detail: err instanceof Error ? err.message : 'Unknown error',
      life: 4000,
    })
  } finally {
    loading.value = false
  }
}

async function handleUseModel(model: ModelResult) {
  usingModelId.value = model.id
  try {
    const result = await useModel(model.id, prompt.value)
    if (result.success) {
      responseDialog.modelName = model.name
      responseDialog.modelIcon = model.icon
      responseDialog.prompt = prompt.value
      responseDialog.response = result.response
      responseDialog.visible = true
    }
  } catch (err) {
    toast.add({
      severity: 'error',
      summary: 'Inference failed',
      detail: err instanceof Error ? err.message : 'Unknown error',
      life: 4000,
    })
  } finally {
    usingModelId.value = null
  }
}

async function copyResponse() {
  await navigator.clipboard.writeText(responseDialog.response)
  toast.add({
    severity: 'info',
    summary: 'Copied!',
    detail: 'Response copied to clipboard',
    life: 2000,
  })
}

function getModelIcon(modelName: string): string {
  const name = modelName.toLowerCase()
  if (name.includes('llama') || name.includes('meta')) return '/meta-color.svg'
  if (name.includes('mistral') || name.includes('mixtral'))
    return '/mistral-color.svg'
  if (name.includes('qwen')) return '/qwen-color.svg'
  return '/meta-color.svg'
}

function onImgError(e: Event) {
  const img = e.target as HTMLImageElement
  img.src = getModelIcon(img.alt ?? '')
}
</script>

<style scoped src="@/assets/routing/RoutingView.css" />