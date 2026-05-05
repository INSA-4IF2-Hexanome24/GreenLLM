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
    { id: 1, name: 'Project 1 - Marketing',   date: '28 January 2021', amount: -850,  icon: '🟠' },
    { id: 2, name: 'Project 2 - Engineering', date: '25 January 2021', amount: 2500,  icon: '🔵' },
    { id: 3, name: 'Project 3 - Sales',       date: '21 January 2021', amount: 5400,  icon: '🟢' },
  ]
}

export async function getWeeklyCO2() {
  return {
    labels: ['Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
    actualUsed:    [300, 400, 280, 450, 200, 380, 300],
    estimatedUse:  [400, 350, 400, 300, 400, 280, 420],
  }
}

export async function getExpenseStatistics() {
  return [
    { label: 'Sales',       value: 30, color: '#343C6A' },
    { label: 'HR Team',     value: 15, color: '#5D9628' },
    { label: 'Engineering', value: 35, color: '#F3D914' },
    { label: 'Marketing',   value: 20, color: '#A6DB16' },
  ]
}

export async function getCreditTransferContacts() {
  return [
    { id: 1, name: 'Livia Bator', role: 'CEO',      avatar: 'https://i.pravatar.cc/150?img=1' },
    { id: 2, name: 'Randy Press', role: 'Director',  avatar: 'https://i.pravatar.cc/150?img=2' },
    { id: 3, name: 'Workman',     role: 'Designer',  avatar: 'https://i.pravatar.cc/150?img=3' },
  ]
}

export async function getInferenceUsage() {
  return {
    labels:  ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan'],
    credits: [200, 450, 300, 600, 400, 700, 750],
  }
}

// ── Employee dashboard mock data ──────────────────────────────────────────────

export async function getEmployeeStats() {
  return [
    { label: 'Total Credits Used', value: '$150,000', icon: 'pi pi-dollar'  },
    { label: 'Number of requests', value: '1,250',    icon: 'pi pi-sync'    },
    { label: 'CO2 saved',          value: '4kg',      icon: 'pi pi-refresh' },
  ]
}

export async function getTeamMembers() {
  return [
    {
      name:   'Jaime Rey',
      role:   'Commerce Lead',
      usage:  '$10,200',
      savings: '+16%',
      avatar: 'https://i.pravatar.cc/150?img=10',
    },
    {
      name:   'Martin Vasquez',
      role:   'Engineering Officer',
      usage:  '$25,300',
      savings: '-4%',
      avatar: 'https://i.pravatar.cc/150?img=11',
    },
  ]
}

export async function getRecentOperations() {
  return [
    { model: 'Mistral', name: 'Text Gene...', price: '$0.002',  co2: '+5%'  },
    { model: 'GPT3',    name: 'Basic Sum',    price: '$0.0001', co2: '+10%' },
    { model: 'Bloom',   name: 'Translate F...', price: '$0.0002', co2: '-3%'},
  ]
}

export async function getMonthlyUsage() {
  return {
    labels:  ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    credits: [5000, 21000, 18000, 35000, 28000, 30000],
  }
}

export async function getBalanceStats() {
  return [
    { label: 'My Balance', value: '$12,750', icon: 'pi pi-wallet' },
    { label: 'Income',     value: '$5,600',  icon: 'pi pi-arrow-down' },
    { label: 'Expense',    value: '$3,460',  icon: 'pi pi-arrow-up' },
  ]
}

export async function getOverviewChart() {
  return {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    expense: [20000, 42000, 30000, 42000, 28000],
    budget:  [15000, 28000, 18000, 32000, 22000],
  }
}

export async function getRecentTransactions() {
  return [
    {
      id: 1,
      description: 'Traduire texte',
      transactionId: '#12548796',
      owner: 'Jaime Rey',
      card: '1234 ****',
      date: '28 Jan, 12.30 AM',
      amount: -0.02,
      type: 'expense',
    },
    {
      id: 2,
      description: 'Rediger EMail',
      transactionId: '#12548796',
      owner: 'Martin Vasquez',
      card: '1234 ****',
      date: '25 Jan, 10.40 PM',
      amount: -0.009,
      type: 'expense',
    },
    {
      id: 3,
      description: 'Recherche Budget',
      transactionId: '#12548796',
      owner: 'LiamleGoat',
      card: '1234 ****',
      date: '20 Jan, 10.40 PM',
      amount: -0.2,
      type: 'expense',
    },
    {
      id: 4,
      description: 'Generate Report',
      transactionId: '#12548797',
      owner: 'Jaime Rey',
      card: '1234 ****',
      date: '18 Jan, 09.00 AM',
      amount: 5.6,
      type: 'income',
    },
    {
      id: 5,
      description: 'API Call Batch',
      transactionId: '#12548798',
      owner: 'Martin Vasquez',
      card: '1234 ****',
      date: '15 Jan, 03.20 PM',
      amount: -1.2,
      type: 'expense',
    },
  ]
}