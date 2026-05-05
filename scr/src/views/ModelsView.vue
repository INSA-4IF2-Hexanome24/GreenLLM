<template>
  <div class="models">
    <AddModelForm />
    <ModelList />
  </div>
</template>

<script setup lang="ts">
import AddModelForm from '@/components/models/AddModelForm.vue'
import ModelList from '@/components/models/ModelList.vue'
</script>

<style scoped src="@/assets/models/ModelsView.css" />