<template>
  <div class="profile-container">
    <header class="profile-header">
      <button @click="goBack" class="back-btn">← Back</button>
      <h1 class="header-title">Elder's Profile</h1>
      <div class="spacer"></div>
    </header>

    <div class="profile-content">
      <div class="profile-grid">
        <!-- Left Column - Avatar and Info -->
        <div class="profile-sidebar">
          <div class="avatar-section">
            <div class="avatar-container">
              <div class="avatar" :class="{ 'avatar-female': formData.gender === 'Female' }">
                <User :size="80" v-if="formData.gender === 'Male'" />
                <UserCheck :size="80" v-else />
              </div>
              <h2 class="elder-name">{{ formData.name || 'Elder Profile' }}</h2>
              <p class="elder-subtitle">{{ formData.gender || 'Not specified' }} • {{ formData.ageRange || 'Age not set' }}</p>
            </div>
          </div>

          <!-- Quick Stats -->
          <div class="quick-stats">
            <div class="stat-item">
              <div class="stat-icon"><Heart :size="24" /></div>
              <div class="stat-info">
                <div class="stat-label">Health Conditions</div>
                <div class="stat-value">{{ formData.healthConditions.length || 0 }}</div>
              </div>
            </div>
            <div class="stat-item">
              <div class="stat-icon"><Pill :size="24" /></div>
              <div class="stat-info">
                <div class="stat-label">Medications</div>
                <div class="stat-value">{{ formData.medications.length || 0 }}</div>
              </div>
            </div>
            <div class="stat-item">
              <div class="stat-icon"><AlertCircle :size="24" /></div>
              <div class="stat-info">
                <div class="stat-label">Allergies</div>
                <div class="stat-value">{{ formData.allergies.length || 0 }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column - Form -->
        <div class="profile-form-column">
          <div class="profile-card">
        <form @submit.prevent="saveProfile" class="profile-form">
          <!-- Name and Gender Row -->
          <div class="form-row">
            <div class="form-section">
              <label class="form-label">Name</label>
              <input
                v-model="formData.name"
                type="text"
                placeholder="Enter elder's name"
                class="form-input"
              />
            </div>

            <div class="form-section">
              <label class="form-label">Gender</label>
              <select v-model="formData.gender" class="form-select">
                <option value="">Select gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
              </select>
            </div>
          </div>

          <!-- Age Range -->
          <div class="form-section">
            <label class="form-label">Age Range</label>
            <select v-model="formData.ageRange" class="form-select">
              <option value="">Select age range</option>
              <option value="60-69">60-69 years</option>
              <option value="70-79">70-79 years</option>
              <option value="80-89">80-89 years</option>
              <option value="90+">90+ years</option>
            </select>
          </div>

          <!-- Health Conditions -->
          <div class="form-section">
            <label class="form-label">Health Conditions</label>
            <div class="checkbox-group">
              <label v-for="condition in healthConditionOptions" :key="condition" class="checkbox-label">
                <input
                  type="checkbox"
                  :value="condition"
                  v-model="formData.healthConditions"
                  class="checkbox-input"
                />
                <span>{{ condition }}</span>
              </label>
            </div>
          </div>

          <!-- Custom Health Conditions -->
          <div class="form-section">
            <label class="form-label">Other Health Conditions</label>
            <p class="form-description">Add any health conditions not listed above</p>
            <div class="tags-input">
              <span
                v-for="(condition, index) in formData.customConditions"
                :key="index"
                class="tag"
              >
                {{ condition }}
                <button type="button" @click="removeTag('customConditions', index)" class="tag-remove">✕</button>
              </span>
              <input
                v-model="newCustomCondition"
                @keydown.enter.prevent="addCustomCondition"
                type="text"
                placeholder="Type and press Enter"
                class="tag-input"
              />
            </div>
          </div>

          <!-- Medications -->
          <div class="form-section">
            <label class="form-label">Current Medications</label>
            <div class="tags-input">
              <span
                v-for="(med, index) in formData.medications"
                :key="index"
                class="tag"
              >
                {{ med }}
                <button type="button" @click="removeTag('medications', index)" class="tag-remove">✕</button>
              </span>
              <input
                v-model="newMedication"
                @keydown.enter.prevent="addMedication"
                type="text"
                placeholder="Type and press Enter"
                class="tag-input"
              />
            </div>
          </div>

          <!-- Dietary Preferences -->
          <div class="form-section">
            <label class="form-label">Dietary Preferences</label>
            <div class="checkbox-group">
              <label v-for="pref in dietaryPreferenceOptions" :key="pref" class="checkbox-label">
                <input
                  type="checkbox"
                  :value="pref"
                  v-model="formData.dietaryPreferences"
                  class="checkbox-input"
                />
                <span>{{ pref }}</span>
              </label>
            </div>
          </div>

          <!-- Allergies -->
          <div class="form-section">
            <label class="form-label">Allergies</label>
            <div class="tags-input">
              <span
                v-for="(allergy, index) in formData.allergies"
                :key="index"
                class="tag"
              >
                {{ allergy }}
                <button type="button" @click="removeTag('allergies', index)" class="tag-remove">✕</button>
              </span>
              <input
                v-model="newAllergy"
                @keydown.enter.prevent="addAllergy"
                type="text"
                placeholder="Type and press Enter"
                class="tag-input"
              />
            </div>
          </div>

          <!-- Region -->
          <div class="form-section">
            <label class="form-label">Region in Uganda</label>
            <select v-model="formData.region" class="form-select">
              <option value="">Select region</option>
              <option value="Central">Central</option>
              <option value="Eastern">Eastern</option>
              <option value="Northern">Northern</option>
              <option value="Western">Western</option>
            </select>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn btn-primary">Save Profile</button>
            <button type="button" @click="resetForm" class="btn btn-secondary">Reset</button>
          </div>
        </form>

            <div v-if="saved" class="success-message">
              ✓ Profile saved successfully!
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useProfileStore } from '../stores/profile'
import { User, UserCheck, Heart, Pill, AlertCircle } from 'lucide-vue-next'

