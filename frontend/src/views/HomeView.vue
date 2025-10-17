
<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, RouterView } from 'vue-router'

const router = useRouter()
const menuOpen = ref(true)

const goTo = (route: string) => {
  router.push(route)
}

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}
</script>

<template>
  <div class="home-container">
    <!-- Side Menu -->
    <div class="instagram-side-menu" :class="{ closed: !menuOpen }">
      <div class="menu-header">
        <div class="menu-toggle" @click="menuOpen = !menuOpen">
          <span class="menu-icon">☰</span>
          <span class="menu-title" v-if="menuOpen">Menu</span>
        </div>
      </div>
      <nav class="instagram-nav">
        <a @click.prevent="goTo('/home/people')" class="nav-link">
          <span class="nav-icon">👥</span>
          <span class="nav-text" v-if="menuOpen">People</span>
        </a>
        <a @click.prevent="goTo('/home/assignments')" class="nav-link">
          <span class="nav-icon">📋</span>
          <span class="nav-text" v-if="menuOpen">Assignments</span>
        </a>
        <a @click.prevent="goTo('/home/privileges')" class="nav-link">
          <span class="nav-icon">🔑</span>
          <span class="nav-text" v-if="menuOpen">Privileges</span>
        </a>
        <a @click="logout" class="nav-link logout">
          <span class="nav-icon">🚪</span>
          <span class="nav-text" v-if="menuOpen">Logout</span>
        </a>
      </nav>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <RouterView />
    </div>
  </div>
</template>

<style scoped>
.home-container {
  display: flex;
  min-height: 100vh;
  background-color: var(--ig-background);
}

.instagram-side-menu {
  width: 240px;
  background-color: white;
  border-right: 1px solid var(--ig-border);
  transition: width 0.3s ease;
  padding: 20px 0;
}

.instagram-side-menu.closed {
  width: 60px;
}

.menu-header {
  padding: 0 20px 20px;
  border-bottom: 1px solid var(--ig-border);
}

.menu-toggle {
  display: flex;
  align-items: center;
  cursor: pointer;
  color: var(--ig-text);
  font-weight: 600;
}

.menu-icon {
  font-size: 24px;
  margin-right: 12px;
}

.instagram-nav {
  display: flex;
  flex-direction: column;
  margin-top: 16px;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  color: var(--ig-text);
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.2s;
  border-radius: 8px;
  margin: 0 8px;
}

.nav-link:hover {
  background-color: var(--ig-background);
}

.nav-icon {
  font-size: 20px;
  margin-right: 12px;
  width: 24px;
  text-align: center;
}

.nav-text {
  font-size: 14px;
  font-weight: 500;
}

.logout {
  margin-top: auto;
  color: var(--ig-primary);
}

.main-content {
  flex-grow: 1;
  min-height: 100vh;
  overflow-y: auto;
  background-color: var(--ig-background);
}

/* Responsive styles */
@media (max-width: 768px) {
  .instagram-side-menu {
    position: fixed;
    height: 100vh;
    z-index: 1000;
    transform: translateX(-100%);
  }

  .instagram-side-menu:not(.closed) {
    transform: translateX(0);
  }

  .main-content {
    margin-left: 0;
  }
}
</style>