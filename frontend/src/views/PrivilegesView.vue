<script setup lang="ts">
import { ref, onMounted } from 'vue'

const privileges = ref([])
const error = ref('')
const showModal = ref(false)
const isEdit = ref(false)
const form = ref({
  id: null,
  user_id: null,
  privilege_date: '',
  privilege_part: '',
  created_by: null,
  room_number: null,
  additional_notes: '',
  privilege_sent: false
})
const deleteId = ref<number|null>(null)
const showDeleteConfirm = ref(false)

const fetchPrivileges = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      error.value = 'No authentication token found'
      return
    }

    const res = await fetch('http://localhost:8000/privileges/', {
      headers: { 
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}))
      throw new Error(errorData.detail || 'Error loading privileges')
    }

    const data = await res.json()
    privileges.value = Array.isArray(data) ? data : []
  } catch (e: unknown) {
    console.error('Error fetching privileges:', e)
    if (e instanceof Error) {
      error.value = e.message
    } else {
      error.value = 'Could not load information.'
    }
  }
}

onMounted(fetchPrivileges)

const openAdd = () => {
  isEdit.value = false
  showModal.value = true
  Object.assign(form.value, {
    id: null,
    user_id: null,
    privilege_date: '',
    privilege_part: '',
    created_by: null,
    room_number: null,
    additional_notes: '',
    privilege_sent: false
  })
}

const openEdit = (privilege: any) => {
  isEdit.value = true
  showModal.value = true
  Object.assign(form.value, privilege)
}

const savePrivilege = async () => {
  const token = localStorage.getItem('token')
  const url = isEdit.value
    ? `http://localhost:8000/privileges/${form.value.id}`
    : 'http://localhost:8000/privileges/'
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
    await fetchPrivileges()
  } else {
    alert('Error saving privilege')
  }
}

const confirmDelete = (id: number) => {
  deleteId.value = id
  showDeleteConfirm.value = true
}

const deletePrivilege = async () => {
  const token = localStorage.getItem('token')
  const res = await fetch(`http://localhost:8000/privileges/${deleteId.value}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    showDeleteConfirm.value = false
    await fetchPrivileges()
  } else {
    alert('Error deleting privilege')
  }
}
</script>
<template>
  <div class="instagram-container">
    <div class="instagram-header">
      <h2>Privileges</h2>
      <button @click="openAdd" class="instagram-button">
        <span class="add-icon">+</span> New Privilege
      </button>
    </div>

    <div v-if="error" class="instagram-error">
      {{ error }}
    </div>
    
    <div class="instagram-card-list">
      <div v-for="p in privileges" :key="p.id" class="instagram-card">
        <div class="card-header">
          <div class="user-info">
            <div class="user-avatar">{{ p.user_id?.charAt(0)?.toUpperCase() || 'U' }}</div>
            <span class="username">{{ p.user_id || 'Unknown User' }}</span>
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
            <span class="label">Date:</span>
            <span class="value">{{ p.privilege_date || 'Not set' }}</span>
          </div>
          <div class="content-row">
            <span class="label">Part:</span>
            <span class="value">{{ p.privilege_part || 'Not set' }}</span>
          </div>
          <div class="content-row">
            <span class="label">Room:</span>
            <span class="value">{{ p.room_number || 'Not set' }}</span>
          </div>
          <div class="content-row">
            <span class="label">Status:</span>
            <span :class="['status-badge', p.privilege_sent ? 'status-sent' : 'status-pending']">
              {{ p.privilege_sent ? 'Sent' : 'Pending' }}
            </span>
          </div>
          <div class="content-row" v-if="p.additional_notes">
            <span class="label">Notes:</span>
            <span class="value">{{ p.additional_notes }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Form Modal -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h3>{{ isEdit ? 'Edit' : 'Add' }} Privilege</h3>
        <form @submit.prevent="savePrivilege">
          <input v-model="form.user_id" placeholder="User ID" required />
          <input v-model="form.privilege_date" placeholder="Privilege Date" type="datetime-local" />
          <input v-model="form.privilege_part" placeholder="Privilege Part" />
          <input v-model="form.created_by" placeholder="Created By (ID)" />
          <input v-model="form.room_number" placeholder="Room Number" />
          <input v-model="form.additional_notes" placeholder="Additional Notes" />
          <label><input type="checkbox" v-model="form.privilege_sent" /> Privilege Sent</label>
          <div style="margin-top:1em;">
            <button type="submit">Save</button>
            <button type="button" @click="showModal = false">Cancel</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteConfirm" class="modal">
      <div class="modal-content">
        <p>Are you sure you want to delete this privilege?</p>
        <button @click="deletePrivilege">Yes, delete</button>
        <button @click="showDeleteConfirm = false">Cancel</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal-content {
  background: #fff;
  padding: 2em;
  border-radius: 8px;
  min-width: 300px;
}
</style>