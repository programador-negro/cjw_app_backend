<script setup lang="ts">
import { ref, onMounted } from 'vue'

const people = ref([])
const loading = ref(true)
const error = ref('')
const showModal = ref(false)
const isEdit = ref(false)
const form = ref({
  id: null,
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  contact_name: '',
  contact_phone: '',
  has_whatsapp: false,
  address: '',
  congregation: '',
  user_id: null,
  current_level: ''
})
const deleteId = ref<number|null>(null)
const showDeleteConfirm = ref(false)

const fetchPeople = async () => {
  loading.value = true
  try {
    const token = localStorage.getItem('token')
    const res = await fetch('http://localhost:8000/people/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (!res.ok) throw new Error('Error loading people')
    people.value = await res.json()
  } catch (e) {
    error.value = 'Could not load information.'
  } finally {
    loading.value = false
  }
}

onMounted(fetchPeople)

const openAdd = () => {
  isEdit.value = false
  showModal.value = true
  Object.assign(form.value, {
    id: null,
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    contact_name: '',
    contact_phone: '',
    has_whatsapp: false,
    address: '',
    congregation: '',
    user_id: null,
    current_level: ''
  })
}

const openEdit = (person: any) => {
  isEdit.value = true
  showModal.value = true
  Object.assign(form.value, person)
}

const savePerson = async () => {
  const token = localStorage.getItem('token')
  const url = isEdit.value
    ? `http://localhost:8000/people/${form.value.id}`
    : 'http://localhost:8000/people/'
  const method = isEdit.value ? 'PUT' : 'POST'
  const res = await fetch(url, {
    method,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(form.value)
  })
  if (res.ok) {
    showModal.value = false
    await fetchPeople()
  } else {
    alert('Error saving person')
  }
}

const confirmDelete = (id: number) => {
  deleteId.value = id
  showDeleteConfirm.value = true
}

const deletePerson = async () => {
  const token = localStorage.getItem('token')
  const res = await fetch(`http://localhost:8000/people/${deleteId.value}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    showDeleteConfirm.value = false
    await fetchPeople()
  } else {
    alert('Error deleting person')
  }
}
</script>
<template>
  <div class="instagram-container">
    <div class="instagram-header">
      <h2>People</h2>
      <button @click="openAdd" class="instagram-button">
        <span class="add-icon">+</span> New Person
      </button>
    </div>

    <div v-if="loading" class="instagram-loading">
      <div class="loading-spinner"></div>
      <span>Loading...</span>
    </div>
    
    <div v-else-if="error" class="instagram-error">
      {{ error }}
    </div>
    
    <div v-else class="instagram-card-list">
      <div v-for="p in people" :key="p.id" class="instagram-card">
        <div class="card-header">
          <div class="user-info">
            <div class="user-avatar">{{ p.first_name.charAt(0).toUpperCase() }}</div>
            <span class="username">{{ p.first_name }} {{ p.last_name }}</span>
          </div>
          <div class="card-actions">
            <button @click="openEdit(p)" class="action-button">
              <span>✏️</span>
            </button>
            <button @click="confirmDelete(p.id)" class="action-button">
              <span>🗑️</span>
            </button>
          </div>
        </div>
        
        <div class="card-content">
          <div class="content-row">
            <span class="label">Email:</span>
            <span class="value">{{ p.email }}</span>
          </div>
          <div class="content-row">
            <span class="label">Phone:</span>
            <span class="value">{{ p.phone }}</span>
          </div>
          <div class="content-row">
            <span class="label">WhatsApp:</span>
            <span class="value">{{ p.has_whatsapp ? '✓' : '✗' }}</span>
          </div>
          <div class="content-row">
            <span class="label">Congregation:</span>
            <span class="value">{{ p.congregation }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Form Modal -->
    <div v-if="showModal" class="instagram-modal">
      <div class="instagram-modal-content">
        <div class="modal-header">
          <h3>{{ isEdit ? 'Edit' : 'New' }} Person</h3>
          <button class="modal-close" @click="showModal = false">&times;</button>
        </div>
        
        <form @submit.prevent="savePerson" class="instagram-form">
          <div class="form-group">
            <input v-model="form.first_name" class="instagram-input" placeholder="First Name" required />
          </div>
          
          <div class="form-group">
            <input v-model="form.last_name" class="instagram-input" placeholder="Last Name" required />
          </div>

          <div class="form-group">
            <input v-model="form.email" type="email" class="instagram-input" placeholder="Email" />
          </div>
          
          <div class="form-group">
            <input v-model="form.phone" class="instagram-input" placeholder="Phone" />
          </div>

          <div class="form-group">
            <input v-model="form.contact_name" class="instagram-input" placeholder="Contact Name" />
          </div>
          
          <div class="form-group">
            <input v-model="form.contact_phone" class="instagram-input" placeholder="Contact Phone" />
          </div>

          <div class="form-group checkbox-group">
            <label class="instagram-checkbox">
              <input type="checkbox" v-model="form.has_whatsapp" />
              <span class="checkbox-label">Has WhatsApp</span>
            </label>
          </div>

          <div class="form-group">
            <textarea v-model="form.address" class="instagram-input" rows="2" placeholder="Address"></textarea>
          </div>

          <div class="form-group">
            <input v-model="form.congregation" class="instagram-input" placeholder="Congregation" />
          </div>
          
          <div class="form-group">
            <input v-model="form.current_level" class="instagram-input" placeholder="Current Level" />
          </div>

          <div class="modal-footer">
            <button type="submit" class="instagram-button">
              {{ isEdit ? 'Save Changes' : 'Create Person' }}
            </button>
            <button type="button" class="instagram-button-secondary" @click="showModal = false">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteConfirm" class="instagram-modal">
      <div class="instagram-modal-content confirmation-modal">
        <div class="modal-header">
          <h3>Delete Person</h3>
          <button class="modal-close" @click="showDeleteConfirm = false">&times;</button>
        </div>
        
        <div class="modal-body">
          <p>Are you sure you want to delete this person?</p>
          <p class="text-muted">This action cannot be undone.</p>
        </div>
        
        <div class="modal-footer">
          <button @click="deletePerson" class="instagram-button-danger">
            Delete
          </button>
          <button @click="showDeleteConfirm = false" class="instagram-button-secondary">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Instagram Modal Styles */
.instagram-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.instagram-modal-content {
  background: white;
  border-radius: 12px;
  width: 100%;
  max-width: 400px;
  padding: 20px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--ig-border);
  
  h3 {
    font-size: 16px;
    font-weight: 600;
    margin: 0;
  }
}

.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: var(--ig-text-secondary);
  padding: 0;
  
  &:hover {
    color: var(--ig-text);
  }
}

.instagram-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.form-group {
  margin-bottom: 12px;
}

.checkbox-group {
  display: flex;
  align-items: center;
  padding: 8px 0;
}

.instagram-checkbox {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
  
  input[type="checkbox"] {
    margin-right: 8px;
  }
  
  .checkbox-label {
    color: var(--ig-text);
    font-size: 14px;
  }
}

.modal-footer {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid var(--ig-border);
}

.instagram-button-secondary {
  background: none;
  border: none;
  color: var(--ig-text-secondary);
  padding: 7px 16px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  
  &:hover {
    color: var(--ig-text);
  }
}

.instagram-button-danger {
  background: var(--ig-error);
  border: none;
  color: white;
  padding: 7px 16px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  
  &:hover {
    opacity: 0.9;
  }
}

.confirmation-modal {
  max-width: 300px;
  text-align: center;
}

.modal-body {
  margin: 20px 0;
  
  p {
    margin: 10px 0;
    
    &.text-muted {
      color: var(--ig-text-secondary);
      font-size: 13px;
    }
  }
}

/* Responsive styles */
@media (max-width: 768px) {
  .instagram-modal-content {
    margin: 20px;
    max-height: calc(100vh - 40px);
    overflow-y: auto;
  }
}
</style>

<style>
.instagram-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(0, 0, 0, 0.6);
  z-index: 1000;
}
</style>