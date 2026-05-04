<template>
  <div class="login-wrapper">
    <!-- Left: Image -->
    <div class="login-image">
      <img
        src="/login/logIn.png"
        alt="Green nature"
      />
      <div class="login-image__overlay">
        <!-- <h2 class="login-image__text">Welcome to GreenLLM</h2> -->
      </div>
    </div>

    <!-- Right: Form -->
    <div class="login-form-side">
      <div class="login-card">
        <!-- Logo -->
        <div class="login-header">
          <img
            src="\logo.png"
            alt="GreenLLM Logo"
            class="login-logo"
          />
          <h3 class="login-brand">GreenLLM</h3>
        </div>

        <div class="login-title-group">
          <h1 class="login-title">Ready to save some CO2?</h1>
        </div>

        <!-- Error -->
        <Message v-if="errorMsg" severity="error" :closable="false">
          {{ errorMsg }}
        </Message>

        <!-- Fields -->
        <div class="login-fields">
          <div class="login-field">
            <label for="email" class="login-label">Login</label>
            <InputText
              id="email"
              v-model="username"
              type="text"
              placeholder="Email or phone number"
              class="login-input"
            />
          </div>

          <div class="login-field">
            <label for="password" class="login-label">Password</label>
            <Password
              id="password"
              v-model="password"
              placeholder="Enter password"
              :toggleMask="true"
              :feedback="false"
              fluid
              @keyup.enter="handleLogin"
            />
          </div>

          <div class="login-options">
            <div class="login-remember">
              <ToggleSwitch v-model="rememberMe" />
              <label class="login-label">Remember me</label>
            </div>
            <a class="login-link">Forgot password?</a>
          </div>
        </div>

        <!-- Sign In Button -->
        <Button
          label="Sign in"
          class="login-btn"
          :loading="loading"
          @click="handleLogin"
        />

        <!-- Divider -->
        <Divider align="center">
          <span class="login-divider-text">or</span>
        </Divider>

        <!-- Google Button -->
        <Button
          class="login-google-btn"
          outlined
        >
          <template #default>
            <img
              src="https://www.svgrepo.com/show/475656/google-color.svg"
              alt="Google"
              class="login-google-icon"
            />
            <span>Sign in with Google</span>
          </template>
        </Button>

        <!-- Register -->
        <p class="login-register">
          Don't have an account?
          <a class="login-link" @click="router.push('/register')">Sign up now</a>
        </p>
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
import Divider from 'primevue/divider'
import ToggleSwitch from 'primevue/toggleswitch'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const username = ref('')
const password = ref('')
const rememberMe = ref(false)
const errorMsg = ref('')
const loading = ref(false)

async function handleLogin() {
  errorMsg.value = ''
  loading.value = true

  await new Promise((resolve) => setTimeout(resolve, 800))

  const success = auth.login(username.value, password.value)

  if (success) {
    router.push('/user/dashboard')
  } else {
    errorMsg.value = 'Invalid username or password.'
  }

  loading.value = false
}
</script>

<style scoped src="@/assets/auth/LoginView.css" />