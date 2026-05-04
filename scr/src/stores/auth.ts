import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref(false)
  const currentUser = ref<string | null>(null)

  function login(username: string, password: string): boolean {
    // Fake auth — replace with real API call later
    if (username === 'ewan' && password === 'admin') {
      isAuthenticated.value = true
      currentUser.value = username
      return true
    }
    return false
  }

  function logout() {
    isAuthenticated.value = false
    currentUser.value = null
  }

  return { isAuthenticated, currentUser, login, logout }
})