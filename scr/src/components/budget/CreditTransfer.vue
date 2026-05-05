<template>
  <Card class="dashboard-card">
    <template #title>Credit Transfer</template>
    <template #content>
      <div class="contacts">
        <div
          v-for="contact in contacts"
          :key="contact.id"
          class="contact"
        >
          <Avatar :image="contact.avatar" shape="circle" size="large" />
          <span class="contact__name">{{ contact.name }}</span>
          <span class="contact__role">{{ contact.role }}</span>
        </div>
      </div>
      <Divider />
      <div class="transfer-row">
        <span class="transfer-label">Write Amount</span>
        <InputNumber
          v-model="amount"
          mode="currency"
          currency="USD"
          locale="en-US"
          inputClass="transfer-input"
        />
        <Button label="Send" icon="pi pi-send" rounded />
      </div>
    </template>
  </Card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Card from 'primevue/card'
import Avatar from 'primevue/avatar'
import Button from 'primevue/button'
import InputNumber from 'primevue/inputnumber'
import Divider from 'primevue/divider'
import { getCreditTransferContacts } from '@/services/dashboardService'

const contacts = ref<any[]>([])
const amount = ref(25.5)

onMounted(async () => {
  contacts.value = await getCreditTransferContacts()
})
</script>

<style scoped src="@/assets/budget/CreditTransfer.css" />