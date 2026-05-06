// src/services/routingService.ts

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8080'

export interface ModelResult {
  id: string
  name: string
  tag: string
  co2: number
  power: 'Low' | 'Medium' | 'High'
  cost: number
  icon: string
  utility: number
  performanceScore: number
}

export interface QuotaResult {
  remaining: number
  total: number
}

function getPowerLabel(performance: number): 'Low' | 'Medium' | 'High' {
  if (performance >= 0.7) return 'High'
  if (performance >= 0.4) return 'Medium'
  return 'Low'
}

function getModelIcon(modelName: string): string {
  const name = modelName.toLowerCase()
  if (name.includes('llama') || name.includes('meta')) return '/meta-color.svg'
  if (name.includes('mistral') || name.includes('mixtral')) return '/mistral-color.svg'
  if (name.includes('qwen')) return '/qwen-color.svg'
  return '/meta-color.svg'
}

export async function getQuota(): Promise<QuotaResult> {
  // TODO: replace with real quota endpoint when available
  return { remaining: 10000, total: 10000 }
}

export async function submitPrompt(
  prompt: string,
  mode: 'router' | 'chat',
): Promise<{ models: ModelResult[] }> {
  const res = await fetch(`${API_BASE}/api/dashboard/stats`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: prompt, mode }),
  })

  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`)
  }

  const data = await res.json()

  // data.statsPerModel is the array from RequestDashboardResponse
  const models: ModelResult[] = (data.statsPerModel ?? []).map(
    (item: any, index: number) => ({
      id: item.name,
      name: item.name,
      tag: index === 0 ? 'Best match' : `#${index + 1}`,
      co2: item.co2CostScore,
      power: getPowerLabel(item.performanceScore),
      cost: +(item.co2CostScore * 0.03).toFixed(4), // derived — replace if you add a cost field
      icon: getModelIcon(item.name),
      utility: item.performanceScore, // closest available proxy
      performanceScore: item.performanceScore,
    }),
  )

  return { models }
}

export async function useModel(modelId: string, prompt: string) {
  // TODO: implement when inference endpoint is ready
  await new Promise((resolve) => setTimeout(resolve, 800))
  return {
    success: true,
    modelId,
    response: `[Mock] Using ${modelId} for: "${prompt.slice(0, 40)}..."`,
  }
}