const router = useRouter()
const profileStore = useProfileStore()

const formData = ref({
  name: '',
  gender: '',
  ageRange: '',
  healthConditions: [],
  customConditions: [],
  medications: [],
  dietaryPreferences: [],
  allergies: [],
  region: ''
})

const newMedication = ref('')
const newAllergy = ref('')
const newCustomCondition = ref('')
const saved = ref(false)

const healthConditionOptions = [
  'Diabetes',
  'Hypertension',
  'Heart Disease',
  'Arthritis',
  'Osteoporosis',
  'Kidney Disease',
  'Anemia',
  'High Cholesterol'
]

const dietaryPreferenceOptions = [
  'Vegetarian',
  'Low Sodium',
  'Low Sugar',
  'Low Fat',
  'High Protein',
  'High Fiber'
]

onMounted(() => {
  profileStore.loadProfile()
  formData.value = { ...profileStore.elderProfile }
})

const goBack = () => {
  router.push({ name: 'Chat' })
}

const addMedication = () => {
  if (newMedication.value.trim()) {
    formData.value.medications.push(newMedication.value.trim())
    newMedication.value = ''
  }
}

const addAllergy = () => {
  if (newAllergy.value.trim()) {
    formData.value.allergies.push(newAllergy.value.trim())
    newAllergy.value = ''
  }
}

const addCustomCondition = () => {
  if (newCustomCondition.value.trim()) {
    formData.value.customConditions.push(newCustomCondition.value.trim())
    newCustomCondition.value = ''
  }
}

const removeTag = (field, index) => {
  formData.value[field].splice(index, 1)
}

const saveProfile = () => {
  profileStore.saveProfile(formData.value)
  saved.value = true

  setTimeout(() => {
    saved.value = false
  }, 3000)
}

const resetForm = () => {
  if (confirm('Are you sure you want to reset the profile?')) {
    profileStore.resetProfile()
    formData.value = {
      name: '',
      gender: '',
      ageRange: '',
      healthConditions: [],
      customConditions: [],
      medications: [],
      dietaryPreferences: [],
      allergies: [],
      region: ''
    }
  }
}
</script>

<style scoped>
.profile-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

.profile-header {
  background: white;
  border-bottom: 1px solid var(--color-gray-200);
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.back-btn {
  background: none;
  border: none;
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-primary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.back-btn:hover {
  color: #2d46b9;
}

.header-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #212529;
  margin: 0;
}

.spacer {
  width: 60px;
}

.profile-content {
  padding: 2rem 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
}

.profile-grid {
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: 2rem;
}

.profile-sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.avatar-section {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  border-radius: 20px;
  padding: 2.5rem 2rem;
  box-shadow: 0 10px 30px rgba(217, 0, 0, 0.2);
}

.avatar-container {
  text-align: center;
}

.avatar {
  width: 140px;
  height: 140px;
  background: rgba(255, 255, 255, 0.2);
  border: 4px solid var(--color-white);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem auto;
  color: var(--color-white);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.avatar-female {
  background: linear-gradient(135deg, rgba(252, 220, 4, 0.3) 0%, rgba(252, 220, 4, 0.1) 100%);
  border-color: var(--color-secondary);
}

.elder-name {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-white);
  margin: 0 0 0.5rem 0;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.elder-subtitle {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  font-weight: 500;
}

.quick-stats {
  background: white;
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border-radius: 12px;
  border: 2px solid var(--color-gray-100);
  transition: all 0.3s ease;
}

.stat-item:hover {
  transform: translateX(5px);
  border-color: var(--color-primary);
}

.stat-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.stat-info {
  flex: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: var(--color-gray-600);
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-dark);
}

.profile-form-column {
  min-width: 0;
}

.profile-card {
  background: white;
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.form-input {
  padding: 0.875rem 1rem;
  border: 2px solid var(--color-gray-200);
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(217, 0, 0, 0.1);
}

.form-label {
  font-size: 1rem;
  font-weight: 600;
  color: #212529;
}

.form-select {
  padding: 0.875rem 1rem;
  border: 2px solid var(--color-gray-200);
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
  cursor: pointer;
}

.form-select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.1);
}

