import { defineStore } from 'pinia'
import { ref } from 'vue'
import { apiLogin, apiRegister } from '@/services/authService'

export type UserRole = 'admin' | 'employee'

interface User {
  name: string
  username: string
  email: string
  role: UserRole
  city: string
  country: string
  avatar?: string
}

export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref(false)
  const currentUser = ref<User | null>(null)
  const error = ref<string | null>(null)
  const loading = ref(false)

  async function login(email: string, password: string): Promise<boolean> {
    loading.value = true
    error.value = null
    try {
      const data = await apiLogin(email, password)
      currentUser.value = {
        name: data.name,
        username: data.username,
        email: data.email,
        role: data.role as UserRole,
        city: data.city,
        country: data.country,
        avatar: data.avatar ?? undefined,
      }
      isAuthenticated.value = true
      return true
    } catch (e: any) {
      error.value = e.message ?? 'Login failed'
      return false
    } finally {
      loading.value = false
    }
  }

  async function register(userData: {
    email: string
    password: string
    prenom: string
    nom: string
    adresse?: string
    budget?: number
  }): Promise<boolean> {
    loading.value = true
    error.value = null
    try {
      const data = await apiRegister({
        email: userData.email,
        motDePasse: userData.password,
        prenom: userData.prenom,
        nom: userData.nom,
        adresse: userData.adresse,
        budget: userData.budget,
        statut: 'EMPLOYE',
      })
      currentUser.value = {
        name: data.name,
        username: data.username,
        email: data.email,
        role: data.role as UserRole,
        city: data.city,
        country: data.country,
        avatar: data.avatar ?? undefined,
      }
      isAuthenticated.value = true
      return true
    } catch (e: any) {
      error.value = e.message ?? 'Registration failed'
      return false
    } finally {
      loading.value = false
    }
  }

  function logout() {
    isAuthenticated.value = false
    currentUser.value = null
    error.value = null
  }

  return {
    isAuthenticated,
    currentUser,
    error,
    loading,
    login,
    register,
    logout,
  }
})