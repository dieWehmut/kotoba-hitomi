<!-- filepath: vue-chat/src/components/function/SettingsModal.vue -->
<template>
  <div class="modal-mask" @click.self="close">
    <div class="modal-container">
      <div class="modal-header">
        <h3>{{ $t('settings') }}</h3>
        <button class="close-btn" @click="close">&times;</button>
      </div>
      
      <div class="modal-body">
        <!-- 语言设置 -->
        <div class="settings-section">
          <h4>{{ $t('languageSetting') }}</h4>
          <div class="language-options">
            <label v-for="lang in languages" :key="lang.value">
              <input 
                type="radio" 
                v-model="selectedLanguage" 
                :value="lang.value"
              >
              {{ lang.label }}
            </label>
          </div>
        </div>

        <!-- 账户设置 -->

      </div>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
import { ref ,watch,onMounted} from 'vue'

const selectedLanguage = ref('zh-Hans')
const emit = defineEmits(['close'])
const { locale } = useI18n()
const languages = ref([
  { label: '简体中文', value: 'zh-Hans', font: 'SC_Font' },
  { label: '繁體中文', value: 'zh-Hant', font: 'TC_Font' },
  { label: 'English', value: 'en', font: 'EN_Font' },
  { label: '日本語', value: 'jp', font: 'JP_Font' }
])
watch(selectedLanguage, (newVal) => {
  const selectedFont = languages.value.find(lang => lang.value === newVal).font
  document.documentElement.style.setProperty('--main-font', selectedFont)
  locale.value = newVal // 切换i18n语言
  // 持久化存储
  localStorage.setItem('selectedLanguage', newVal)
  localStorage.setItem('selectedFont', selectedFont)
})
// 初始化读取
onMounted(() => {
  const savedLang = localStorage.getItem('selectedLanguage')||'zh-Hans'
  selectedLanguage.value = savedLang
  locale.value = savedLang
})


const close = () => {
  emit('close')
}
</script>

<style scoped>
.modal-mask {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-container {
  background: white;
  border-radius: 12px;
  padding: 20px;
  width: 400px;
  max-width: 90%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
  margin-bottom: 15px;
}

.close-btn {
  font-size: 24px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0 8px;
  transition: opacity 0.2s;
}

.close-btn:hover {
  opacity: 0.7;
}

.settings-section {
  margin-bottom: 20px;
}

.settings-section h4 {
  color: #1f1c16;
  margin-bottom: 10px;
  font-size: 16px;
}

.language-options {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.language-options label {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  border-radius: 6px;
  transition: background 0.2s;
}

.language-options label:hover {
  background: #f5f5f5;
}

.placeholder {
  padding: 15px;
  background: #f8f8f8;
  border-radius: 8px;
  text-align: center;
  color: #666;
}
</style>