.checkbox-group {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0.75rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  border: 2px solid var(--color-gray-200);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.checkbox-label:hover {
  border-color: var(--color-primary);
  background: var(--color-gray-50);
}

.checkbox-input {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.checkbox-input:checked + span {
  font-weight: 600;
  color: var(--color-primary);
}

.tags-input {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  padding: 0.75rem;
  border: 2px solid var(--color-gray-200);
  border-radius: 10px;
  min-height: 50px;
  transition: all 0.3s ease;
}

.tags-input:focus-within {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.1);
}

.tag {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: var(--color-gray-100);
  color: var(--color-primary);
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
}

.tag-remove {
  background: none;
  border: none;
  color: var(--color-primary);
  cursor: pointer;
  font-size: 1rem;
  line-height: 1;
  padding: 0;
}

.tag-input {
  flex: 1;
  min-width: 150px;
  border: none;
  outline: none;
  font-size: 1rem;
  padding: 0.5rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.btn {
  flex: 1;
  padding: 1rem;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.btn-primary {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(67, 97, 238, 0.3);
}

.btn-secondary {
  background: white;
  color: #6c757d;
  border: 2px solid var(--color-gray-200);
}

.btn-secondary:hover {
  background: var(--color-gray-50);
  border-color: #adb5bd;
}

.success-message {
  margin-top: 1.5rem;
  padding: 1rem;
  background: #d1e7dd;
  color: #0f5132;
  border-radius: 10px;
  text-align: center;
  font-weight: 600;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 1200px) {
  .profile-grid {
    grid-template-columns: 300px 1fr;
    gap: 1.5rem;
  }
}

@media (max-width: 1024px) {
  .profile-grid {
    grid-template-columns: 1fr;
  }

  .profile-sidebar {
    max-width: 600px;
    margin: 0 auto;
  }
}

@media (max-width: 768px) {
  .profile-content {
    padding: 1rem;
  }

  .profile-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  .profile-sidebar {
    max-width: 100%;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
  }

  .avatar-section {
    padding: 1rem;
  }

  .avatar {
    width: 60px;
    height: 60px;
  }

  .avatar svg {
    width: 32px;
    height: 32px;
  }

  .elder-name {
    font-size: 0.875rem;
    margin: 0 0 0.25rem 0;
  }

  .elder-subtitle {
    font-size: 0.625rem;
  }

  .quick-stats {
    padding: 0.75rem;
    gap: 0.5rem;
  }

  .stat-item {
    padding: 0.5rem;
    gap: 0.5rem;
  }

  .stat-icon {
    width: 32px;
    height: 32px;
  }

  .stat-icon svg {
    width: 16px;
    height: 16px;
  }

  .stat-label {
    font-size: 0.625rem;
  }

  .stat-value {
    font-size: 1rem;
  }

  .profile-card {
    padding: 1rem;
  }

  .profile-form {
    gap: 1rem;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .form-section {
    gap: 0.5rem;
  }

  .form-label {
    font-size: 0.875rem;
  }

  .form-input,
  .form-select {
    padding: 0.625rem;
    font-size: 0.875rem;
  }

  .checkbox-group {
    grid-template-columns: 1fr;
  }

  .checkbox-label {
    padding: 0.5rem;
    font-size: 0.875rem;
  }

  .tags-input {
    padding: 0.5rem;
    font-size: 0.875rem;
  }

  .tag {
    font-size: 0.75rem;
    padding: 0.375rem 0.5rem;
  }

  .form-actions {
    flex-direction: column;
    gap: 0.5rem;
  }

  .btn {
    padding: 0.75rem;
    font-size: 0.875rem;
  }
}
</style>
