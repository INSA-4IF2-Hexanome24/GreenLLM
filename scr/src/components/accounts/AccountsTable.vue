<template>
  <div class="accounts-table-wrapper">
    <table class="accounts-table">
      <thead>
        <tr>
          <!-- <th>#</th> -->
          <th>Member</th>
          <th>Department</th>
          <th>Monthly Budget</th>
          <th>Used</th>
          <th>Usage</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="account in accounts" :key="account.id">
        <td>
            <div class="accounts-table__member">
            <img
                :src="account.avatar"
                :alt="account.name"
                class="accounts-table__avatar"
            />
            <span>{{ account.name }}</span>
            </div>
        </td>
        <td>{{ account.department }}</td>
        <td>${{ account.monthlyBudget.toLocaleString() }}</td>
        <td>${{ account.used.toLocaleString() }}</td>
        <td>
            <div class="accounts-table__progress-wrap">
            <div class="accounts-table__progress">
                <div
                class="accounts-table__progress-bar"
                :class="getBarClass(account)"
                :style="{ width: getUsagePercent(account) + '%' }"
                />
            </div>
            <span class="accounts-table__percent">
                {{ getUsagePercent(account) }}%
            </span>
            </div>
        </td>
        <td>
            <span
            class="accounts-table__status"
            :class="`accounts-table__status--${getStatusClass(account)}`"
            >
            {{ getStatusLabel(account) }}
            </span>
        </td>
        <td>
            <div class="accounts-table__actions">
            <button
                class="accounts-table__btn accounts-table__btn--adjust"
                @click="openAdjust(account)"
            >
                Adjust
            </button>
            <button
                class="accounts-table__btn"
                :class="
                account.status === 'suspended'
                    ? 'accounts-table__btn--reactivate'
                    : 'accounts-table__btn--suspend'
                "
                @click="toggleStatus(account)"
            >
                {{ account.status === 'suspended' ? 'Reactivate' : 'Suspend' }}
            </button>
            </div>
        </td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- Adjust Budget Dialog -->
  <Dialog
    v-model:visible="adjustDialog"
    modal
    header="Adjust Budget"
    :style="{ width: '380px' }"
  >
    <div class="adjust-dialog">
      <p class="adjust-dialog__name">{{ selectedAccount?.name }}</p>
      <label class="adjust-dialog__label">New Monthly Budget ($)</label>
      <InputNumber
        v-model="newBudget"
        :min="0"
        :use-grouping="true"
        class="adjust-dialog__input"
        fluid
      />
    </div>
    <template #footer>
      <Button
        label="Cancel"
        severity="secondary"
        text
        @click="adjustDialog = false"
      />
      <Button label="Save" @click="saveAdjust" />
    </template>
  </Dialog>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import InputNumber from 'primevue/inputnumber'
import {
  getAccounts,
  updateAccountBudget,
  toggleAccountStatus,
} from '@/services/dashboardService'

type Account = {
  id: number
  name: string
  avatar: string
  department: string
  monthlyBudget: number
  used: number
  status: 'active' | 'suspended'
}

const accounts = ref<Account[]>([])
const adjustDialog = ref(false)
const selectedAccount = ref<Account | null>(null)
const newBudget = ref(0)

onMounted(async () => {
  accounts.value = await getAccounts()
})

function getUsagePercent(account: Account) {
  return Math.min(
    Math.round((account.used / account.monthlyBudget) * 100),
    100
  )
}

function getBarClass(account: Account) {
  const pct = (account.used / account.monthlyBudget) * 100
  if (account.status === 'suspended') return 'accounts-table__progress-bar--suspended'
  if (pct >= 100) return 'accounts-table__progress-bar--danger'
  if (pct >= 80) return 'accounts-table__progress-bar--warning'
  return 'accounts-table__progress-bar--ok'
}

function getStatusClass(account: Account) {
  if (account.status === 'suspended') return 'suspended'
  const pct = (account.used / account.monthlyBudget) * 100
  if (pct >= 100) return 'over'
  return 'active'
}

function getStatusLabel(account: Account) {
  if (account.status === 'suspended') return 'Suspended'
  const pct = (account.used / account.monthlyBudget) * 100
  if (pct >= 100) return 'Over Budget'
  return 'Active'
}

function openAdjust(account: Account) {
  selectedAccount.value = account
  newBudget.value = account.monthlyBudget
  adjustDialog.value = true
}

async function saveAdjust() {
  if (!selectedAccount.value) return
  await updateAccountBudget(selectedAccount.value.id, newBudget.value)
  const target = accounts.value.find((a) => a.id === selectedAccount.value!.id)
  if (target) target.monthlyBudget = newBudget.value
  adjustDialog.value = false
}

async function toggleStatus(account: Account) {
  const next = account.status === 'suspended' ? 'active' : 'suspended'
  await toggleAccountStatus(account.id, next)
  account.status = next
}
</script>

<style scoped src="@/assets/accounts/AccountsTable.css" />