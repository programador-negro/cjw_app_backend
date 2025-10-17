<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

const login = async () => {
  try {
    const response = await fetch('http://localhost:8000/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email.value,
        password: password.value
      }),
    })

    if (response.ok) {
      const data = await response.json()
      localStorage.setItem('token', data.token)
      router.push('/home')
    } else {
      error.value = 'Invalid credentials'
    }
  } catch (e) {
    error.value = 'An error occurred during login'
  }
}
</script>

<template>
  <div class="login-container">
    <div class="login-box">
      <form @submit.prevent="login" class="login-form">
        <h1 class="instagram-logo">App Name</h1>
        
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
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <button type="submit" class="instagram-button">
          Log In
        </button>
        
        <div class="separator">
          <div class="line"></div>
          <div class="or">OR</div>
          <div class="line"></div>
        </div>
        
      </form>
      
      <div class="signup-box">
        <p>Don't have an account? <router-link to="/signup" class="signup-link">Sign up</router-link></p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #fafafa;
  padding: 20px;
}

.login-box {
  background: #fff;
  border: 1px solid #dbdbdb;
  border-radius: 1px;
  padding: 40px;
  max-width: 350px;
  width: 100%;
  margin-bottom: 10px;
}

.instagram-logo {
  text-align: center;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 6px;
}

.instagram-input {
  width: 100%;
  padding: 9px 8px;
  background: #fafafa;
  border: 1px solid #dbdbdb;
  border-radius: 3px;
  font-size: 12px;
  
  &:focus {
    border-color: #a8a8a8;
    outline: none;
  }
  
  &::placeholder {
    color: #8e8e8e;
  }
}

.instagram-button {
  width: 100%;
  background: #0095f6;
  border: none;
  color: white;
  padding: 7px 16px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
  margin-top: 14px;
  cursor: pointer;
  
  &:hover {
    background: #1877f2;
  }
}

.separator {
  display: flex;
  align-items: center;
  margin: 20px 0;
  
  .line {
    flex-grow: 1;
    height: 1px;
    background: #dbdbdb;
  }
  
  .or {
    color: #8e8e8e;
    font-size: 13px;
    font-weight: 600;
    margin: 0 18px;
    text-transform: uppercase;
  }
}

.error-message {
  color: #ed4956;
  font-size: 14px;
  text-align: center;
  margin: 10px 0;
}

.signup-box {
  background: #fff;
  border: 1px solid #dbdbdb;
  border-radius: 1px;
  padding: 20px;
  text-align: center;
  font-size: 14px;
  
  p {
    margin: 0;
  }
  
  .signup-link {
    color: #0095f6;
    text-decoration: none;
    font-weight: 600;
    
    &:hover {
      color: #1877f2;
    }
  }
}
</style>