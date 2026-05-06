const BASE_URL = 'http://localhost:8080/api/auth/users'

export async function apiLogin(email: string, password: string) {
  const res = await fetch(`${BASE_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, motDePasse: password }),
  })

  if (!res.ok) {
    const err = await res.text()
    throw new Error(err || 'Login failed')
  }

  return res.json()
}

export async function apiRegister(data: {
  email: string
  motDePasse: string
  prenom: string
  nom: string
  statut?: string
  budget?: number
  adresse?: string
}) {
  const res = await fetch(`${BASE_URL}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })

  if (!res.ok) {
    const err = await res.text()
    throw new Error(err || 'Registration failed')
  }

  return res.json()
}