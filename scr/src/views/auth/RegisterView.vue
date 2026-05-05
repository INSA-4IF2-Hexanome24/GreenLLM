<template>
  <div class="register-wrapper">
    <img src="/login/logIn2.png" alt="background" class="register-bg" />

    <div class="register-card">
      <!-- Header: Tabs + Logo -->
      <div class="register-card__header">
        <div class="register-tabs">
          <button
            v-for="tab in tabs"
            :key="tab.value"
            class="register-tab"
            :class="{ 'register-tab--active': activeTab === tab.value }"
            @click="activeTab = tab.value"
          >
            {{ tab.label }}
          </button>
        </div>
        <div class="login-header">
          <img src="/logo.png" alt="GreenLLM Logo" class="login-logo" />
          <h3 class="login-brand">GreenLLM</h3>
        </div>
      </div>

      <!-- Profile Tab -->
      <div v-if="activeTab === 'profile'" class="register-body">
        <div class="register-avatar">
          <img
            :src="avatarPreview ?? '/default-avatar.png'"
            alt=""
            class="register-avatar__img"
          />
          <button class="register-avatar__btn" @click="triggerAvatarUpload">
            <i class="pi pi-pencil" style="font-size: 0.65rem" />
          </button>
          <input
            ref="avatarInput"
            type="file"
            accept="image/*"
            class="hidden"
            @change="onAvatarChange"
          />
        </div>

        <div class="register-fields">
          <div class="register-grid">
            <div class="login-field">
              <label class="login-label">Your Name</label>
              <InputText v-model="form.name" placeholder="Charlene Reed" />
            </div>
            <div class="login-field">
              <label class="login-label">User Name</label>
              <InputText v-model="form.username" placeholder="Charlene Reed" />
            </div>
            <div class="login-field">
              <label class="login-label">Email</label>
              <InputText
                v-model="form.email"
                type="email"
                placeholder="charlenereed@gmail.com"
              />
            </div>
            <div class="login-field">
              <label class="login-label">Password</label>
              <Password
                v-model="form.password"
                placeholder="••••••••••"
                :toggleMask="true"
                :feedback="false"
                fluid
              />
            </div>
            <div class="login-field">
              <label class="login-label">Role</label>
              <InputText v-model="form.role" placeholder="CEO" />
            </div>
            <div class="login-field">
              <label class="login-label">City</label>
              <InputText v-model="form.city" placeholder="San Jose" />
            </div>
            <div class="login-field register-grid__full">
              <label class="login-label">Country</label>
              <InputText v-model="form.country" placeholder="USA" />
            </div>
          </div>
        </div>
      </div>

      <!-- Preferences Tab -->
      <div v-else-if="activeTab === 'preferences'" class="register-placeholder">
        <p>Preferences settings coming soon.</p>
      </div>

      <!-- Security Tab -->
      <div v-else-if="activeTab === 'security'" class="register-placeholder">
        <p>Security settings coming soon.</p>
      </div>

      <!-- Error -->
      <Message v-if="errorMsg" severity="error" :closable="false">
        {{ errorMsg }}
      </Message>

      <!-- Footer -->
      <div class="register-footer">
        <p class="login-register">
          Already have an account?
          <a class="login-link" @click="router.push('/login')">Sign in</a>
        </p>
        <Button
          label="Save"
          :loading="loading"
          class="register-save-btn"
          @click="handleRegister"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Message from 'primevue/message'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const tabs = [
  { label: 'Edit Profile', value: 'profile' },
  { label: 'Preferences', value: 'preferences' },
  { label: 'Security', value: 'security' },
]

const activeTab = ref('profile')
const loading = ref(false)
const errorMsg = ref('')
const avatarPreview = ref<string | null>(null)
const avatarInput = ref<HTMLInputElement | null>(null)

const form = ref({
  name: '',
  username: '',
  email: '',
  password: '',
  role: '',
  city: '',
  country: '',
})

function triggerAvatarUpload() {
  avatarInput.value?.click()
}

function onAvatarChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  avatarPreview.value = URL.createObjectURL(file)
}

async function handleRegister() {
  errorMsg.value = ''
  const { name, username, email, password } = form.value
  if (!name || !username || !email || !password) {
    errorMsg.value = 'Please fill in all required fields.'
    return
  }

  loading.value = true
  await new Promise((resolve) => setTimeout(resolve, 800))

  const success = auth.register(form.value)
  if (success) {
    router.push('/user/dashboard')
  } else {
    errorMsg.value = 'Registration failed. Please try again.'
  }
  loading.value = false
}
</script>

<style scoped src="@/assets/auth/RegisterView.css" />