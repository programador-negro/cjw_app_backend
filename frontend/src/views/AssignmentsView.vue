<script setup lang="ts">
import { ref, onMounted } from 'vue'

const assignments = ref([])
const error = ref('')
const showModal = ref(false)
const isEdit = ref(false)
const form = ref({
  id: null,
  user_id: null,
  assignment_date: '',
  assignment_part: '',
  created_by: null,
  room_number: null,
  additional_notes: '',
  assignment_sent: false
})
const deleteId = ref<number|null>(null)
const showDeleteConfirm = ref(false)

const fetchAssignments = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      error.value = 'No authentication token found'
      return
    }

    const res = await fetch('http://localhost:8000/assignments/', {
      headers: { 
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    if (!res.ok) {
      if (res.status === 401) {
        error.value = 'Session expired. Please login again.'
        // Optionally redirect to login
        return
      }
      const errorData = await res.json().catch(() => ({}))
      throw new Error(errorData.detail || `Error loading assignments (${res.status})`)
    }

    const data = await res.json()
    if (!Array.isArray(data)) {
      console.error('Unexpected data format:', data)
      error.value = 'Server returned invalid data format'
      assignments.value = []
      return
    }

    // Validate and transform data
    assignments.value = data.map(assignment => ({
      id: assignment.id,
      user_id: assignment.user_id || 'Unknown User',
      assignment_date: assignment.assignment_date || null,
      assignment_part: assignment.assignment_part || '',
      created_by: assignment.created_by,
      room_number: assignment.room_number,
      additional_notes: assignment.additional_notes || '',
      assignment_sent: Boolean(assignment.assignment_sent)
    }))
  } catch (e: unknown) {
    console.error('Error fetching assignments:', e)
    if (e instanceof Error) {
      error.value = e.message
    } else {
      error.value = 'Could not load information.'
    }
    assignments.value = []
  }
}

onMounted(fetchAssignments)

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

const openAdd = () => {
  isEdit.value = false
  showModal.value = true
  Object.assign(form.value, {
    id: null,
    user_id: null,
    assignment_date: '',
    assignment_part: '',
    created_by: null,
    room_number: null,
    additional_notes: '',
    assignment_sent: false
  })
}

const openEdit = (assignment: any) => {
  isEdit.value = true
  showModal.value = true
  Object.assign(form.value, assignment)
}

const saveAssignment = async () => {
  const token = localStorage.getItem('token')
  const url = isEdit.value
    ? `http://localhost:8000/assignments/${form.value.id}`
    : 'http://localhost:8000/assignments/'
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
    await fetchAssignments()
  } else {
    alert('Error saving assignment')
  }
}

const confirmDelete = (id: number) => {
  deleteId.value = id
  showDeleteConfirm.value = true
}

