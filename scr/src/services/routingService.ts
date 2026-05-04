// src/services/routingService.ts
// Replace these with real API calls later

export async function getModels() {
  return [
    {
      id: 1,
      name: 'Mistral 7B',
      tag: 'The best deal',
      co2: 0.02,
      power: 'Low',
      cost: 0.003,
      icon: 'https://upload.wikimedia.org/wikipedia/commons/e/e5/Mistral_AI_logo.svg',
    },
    {
      id: 2,
      name: 'Bloom 172B',
      tag: 'The most powerful',
      co2: 1,
      power: 'High',
      cost: 0.03,
      icon: 'https://huggingface.co/front/assets/huggingface_logo-noborder.svg',
    },
    {
      id: 3,
      name: 'Qwen 2.5',
      tag: 'The most balanced',
      co2: 0.5,
      power: 'Medium',
      cost: 0.3,
      icon: 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Qwen_logo.svg/200px-Qwen_logo.svg.png',
    },
  ]
}

export async function getQuota() {
  return { remaining: 10000, total: 10000 }
}

// This will call your carbon routing service later
export async function submitPrompt(prompt: string, mode: 'router' | 'chat') {
  // TODO: replace with real carbon routing API call
  // e.g. POST /api/route { prompt, mode }
  await new Promise((resolve) => setTimeout(resolve, 500))
  return {
    models: await getModels(),
    charCount: prompt.length,
  }
}

export async function useModel(modelId: number, prompt: string) {
  // TODO: replace with real API call
  // e.g. POST /api/inference { modelId, prompt }
  await new Promise((resolve) => setTimeout(resolve, 800))
  return {
    success: true,
    modelId,
    response: `[Mock response from model ${modelId}] for: "${prompt.slice(0, 30)}..."`,
  }
}