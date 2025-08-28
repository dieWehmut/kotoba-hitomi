<!-- filepath: vue-chat/src/components/function/HelpModal.vue -->
<template>
  <div class="modal-mask" @click.self="close">
    <div class="modal-container">
      <div class="modal-header">
        <h3>{{ $t('modals.help.title') }}</h3>
        <button class="close-btn" @click="close">&times;</button>
      </div>

      <div class="modal-body vertical-layout">
        <div class="top-tabs">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            @click="currentTab = tab.id"
            :class="{ active: currentTab === tab.id }"
          >
            {{ tab.title }}
          </button>
        </div>

        <div class="content-area">
          <div class="tab-content">
            <div class="scroll-content" v-html="renderedContent"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { marked } from 'marked'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
// 引入 Markdown 文件，Vite 支持 `?raw` 读取纯文本内容
import guideMd from '@assets/help/guide.md?raw'
import statementMd from '@assets/help/statement.md?raw'

const emit = defineEmits(['close'])
const currentTab = ref('statement')

const tabs = [
{ id: 'statement', title: t('modals.help.tabs.feedback') },
  { id: 'guide', title: t('modals.help.tabs.manual') }
]

// tab id 到 markdown 内容映射
const contentMap = {
  statement: statementMd,
  guide: guideMd
}

// 动态渲染 markdown 为 html
const renderedContent = computed(() => marked(contentMap[currentTab.value]))

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
  background: rgb(251, 247, 247);
  border-radius: 12px;
  padding: 10px;
  width: 500px;
  max-width: 100%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
}

.modal-header {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
  margin-bottom: 10px;
}

.modal-header h3 {
  font-size: 20px;
  font-weight: bold;
  margin: 0;
}

.close-btn {
  position: absolute;
  right: 0;
  top: 0;
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

.modal-body.vertical-layout {
  display: flex;
  flex-direction: column;
  height: 500px;
}

.top-tabs {
  display: flex;
  border-bottom: 2px solid #eee;
  margin-bottom: 10px;
}

.top-tabs button {
  background: none;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  color: #555;
  cursor: pointer;
  position: relative;
  transition: all 0.2s ease;
}

.top-tabs button:hover {
  color: #3498db;
}

.top-tabs button.active {
  color: #3498db;
  font-weight: 600;
}

.top-tabs button.active::after {
  content: "";
  position: absolute;
  bottom: -2px;
  left: 0;
  right: 0;
  height: 3px;
  background-color: #3498db;
  border-radius: 2px 2px 0 0;
}

.content-area {
  flex: 1;
  overflow: hidden;
}

.tab-content {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.scroll-content {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  line-height: 1.6;
  color: #444;
  font-family: 'KaiseiDecol-Regular';
}
@font-face {
  font-family: 'KaiseiDecol-Regular';
  src: url('@assets/fonts/KaiseiDecol-Regular.woff2') format('woff2');
}

.scroll-content h1, .scroll-content h2, .scroll-content h3 {
  margin-top: 1em;
  font-weight: bold;
  color: #333;
}

.scroll-content ul {
  padding-left: 1.2em;
  list-style: disc;
}
</style>
