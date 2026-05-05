// src/stores/auth.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'

interface User {
  name: string
  username: string
  email: string
  role: string
  city: string
  country: string
  avatar?: string
}

export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref(false)
  const currentUser = ref<User | null>(null)

  function login(username: string, password: string): boolean {
    if (username === 'ewan' && password === 'admin') {
      isAuthenticated.value = true
      currentUser.value = {
        name: 'Ewan',
        username,
        email: '',
        role: '',
        city: '',
        country: '',
      }
      return true
    }
    return false
  }

  function register(userData: Omit<User, 'avatar'> & { password: string }): boolean {
    // Mock registration — replace with API call later
    isAuthenticated.value = true
    currentUser.value = {
      name: userData.name,
      username: userData.username,
      email: userData.email,
      role: userData.role,
      city: userData.city,
      country: userData.country,
    }
    return true
  }

  function logout() {
    isAuthenticated.value = false
    currentUser.value = null
  }

  return { isAuthenticated, currentUser, login, register, logout }
})