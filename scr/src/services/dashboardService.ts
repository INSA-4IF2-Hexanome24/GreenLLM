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


//---------------------------Carbon dashboard mock data ------------------------------

export async function getCO2SavedOverTime() {
  return {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    data: [200, 320, 280, 350, 300, 390],
  }
}

export async function getCO2EmissionsOverTime() {
  return {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
    data: [480, 520, 410, 390, 220],
  }
}

export async function getCO2ByModel() {
  return {
    labels: ['Claude', 'GPT-4', 'Mistral', 'Gemini'],
    data: [40, 25, 20, 15],
  }
}

export async function getCO2ByTeam() {
  return {
    labels: ['Engineering', 'HR', 'Direction', 'Marketing'],
    data: [40, 20, 25, 15],
  }
}

export async function getCarbonSavings(range: string) {
  const data: Record<string, string> = {
    'Jan – Feb': '180kgCO2e',
    'Mar – Apr': '260kgCO2e',
    'May – Jun': '400kgCO2e',
    'Jul – Aug': '310kgCO2e',
    'Sep – Oct': '290kgCO2e',
    'Nov – Dec': '350kgCO2e',
  }
  return {
    saved: data[range] ?? '—',
    dateRange: range,
  }
}

export async function getCarbonStats() {
  return [
    { label: 'Actual emissions', value: '820 kgCO2e',  icon: 'pi pi-send' },
    { label: 'Baseline',         value: '1,220 kgCO2e', icon: 'pi pi-globe' },
    { label: 'Reduction',        value: '32.8%',        icon: 'pi pi-chart-line' },
  ]
}

export async function getTopSpenders() {
  return [
    { name: 'Jaime Rey',      time: '5h ago',      value: 100, avatar: '/avatars/jaime.jpg' },
    { name: 'Martin Vasquez', time: '2 days ago',  value: 50,  avatar: '/avatars/martin.jpg' },
    { name: 'Liam LeGoat',   time: '5 days ago',  value: 20,  avatar: '/avatars/liam.jpg' },
    { name: 'Josue Vega',    time: '10 days ago', value: 10,  avatar: '/avatars/josue.jpg' },
  ]
}

export async function getTopSavers() {
  return [
    { name: 'Jaime Rey',      time: '5h ago',      value: 100, avatar: '/avatars/jaime.jpg' },
    { name: 'Martin Vasquez', time: '2 days ago',  value: 50,  avatar: '/avatars/martin.jpg' },
    { name: 'Liam LeGoat',   time: '5 days ago',  value: 20,  avatar: '/avatars/liam.jpg' },
    { name: 'Josue Vega',    time: '10 days ago', value: 10,  avatar: '/avatars/josue.jpg' },
  ]
}

//---------------------------comptes employess ---------------------------------

export async function getAccountsStats() {
  return {
    totalMembers: 8,
    totalBudget: '$1,640,000',
    totalSpent: '$312,400',
    overBudget: 2,
  }
}

export async function getAccounts() {
  return [
    {
      id: 1,
      name: 'Jaime Rey',
      avatar: '/avatars/jaime.jpg',
      department: 'Engineering',
      monthlyBudget: 40500,
      used: 38200,
      status: 'active',
    },
    {
      id: 2,
      name: 'Ewan McGregor',
      avatar: '/avatars/ewan.jpg',
      department: 'Direction',
      monthlyBudget: 250000,
      used: 261000,
      status: 'active',
    },
    {
      id: 3,
      name: 'Martin Vasquez',
      avatar: '/avatars/martin.jpg',
      department: 'Engineering',
      monthlyBudget: 900000,
      used: 420000,
      status: 'active',
    },
    {
      id: 4,
      name: 'Liam LeGoat',
      avatar: '/avatars/liam.jpg',
      department: 'Marketing',
      monthlyBudget: 50000,
      used: 51200,
      status: 'suspended',
    },
    {
      id: 5,
      name: 'Josue Vega',
      avatar: '/avatars/josue.jpg',
      department: 'HR',
      monthlyBudget: 50000,
      used: 8000,
      status: 'active',
    },
    {
      id: 6,
      name: 'Sofia Reyes',
      avatar: '/avatars/sofia.jpg',
      department: 'Marketing',
      monthlyBudget: 80000,
      used: 64000,
      status: 'active',
    },
    {
      id: 7,
      name: 'Noah Petit',
      avatar: '/avatars/noah.jpg',
      department: 'HR',
      monthlyBudget: 12000,
      used: 1560,
      status: 'active',
    },
    {
      id: 8,
      name: 'Amira Osei',
      avatar: '/avatars/amira.jpg',
      department: 'Engineering',
      monthlyBudget: 160000,
      used: 160800,
      status: 'active',
    },
  ]
}

