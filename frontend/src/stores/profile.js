import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useProfileStore = defineStore('profile', () => {
  const elderProfile = ref({
    name: '',
    gender: '',
    ageRange: '',
    healthConditions: [],
    medications: [],
    dietaryPreferences: [],
    allergies: [],
    region: ''
  })

  const loadProfile = () => {
    const saved = localStorage.getItem('elder_profile')
    if (saved) {
      elderProfile.value = JSON.parse(saved)
    }
  }

  const saveProfile = (profileData) => {
    elderProfile.value = { ...elderProfile.value, ...profileData }
    localStorage.setItem('elder_profile', JSON.stringify(elderProfile.value))
  }

  const updateField = (field, value) => {
    elderProfile.value[field] = value
    localStorage.setItem('elder_profile', JSON.stringify(elderProfile.value))
  }

  const resetProfile = () => {
    elderProfile.value = {
      name: '',
      gender: '',
      ageRange: '',
      healthConditions: [],
      medications: [],
      dietaryPreferences: [],
      allergies: [],
      region: ''
    }
    localStorage.removeItem('elder_profile')
  }

  return {
    elderProfile,
    loadProfile,
    saveProfile,
    updateField,
    resetProfile
  }
})