const deleteAssignment = async () => {
  const token = localStorage.getItem('token')
  const res = await fetch(`http://localhost:8000/assignments/${deleteId.value}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` }
  })
  if (res.ok) {
    showDeleteConfirm.value = false
    await fetchAssignments()
  } else {
    alert('Error deleting assignment')
  }
}
</script>
<template>
  <div class="instagram-container">
    <div class="instagram-header">
      <h2>Assignments</h2>
      <button @click="openAdd" class="instagram-button">
        <span class="add-icon">+</span> New Assignment
      </button>
    </div>

    <div v-if="error" class="instagram-error">
      {{ error }}
    </div>
    
    <div class="instagram-card-list">
      <div v-for="a in assignments" :key="a.id" class="instagram-card">
        <div class="card-header">
          <div class="user-info">
            <div class="user-avatar">{{ a.user_id.charAt(0).toUpperCase() }}</div>
            <span class="username">{{ a.user_id }}</span>
          </div>
          <div class="card-actions">
            <button @click="openEdit(a)" class="action-button">
              <span>✏️</span>
            </button>
            <button @click="confirmDelete(a.id)" class="action-button">
              <span>🗑️</span>
            </button>
          </div>
        </div>
        
        <div class="card-content">
          <div class="content-row">
            <span class="label">Date:</span>
            <span class="value">{{ formatDate(a.assignment_date) }}</span>
          </div>
          <div class="content-row">
            <span class="label">Part:</span>
            <span class="value">{{ a.assignment_part }}</span>
          </div>
          <div class="content-row">
            <span class="label">Room:</span>
            <span class="value">{{ a.room_number }}</span>
          </div>
          <div class="content-row">
            <span class="label">Status:</span>
            <span :class="['status-badge', a.assignment_sent ? 'status-sent' : 'status-pending']">
              {{ a.assignment_sent ? 'Sent' : 'Pending' }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Form Modal -->
    <div v-if="showModal" class="instagram-modal">
      <div class="instagram-modal-content">
        <div class="modal-header">
          <h3>{{ isEdit ? 'Edit' : 'New' }} Assignment</h3>
          <button class="modal-close" @click="showModal = false">&times;</button>
        </div>
        
        <form @submit.prevent="saveAssignment" class="instagram-form">
          <div class="form-group">
            <input 
              v-model="form.user_id" 
              class="instagram-input"
              placeholder="User ID" 
              required 
            />
          </div>
          
          <div class="form-group">
            <input 
              v-model="form.assignment_date" 
              class="instagram-input"
              type="datetime-local" 
              placeholder="Assignment Date"
            />
          </div>
          
          <div class="form-group">
            <input 
              v-model="form.assignment_part" 
              class="instagram-input"
              placeholder="Assignment Part"
            />
          </div>
          
          <div class="form-group">
            <input 
              v-model="form.room_number" 
              class="instagram-input"
              placeholder="Room Number"
            />
          </div>
          
          <div class="form-group">
            <textarea 
              v-model="form.additional_notes" 
              class="instagram-input"
              placeholder="Additional Notes"
              rows="3"
            ></textarea>
          </div>
          
          <div class="form-group checkbox-group">
            <label class="instagram-checkbox">
              <input type="checkbox" v-model="form.assignment_sent" />
              <span class="checkbox-label">Assignment Sent</span>
            </label>
          </div>

          <div class="modal-footer">
            <button type="submit" class="instagram-button">
              {{ isEdit ? 'Save Changes' : 'Create Assignment' }}
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
          <h3>Delete Assignment</h3>
          <button class="modal-close" @click="showDeleteConfirm = false">&times;</button>
        </div>
        
        <div class="modal-body">
          <p>Are you sure you want to delete this assignment?</p>
          <p class="text-muted">This action cannot be undone.</p>
        </div>
        
        <div class="modal-footer">
          <button @click="deleteAssignment" class="instagram-button-danger">
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

.instagram-container {
  max-width: 935px;
  margin: 0 auto;
  padding: 20px;
}

.instagram-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 0 20px;
  
  h2 {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 24px;
    font-weight: 600;
  }
}

.instagram-button {
  background: var(--ig-primary);
  border: none;
  color: white;
  padding: 7px 16px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  
  &:hover {
    background: var(--ig-primary-hover);
  }
  
  .add-icon {
    font-size: 18px;
  }
}

.instagram-error {
  background: var(--ig-error);
  color: white;
  padding: 12px;
  border-radius: 4px;
  margin: 20px;
  text-align: center;
}

.instagram-card-list {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}

.instagram-card {
  background: white;
  border: 1px solid var(--ig-border);
  border-radius: 3px;
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-bottom: 1px solid var(--ig-border);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 32px;
  height: 32px;
  background: var(--ig-primary);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.username {
  font-weight: 600;
  font-size: 14px;
  color: var(--ig-text);
}

.card-actions {
  display: flex;
  gap: 8px;
}

.action-button {
  background: none;
  border: none;
  padding: 4px;
  cursor: pointer;
  font-size: 16px;
  
  &:hover {
    opacity: 0.7;
  }
}

.card-content {
  padding: 12px;
}

.content-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid var(--ig-border);
  
  &:last-child {
    border-bottom: none;
  }
}

.label {
  color: var(--ig-text-secondary);
  font-size: 14px;
}

.value {
  font-size: 14px;
  font-weight: 500;
  color: var(--ig-text);
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.status-sent {
  background-color: var(--ig-success);
  color: white;
}

.status-pending {
  background-color: var(--ig-background);
  border: 1px solid var(--ig-border);
  color: var(--ig-text-secondary);
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Responsive styles */
@media (max-width: 768px) {
  .instagram-modal-content {
    margin: 20px;
    max-height: calc(100vh - 40px);
    overflow-y: auto;
  }

  .instagram-header {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }

  .instagram-card-list {
    grid-template-columns: 1fr;
  }
}
</style>

<style>
/* Global styles needed for the instagram theme */
:root {
  --ig-primary: #0095f6;
  --ig-primary-hover: #1877f2;
  --ig-background: #fafafa;
  --ig-border: #dbdbdb;
  --ig-text: #262626;
  --ig-text-secondary: #8e8e8e;
  --ig-error: #ed4956;
  --ig-success: #70c050;
}
</style>