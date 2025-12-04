import { createI18n } from 'vue-i18n'
import eng from './locales/eng.json'
import lug from './locales/lug.json'
import nyn from './locales/nyn.json'
import ach from './locales/ach.json'
import teo from './locales/teo.json'
import lgg from './locales/lgg.json'

// Get saved language from localStorage or default to English
const savedLanguage = localStorage.getItem('preferred_language') || 'eng'

const i18n = createI18n({
    legacy: false, // Use Composition API
    locale: savedLanguage,
    fallbackLocale: 'eng',
    messages: {
        eng,
        lug,
        nyn,
        ach,
        teo,
        lgg
    }
})

export default i18n
