<template>
  <div class="dashboard">
    <h1 class="dashboard__title">Overview</h1>

    <div class="dashboard__grid">
      <!-- Budget Cards -->
      <section class="card budget-section">
        <div class="section-header">
          <span class="section-title">My Budgets</span>
          <Button label="See All" link />
        </div>
        <div class="budget-cards">
          <div
            v-for="budget in budgets"
            :key="budget.id"
            :class="['budget-card', { 'budget-card--active': budget.active }]"
          >
            <div class="budget-card__top">
              <span class="budget-card__label">Balance</span>
              <span class="budget-card__valid">VALID THRU {{ budget.validThru }}</span>
            </div>
            <div class="budget-card__balance">${{ budget.balance.toLocaleString() }}</div>
            <div class="budget-card__holder">CARD HOLDER: {{ budget.cardHolder }}</div>
          </div>
        </div>
      </section>

      <!-- Recent Usages -->
      <section class="card recent-section">
        <span class="section-title">Recent Usages</span>
        <div class="recent-list">
          <div v-for="usage in recentUsages" :key="usage.id" class="recent-item">
            <span class="recent-item__icon">{{ usage.icon }}</span>
            <div class="recent-item__info">
              <span class="recent-item__name">{{ usage.name }}</span>
              <span class="recent-item__date">{{ usage.date }}</span>
            </div>
            <span :class="['recent-item__amount', usage.amount < 0 ? 'negative' : 'positive']">
              {{ usage.amount < 0 ? '-' : '+' }}${{ Math.abs(usage.amount).toLocaleString() }}
            </span>
          </div>
        </div>
      </section>

      <!-- Weekly CO2 Chart -->
      <section class="card co2-section">
        <span class="section-title">Weekly CO2 Savings</span>
        <Chart
          type="bar"
          :data="co2ChartData"
          :options="co2ChartOptions"
          style="height: 220px"
        />
      </section>

      <!-- Expense Statistics -->
      <section class="card expense-section">
        <span class="section-title">Expense Statistics</span>
        <Chart
          type="pie"
          :data="expenseChartData"
          :options="expenseChartOptions"
          style="height: 220px"
        />
      </section>

      <!-- Credit Transfer -->
      <section class="card credit-section">
        <span class="section-title">Credit Transfer</span>
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
        <div class="transfer-input">
          <span class="transfer-input__label">Write Amount</span>
          <InputNumber
            v-model="transferAmount"
            mode="currency"
            currency="USD"
            locale="en-US"
            class="transfer-input__field"
          />
          <Button label="Send" icon="pi pi-send" />
        </div>
      </section>

      <!-- Inference Usage -->
      <section class="card inference-section">
        <span class="section-title">Inference Usage (Credits)</span>
        <Chart
          type="line"
          :data="inferenceChartData"
          :options="inferenceChartOptions"
          style="height: 220px"
        />
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Chart from 'primevue/chart'
import Button from 'primevue/button'
import Avatar from 'primevue/avatar'
import InputNumber from 'primevue/inputnumber'
import {
  getBudgets,
  getRecentUsages,
  getWeeklyCO2,
  getExpenseStatistics,
  getCreditTransferContacts,
  getInferenceUsage,
} from '@/services/dashboardService'

// --- State ---
const budgets = ref<any[]>([])
const recentUsages = ref<any[]>([])
const co2ChartData = ref({})
const expenseChartData = ref({})
const inferenceChartData = ref({})
const contacts = ref<any[]>([])
const transferAmount = ref(25.5)

// --- Chart Options ---
const co2ChartOptions = {
  plugins: { legend: { position: 'top' } },
  scales: { y: { beginAtZero: true } },
}
const expenseChartOptions = {
  plugins: { legend: { position: 'right' } },
}
const inferenceChartOptions = {
  plugins: { legend: { display: false } },
  scales: { y: { beginAtZero: true } },
  elements: { line: { tension: 0.4 } },
}

// --- Load Data ---
onMounted(async () => {
  budgets.value = await getBudgets()
  recentUsages.value = await getRecentUsages()
  contacts.value = await getCreditTransferContacts()

  const co2 = await getWeeklyCO2()
  co2ChartData.value = {
    labels: co2.labels,
    datasets: [
      {
        label: 'Actually Used',
        data: co2.actualUsed,
        backgroundColor: '#22d3ee',
      },
      {
        label: 'Estimated Use',
        data: co2.estimatedUse,
        backgroundColor: '#3b82f6',
      },
    ],
  }

  const expenses = await getExpenseStatistics()
  expenseChartData.value = {
    labels: expenses.map((e) => e.label),
    datasets: [
      {
        data: expenses.map((e) => e.value),
        backgroundColor: expenses.map((e) => e.color),
      },
    ],
  }

  const inference = await getInferenceUsage()
  inferenceChartData.value = {
    labels: inference.labels,
    datasets: [
      {
        data: inference.credits,
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59,130,246,0.2)',
        fill: true,
      },
    ],
  }
})
</script>

<style scoped>
.dashboard {
  padding: 2rem;
}
.dashboard__title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
}
.dashboard__grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1.5rem;
}
.card {
  background: #fff;
  border-radius: 1rem;
  padding: 1.25rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.section-title {
  font-weight: 600;
  font-size: 1rem;
  margin-bottom: 1rem;
  display: block;
}
.budget-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}
.budget-card {
  border-radius: 0.75rem;
  padding: 1rem;
  background: #f1f5f9;
  font-size: 0.85rem;
}
.budget-card--active {
  background: linear-gradient(135deg, #4f46e5, #3b82f6);
  color: white;
}
.budget-card__balance {
  font-size: 1.2rem;
  font-weight: 700;
  margin: 0.5rem 0;
}
.budget-card__top {
  display: flex;
  justify-content: space-between;
}
.recent-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.recent-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.recent-item__info {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.recent-item__date {
  font-size: 0.75rem;
  color: #94a3b8;
}
.positive { color: #22c55e; font-weight: 600; }
.negative { color: #ef4444; font-weight: 600; }
.contacts {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1rem;
}
.contact {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.8rem;
}
.contact__role {
  color: #94a3b8;
}
.transfer-input {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 0.5rem;
}
.co2-section,
.inference-section {
  grid-column: 1;
}
.expense-section,
.recent-section {
  grid-column: 2;
}
</style>