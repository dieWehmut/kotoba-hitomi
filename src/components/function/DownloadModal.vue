<template>
  <div class="modal-mask" @click.self="close">
    <div class="modal-container download-modal">
      <div class="modal-header">
        <h3>{{ $t('modals.download.title') }}</h3>
        <button class="close-btn" @click="close">&times;</button>
      </div>
      <div class="modal-body">
        <div class="download-content">
          <font-awesome-icon :icon="['fab', 'android']" class="icon-android"/>

          <button 
            class="download-btn"
            @click="downloadApk"
          >
            {{ $t('modals.download.android') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['close'])
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
const downloadApk = () => {
  // 直接打开外部下载链接
  window.open('https://github.com/dieSehnsucht0/testCase/releases/download/app/testCase.apk', '_blank')
}

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
.modal-header h3 {
  font-size: 20px;
  font-weight: bold;
  margin: 0;
}
.close-btn:hover {
  opacity: 0.7;
}
.download-modal {
  width: 320px;
  text-align: center;
}

.download-content {
  padding: 20px;
}

.icon-android {
  font-size: 3rem;
  color: #21bb66;
  margin-bottom: 15px;
}

.download-btn {
  background: #52e996;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 25px;
  cursor: pointer;
  font-size: 1.1rem;
  transition: all 0.3s;
  margin-top: 15px;
}

.download-btn:hover {
  background: #29b764;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(61, 220, 132, 0.3);
}
</style>