<template>
  <div class="profile-container">
    <header class="profile-header">
      <button @click="goBack" class="back-btn">← Back</button>
      <h1 class="header-title">Elder's Profile</h1>
      <div class="spacer"></div>
    </header>

    <div class="profile-content">
      <div class="profile-card">
        <p class="card-subtitle">
          Update the elder's information to get personalized nutritional recommendations
        </p>

        <form @submit.prevent="saveProfile" class="profile-form">
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
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useProfileStore } from '../stores/profile'

const router = useRouter()
const profileStore = useProfileStore()

const formData = ref({
  ageRange: '',
  healthConditions: [],
  medications: [],
  dietaryPreferences: [],
  allergies: [],
  region: ''
})

const newMedication = ref('')
const newAllergy = ref('')
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
      ageRange: '',
      healthConditions: [],
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
  background: #f8f9fa;
}

.profile-header {
  background: white;
  border-bottom: 1px solid #dee2e6;
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
  color: #4361ee;
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
  max-width: 800px;
  margin: 0 auto;
}

.profile-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.card-subtitle {
  color: #6c757d;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.form-label {
  font-size: 1rem;
  font-weight: 600;
  color: #212529;
}

.form-select {
  padding: 0.875rem 1rem;
  border: 2px solid #dee2e6;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
  cursor: pointer;
}

.form-select:focus {
  outline: none;
  border-color: #4361ee;
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
  border: 2px solid #dee2e6;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.checkbox-label:hover {
  border-color: #4361ee;
  background: #f8f9fa;
}

.checkbox-input {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.checkbox-input:checked + span {
  font-weight: 600;
  color: #4361ee;
}

.tags-input {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  padding: 0.75rem;
  border: 2px solid #dee2e6;
  border-radius: 10px;
  min-height: 50px;
  transition: all 0.3s ease;
}

.tags-input:focus-within {
  border-color: #4361ee;
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.1);
}

.tag {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: #e7f3ff;
  color: #4361ee;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
}

.tag-remove {
  background: none;
  border: none;
  color: #4361ee;
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
  background: linear-gradient(135deg, #4361ee 0%, #4cc9f0 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(67, 97, 238, 0.3);
}

.btn-secondary {
  background: white;
  color: #6c757d;
  border: 2px solid #dee2e6;
}

.btn-secondary:hover {
  background: #f8f9fa;
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

@media (max-width: 768px) {
  .checkbox-group {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>
