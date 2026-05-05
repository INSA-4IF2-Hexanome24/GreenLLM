<template>
  <div class="add-model">
    <h2 class="add-model__title">Add New Model (Local Ollama Or Remote)</h2>
    <div class="add-model__card">
      <p class="add-model__description">
        Add a remote model using an API key from providers like OpenAI or
        Anthropic, or connect a local model running via Ollama on your
        infrastructure.
      </p>

      <!-- Toggle -->
      <div class="add-model__toggle">
        <button
          class="add-model__toggle-btn"
          :class="{ 'add-model__toggle-btn--active': modelType === 'remote' }"
          @click="modelType = 'remote'"
        >
          Remote
        </button>
        <button
          class="add-model__toggle-btn"
          :class="{ 'add-model__toggle-btn--active': modelType === 'local' }"
          @click="modelType = 'local'"
        >
          Local (Ollama)
        </button>
      </div>

      <div class="add-model__form">
        <!-- Remote fields -->
        <template v-if="modelType === 'remote'">
          <div class="add-model__field">
            <label class="add-model__label">API Key</label>
            <InputText
              v-model="form.apiKey"
              placeholder="XXXX-XXXX"
              class="add-model__input"
              fluid
            />
          </div>
          <div class="add-model__field">
            <label class="add-model__label">Provider</label>
            <Select
              v-model="form.provider"
              :options="providers"
              placeholder="Select provider"
              class="add-model__input"
              fluid
            />
          </div>
        </template>

        <!-- Local fields -->
        <template v-if="modelType === 'local'">
          <div class="add-model__field">
            <label class="add-model__label">Ollama URL</label>
            <InputText
              v-model="form.ollamaUrl"
              placeholder="http://localhost:11434"
              class="add-model__input"
              fluid
            />
          </div>
          <div class="add-model__field">
            <label class="add-model__label">Model Name</label>
            <InputText
              v-model="form.name"
              placeholder="llama3, mistral..."
              class="add-model__input"
              fluid
            />
          </div>
        </template>

        <!-- Common fields -->
        <div class="add-model__field">
          <label class="add-model__label">Display Name</label>
          <InputText
            v-model="form.displayName"
            placeholder="My Model"
            class="add-model__input"
            fluid
          />
        </div>
        <div class="add-model__field">
          <label class="add-model__label">Budget ($)</label>
          <InputNumber
            v-model="form.budget"
            placeholder="1000"
            :min="0"
            class="add-model__input"
            fluid
          />
        </div>
        <div class="add-model__field add-model__field--full">
          <label class="add-model__label">Allowed Teams / Members</label>
          <MultiSelect
            v-model="form.allowed"
            :options="allOptions"
            optionGroupLabel="label"
            optionGroupChildren="items"
            placeholder="Select teams or members"
            class="add-model__input"
            fluid
          />
        </div>
      </div>

      <button class="add-model__submit" @click="handleSubmit">
        Add Model
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Select from 'primevue/select'
import MultiSelect from 'primevue/multiselect'
import { addModel, getTeamsAndMembers } from '@/services/dashboardService'

const modelType = ref<'remote' | 'local'>('remote')

const providers = ['OpenAI', 'Anthropic', 'Mistral', 'Google', 'Cohere']

const form = ref({
  apiKey: '',
  provider: '',
  ollamaUrl: '',
  name: '',
  displayName: '',
  budget: null as number | null,
  allowed: [] as string[],
})

const allOptions = ref<{ label: string; items: string[] }[]>([])

onMounted(async () => {
  const { teams, members } = await getTeamsAndMembers()
  allOptions.value = [
    { label: 'Teams', items: teams },
    { label: 'Members', items: members },
  ]
})

async function handleSubmit() {
  await addModel({ ...form.value, type: modelType.value })
  form.value = {
    apiKey: '',
    provider: '',
    ollamaUrl: '',
    name: '',
    displayName: '',
    budget: null,
    allowed: [],
  }
}
</script>

<style scoped src="@/assets/models/AddModelForm.css" />