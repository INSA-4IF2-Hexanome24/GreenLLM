<template>
  <div class="model-list">
    <h2 class="model-list__title">Model List</h2>
    <div class="model-list__card">
      <div
        v-for="model in models"
        :key="model.id"
        class="model-list__row"
      >
        <div class="model-list__icon-wrap">
          <img
            :src="model.icon"
            :alt="model.name"
            class="model-list__icon"
          />
        </div>

        <div class="model-list__col">
          <span class="model-list__primary">{{ model.displayName }}</span>
          <span class="model-list__secondary">{{ model.type === 'local' ? 'Local' : 'Remote' }}</span>
        </div>

        <div class="model-list__col">
          <span class="model-list__primary">{{ model.provider }}</span>
          <span class="model-list__secondary">Provider</span>
        </div>

        <div class="model-list__col">
          <span class="model-list__primary">
            {{ model.type === 'local' ? model.ollamaUrl : model.apiKey }}
          </span>
          <span class="model-list__secondary">
            {{ model.type === 'local' ? 'URL' : 'API Key' }}
          </span>
        </div>

        <div class="model-list__col">
          <span class="model-list__primary">${{ model.budget.toLocaleString() }}</span>
          <span class="model-list__secondary">Budget</span>
        </div>

        <div class="model-list__col">
          <span class="model-list__primary">
            {{ model.allowedTeams.join(', ') }}
          </span>
          <span class="model-list__secondary">Allowed Teams</span>
        </div>

        <button
          class="model-list__details-btn"
          @click="openDetails(model)"
        >
          View Details
        </button>
      </div>
    </div>
  </div>

  <!-- Details Dialog -->
  <Dialog
    v-model:visible="detailsDialog"
    modal
    :header="selectedModel?.displayName"
    :style="{ width: '460px' }"
  >
    <div v-if="selectedModel" class="model-details">
      <div class="model-details__header">
        <img
          :src="selectedModel.icon"
          :alt="selectedModel.name"
          class="model-details__icon"
        />
        <div>
          <p class="model-details__name">{{ selectedModel.displayName }}</p>
          <span
            class="model-details__type"
            :class="`model-details__type--${selectedModel.type}`"
          >
            {{ selectedModel.type === 'local' ? 'Local' : 'Remote' }}
          </span>
        </div>
      </div>

      <div class="model-details__grid">
        <div class="model-details__item">
          <span class="model-details__item-label">Provider</span>
          <span class="model-details__item-value">{{ selectedModel.provider }}</span>
        </div>
        <div class="model-details__item">
          <span class="model-details__item-label">Model Name</span>
          <span class="model-details__item-value">{{ selectedModel.name }}</span>
        </div>
        <div class="model-details__item">
          <span class="model-details__item-label">
            {{ selectedModel.type === 'local' ? 'Ollama URL' : 'API Key' }}
          </span>
          <span class="model-details__item-value">
            {{ selectedModel.type === 'local' ? selectedModel.ollamaUrl : selectedModel.apiKey }}
          </span>
        </div>
        <div class="model-details__item">
          <span class="model-details__item-label">Budget</span>
          <span class="model-details__item-value">${{ selectedModel.budget.toLocaleString() }}</span>
        </div>
        <div class="model-details__item model-details__item--full">
          <span class="model-details__item-label">Allowed Teams</span>
          <div class="model-details__tags">
            <span
              v-for="team in selectedModel.allowedTeams"
              :key="team"
              class="model-details__tag"
            >
              {{ team }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <Button
        label="Close"
        severity="secondary"
        text
        @click="detailsDialog = false"
      />
      <Button
        label="Delete Model"
        severity="danger"
        @click="handleDelete"
      />
    </template>
  </Dialog>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import { getModels, deleteModel } from '@/services/dashboardService'

type Model = {
  id: number
  name: string
  provider: string
  type: 'remote' | 'local'
  apiKey?: string
  ollamaUrl?: string
  displayName: string
  budget: number
  allowedTeams: string[]
  icon: string
}

const models = ref<Model[]>([])
const detailsDialog = ref(false)
const selectedModel = ref<Model | null>(null)

onMounted(async () => {
  models.value = await getModels()
})

function openDetails(model: Model) {
  selectedModel.value = model
  detailsDialog.value = true
}

async function handleDelete() {
  if (!selectedModel.value) return
  await deleteModel(selectedModel.value.id)
  models.value = models.value.filter((m) => m.id !== selectedModel.value!.id)
  detailsDialog.value = false
}
</script>

<style scoped src="@/assets/models/ModelList.css" />