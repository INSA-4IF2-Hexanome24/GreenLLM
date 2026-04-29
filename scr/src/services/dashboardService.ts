// src/services/dashboardService.ts
// Replace these functions with real API calls later

export async function getBudgets() {
  return [
    { id: 1, balance: 5756, validThru: '12/22', cardHolder: 'Eddy Cusuma', active: true },
    { id: 2, balance: 5756, validThru: '12/22', cardHolder: 'Eddy Cusuma', active: false },
    { id: 3, balance: 5756, validThru: '12/22', cardHolder: 'Eddy Cusuma', active: false },
    { id: 4, balance: 5756, validThru: '12/22', cardHolder: 'Eddy Cusuma', active: true },
  ]
}

export async function getRecentUsages() {
  return [
    { id: 1, name: 'Project 1 - Marketing', date: '28 January 2021', amount: -850, icon: '🟠' },
    { id: 2, name: 'Project 2 - Engineering', date: '25 January 2021', amount: 2500, icon: '🔵' },
    { id: 3, name: 'Project 3 - Sales', date: '21 January 2021', amount: 5400, icon: '🟢' },
  ]
}

export async function getWeeklyCO2() {
  return {
    labels: ['Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
    actualUsed: [300, 400, 280, 450, 200, 380, 300],
    estimatedUse: [400, 350, 400, 300, 400, 280, 420],
  }
}

export async function getExpenseStatistics() {
  return [
    { label: 'Sales', value: 30, color: '#1a1a2e' },
    { label: 'HR Team', value: 15, color: '#f97316' },
    { label: 'Engineering', value: 35, color: '#3b82f6' },
    { label: 'Marketing', value: 20, color: '#ec4899' },
  ]
}

export async function getCreditTransferContacts() {
  return [
    { id: 1, name: 'Livia Bator', role: 'CEO', avatar: 'https://i.pravatar.cc/150?img=1' },
    { id: 2, name: 'Randy Press', role: 'Director', avatar: 'https://i.pravatar.cc/150?img=2' },
    { id: 3, name: 'Workman', role: 'Designer', avatar: 'https://i.pravatar.cc/150?img=3' },
  ]
}

export async function getInferenceUsage() {
  return {
    labels: ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan'],
    credits: [200, 450, 300, 600, 400, 700, 750],
  }
}