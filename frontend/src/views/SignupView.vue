<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const name = ref('')
const email = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

const signup = async () => {
  try {
    const response = await fetch('http://localhost:8000/auth/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: name.value,
        email: email.value,
        password: password.value,
        role: 'user',
        start_date: new Date().toISOString()
      }),
    })

    if (response.ok) {
      router.push('/login')
    } else {
      error.value = 'Error creating account'
    }
  } catch (e) {
    error.value = 'An error occurred during signup'
  }
}
</script>

<template>
  <div class="signup-container">
    <div class="signup-box">
      <form @submit.prevent="signup" class="instagram-form">
        <h1 class="instagram-title">Sign Up</h1>
        
        <p class="subtitle">Sign up to see and manage your assignments.</p>
        
        <div class="form-group">
          <input 
            type="text" 
            id="name"
            v-model="name"
            class="instagram-input"
            placeholder="Full Name"
            required
          >
        </div>
        
        <div class="form-group">
          <input 
            type="email" 
            id="email"
            v-model="email"
            class="instagram-input"
            placeholder="Email"
            required
          >
        </div>
        
        <div class="form-group">
          <input 
            type="password" 
            id="password"
            v-model="password"
            class="instagram-input"
            placeholder="Password"
            required
          >
        </div>
        
        <div v-if="error" class="instagram-error">
          {{ error }}
        </div>
        
        <button type="submit" class="instagram-button">
          Sign Up
        </button>
        
        <div class="separator">
          <div class="line"></div>
          <div class="or">OR</div>
          <div class="line"></div>
        </div>
      </form>
      
      <div class="login-box">
        <p>Already have an account? <router-link to="/login" class="login-link">Log in</router-link></p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.signup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: var(--ig-background);
  padding: 20px;
}

.signup-box {
  background: white;
  border: 1px solid var(--ig-border);
  border-radius: 1px;
  padding: 40px;
  max-width: 350px;
  width: 100%;
  margin-bottom: 10px;
}

.instagram-title {
  text-align: center;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 12px;
}

.subtitle {
  color: var(--ig-text-secondary);
  font-size: 14px;
  text-align: center;
  margin-bottom: 24px;
}

.form-group {
  margin-bottom: 6px;
}

.instagram-input {
  width: 100%;
  padding: 9px 8px;
  background: var(--ig-background);
  border: 1px solid var(--ig-border);
  border-radius: 3px;
  font-size: 12px;
  
  &:focus {
    border-color: #a8a8a8;
    outline: none;
  }
  
  &::placeholder {
    color: var(--ig-text-secondary);
  }
}

.instagram-button {
  width: 100%;
  background: var(--ig-primary);
  border: none;
  color: white;
  padding: 7px 16px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
  margin-top: 14px;
  cursor: pointer;
  
  &:hover {
    background: var(--ig-primary-hover);
  }
}

.instagram-error {
  color: var(--ig-error);
  font-size: 14px;
  text-align: center;
  margin: 10px 0;
}

.separator {
  display: flex;
  align-items: center;
  margin: 20px 0;
  
  .line {
    flex-grow: 1;
    height: 1px;
    background: var(--ig-border);
  }
  
  .or {
    color: var(--ig-text-secondary);
    font-size: 13px;
    font-weight: 600;
    margin: 0 18px;
    text-transform: uppercase;
  }
}

.login-box {
  background: white;
  border: 1px solid var(--ig-border);
  border-radius: 1px;
  padding: 20px;
  text-align: center;
  font-size: 14px;
  
  p {
    margin: 0;
  }
  
  .login-link {
    color: var(--ig-primary);
    text-decoration: none;
    font-weight: 600;
    
    &:hover {
      color: var(--ig-primary-hover);
    }
  }
}
</style>