export async function updateAccountBudget(id: number, newBudget: number) {
  // POST /accounts/:id/budget
  console.log(`Updated account ${id} budget to ${newBudget}`)
}

export async function toggleAccountStatus(id: number, status: 'active' | 'suspended') {
  // POST /accounts/:id/status
  console.log(`Account ${id} status set to ${status}`)
}

//------------------------data for models page ------------------------------

export async function getModels() {
  return [
    {
      id: 1,
      name: 'gpt-4o',
      provider: 'OpenAI',
      type: 'remote',
      apiKey: '****  **** 5600',
      displayName: 'GPT-4 Omni',
      budget: 1000,
      allowedTeams: ['Engineering', 'Marketing'],
      icon: 'https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg',
    },
    {
      id: 2,
      name: 'claude-3-5-sonnet',
      provider: 'Anthropic',
      type: 'remote',
      apiKey: '**** **** 4300',
      displayName: 'Claude Sonnet',
      budget: 2000,
      allowedTeams: ['Direction', 'HR'],
      icon: 'https://upload.wikimedia.org/wikipedia/commons/8/8a/Claude_AI_logo.svg',
    },
    {
      id: 3,
      name: 'llama3',
      provider: 'Ollama',
      type: 'local',
      ollamaUrl: 'http://localhost:11434',
      displayName: 'Llama 3 Local',
      budget: 500,
      allowedTeams: ['Engineering'],
      icon: 'https://ollama.com/public/ollama.png',
    },
    {
      id: 4,
      name: 'mistral',
      provider: 'Mistral',
      type: 'remote',
      apiKey: '**** **** 8821',
      displayName: 'Mistral 7B',
      budget: 800,
      allowedTeams: ['Marketing'],
      icon: 'https://mistral.ai/images/logo_hubc88c4ece131b91c7cb753f40e9e1cc5_2589_256x0_resize_q97_h2_lanczos_3.webp',
    },
  ]
}

export async function addModel(model: Record<string, any>) {
  // POST /models
  console.log('Adding model:', model)
}

export async function deleteModel(id: number) {
  // DELETE /models/:id
  console.log('Deleting model:', id)
}

export async function getTeamsAndMembers() {
  return {
    teams: ['Engineering', 'HR', 'Direction', 'Marketing'],
    members: ['Jaime Rey', 'Ewan McGregor', 'Martin Vasquez', 'Liam LeGoat', 'Josue Vega', 'Sofia Reyes', 'Noah Petit', 'Amira Osei'],
  }
}

//------------------------reports page data ------------------------------

export async function getReports() {
  return [
    {
      id: 1,
      name: 'Business Report',
      description: 'Overview of all AI-related business expenses and usage.',
      generatedBy: 'Jaime Rey',
      frequency: 'Monthly',
      lastGenerated: '01 May 2026',
      icon: 'pi pi-dollar',
      details:
        'This report provides a full breakdown of AI spending across all departments, including cost per model, cost per team, and monthly trends. Ideal for finance and executive review.',
    },
    {
      id: 2,
      name: 'Team Report',
      description: 'AI usage and costs broken down by team.',
      generatedBy: 'Sofia Reyes',
      frequency: 'Weekly',
      lastGenerated: '28 Apr 2026',
      icon: 'pi pi-users',
      details:
        'Breaks down AI usage per team, showing which departments consume the most tokens, their associated costs, and how they track against their allocated budgets.',
    },
    {
      id: 3,
      name: 'CO2 Savings Report',
      description: 'Carbon savings achieved through optimized AI routing.',
      generatedBy: 'Martin Vasquez',
      frequency: 'Monthly',
      lastGenerated: '01 May 2026',
      icon: 'pi pi-chart-line',
      details:
        'Tracks CO2 emissions saved by routing requests to more energy-efficient models. Includes baseline vs actual emissions, reduction percentage, and top contributing teams.',
    },
    {
      id: 4,
      name: 'Usage Report',
      description: 'Detailed log of all AI model requests and token usage.',
      generatedBy: 'Amira Osei',
      frequency: 'On-demand',
      lastGenerated: '30 Apr 2026',
      icon: 'pi pi-list',
      details:
        'A granular log of every AI request made across the platform. Includes model used, token count, cost per request, user, and timestamp. Useful for auditing and optimization.',
    },
  ]
}