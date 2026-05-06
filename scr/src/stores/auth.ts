import { defineStore } from 'pinia'
import { ref } from 'vue'

export type UserRole = 'admin' | 'employee'

interface User {
  name: string
  username: string
  email: string
  role: UserRole
  city: string
  country: string
  avatar?: string
}

// Fake users for demo
const FAKE_USERS: Record<string, { password: string; profile: User }> = {
  ewan: {
    password: 'admin',
    profile: {
      name: 'Ewan',
      username: 'ewan',
      email: 'ewan@greenllm.com',
      role: 'admin',
      city: 'Paris',
      country: 'France',
    },
  },
  jaime: {
    password: 'emp',
    profile: {
      name: 'Jaime Rey',
      username: 'jaime',
      email: 'jaime@greenllm.com',
      role: 'employee',
      city: 'San Jose',
      country: 'USA',
    },
  },
}

export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref(false)
  const currentUser = ref<User | null>(null)
/*
  function login(username: string, password: string): boolean {
    const match = FAKE_USERS[username]
    if (match && match.password === password) {
      isAuthenticated.value = true
      currentUser.value = match.profile
      return true
    }
    return false
  }
*/
  async function login(email: string, motDePasse: string): Promise<User | null> {
    const url = 'http://localhost:8080/api/auth/users/login';
    
    const loginData = {
        email: email,
        motDePasse: motDePasse 
    };

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(loginData)
        });

        if (response.ok) {
            // El "as User" no es estrictamente necesario si confías en la respuesta, 
            // pero declaramos explícitamente el tipo de retorno.
            const user: User = await response.json();
            
            console.log(`Bienvenido ${user.name}, tu rol es ${user.role}`);
            
            // Aquí puedes guardar los datos en el estado global (Redux, Context) 
            // o en el LocalStorage
            localStorage.setItem('userData', JSON.stringify(user));
            
            return user;
        } else {
            console.error("Credenciales inválidas");
            return null;
        }
    } catch (error) {
        console.error("Error al conectar con el servidor:", error);
        return null;
    }
}
  function register(userData: Omit<User, 'role'> & { password: string }): boolean {
    isAuthenticated.value = true
    currentUser.value = {
      ...userData,
      role: 'employee', // new registrations are employees by default
    }
    return true
  }

  function logout() {
    isAuthenticated.value = false
    currentUser.value = null
  }

  return { isAuthenticated, currentUser, login, register, logout }
})