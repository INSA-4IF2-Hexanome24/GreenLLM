// src/stores/routing.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useRoutingStore = defineStore('routing', () => {
  const pendingPrompt = ref('')

  function setPrompt(prompt: string) {
    pendingPrompt.value = prompt
  }

  function clearPrompt() {
    pendingPrompt.value = ''
  }

  return { pendingPrompt, setPrompt, clearPrompt }
})