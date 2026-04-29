<template>
  <div>Landing</div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()
router.push('/user/dashboard')
</script>