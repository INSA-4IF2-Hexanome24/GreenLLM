<template>
  <div class="carbon-hero">
    <div class="carbon-hero__left">
      <span class="carbon-hero__label">Saved</span>
      <span class="carbon-hero__value">{{ savings.saved }}</span>
    </div>
    <div class="carbon-hero__right">
      <span class="carbon-hero__dates-label">DATES</span>

      <div class="carbon-hero__dropdown-wrapper" ref="dropdownRef">
        <button class="carbon-hero__date-btn" @click="toggleDropdown">
          {{ selectedRange }}
          <i :class="open ? 'pi pi-chevron-up' : 'pi pi-chevron-down'" />
        </button>
        <ul v-if="open" class="carbon-hero__dropdown">
          <li
            v-for="range in ranges"
            :key="range"
            class="carbon-hero__dropdown-item"
            :class="{ 'carbon-hero__dropdown-item--active': range === selectedRange }"
            @click="selectRange(range)"
          >
            {{ range }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { getCarbonSavings } from '@/services/dashboardService'

const ranges = [
  'Jan – Feb',
  'Mar – Apr',
  'May – Jun',
  'Jul – Aug',
  'Sep – Oct',
  'Nov – Dec',
]

const selectedRange = ref('May – Jun')
const open = ref(false)
const dropdownRef = ref<HTMLElement | null>(null)
const savings = ref({ saved: '', dateRange: '' })

async function loadSavings() {
  savings.value = await getCarbonSavings(selectedRange.value)
}

function toggleDropdown() {
  open.value = !open.value
}

async function selectRange(range: string) {
  selectedRange.value = range
  open.value = false
  await loadSavings()
}

function handleClickOutside(e: MouseEvent) {
  if (dropdownRef.value && !dropdownRef.value.contains(e.target as Node)) {
    open.value = false
  }
}

onMounted(async () => {
  await loadSavings()
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped src="@/assets/carbon/CarbonSavingsHero.css" />