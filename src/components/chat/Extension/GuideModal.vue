<template>
  <div class="modal-mask" @click.self="close">
    <div class="modal-container guide-modal">
      <div class="modal-header">
        <h3>{{ title }}</h3>
        <button class="close-btn" @click="close">&times;</button>
      </div>
      <div class="modal-body" v-html="guideContent"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { marked } from 'marked'
const props = defineProps({
  mode: String
})

const emit = defineEmits(['close'])
const guideContent = ref('')

const title = computed(() => {
  const modeNames = {
    'correction': '语言纠错',
    'soul': '心灵空间',
    'misheard': '空耳查询',
    'stem': '科学世界',
    'culture': '文化探索',
    'dialect': '方言探索',
    'super-translate': '翻译大师',
    'game-misheard': '空耳游戏',
    'game-word': '字词游戏',
    'dream-weaver': '梦境编织',
    'fantasy-master': '幻想世界',
    'glitch-space': '失控空间',
    'ln-factory': '小说工坊',
    'self-splitter': '拆解空间',
    'unconscious': '潜灵空间',
    'proto-jin': '言灵法师'
  }
  return `${modeNames[props.mode]}使用指南`
})

onMounted(async () => {
  try {
    const content = await import(`@/assets/help/${props.mode}.md?raw`)
    guideContent.value = marked.parse(content.default)
  } catch (e) {
    guideContent.value = '<p>使用说明加载中...</p>'
  }
})

const close = () => {
  emit('close')
}
</script>

<style scoped>
.guide-modal {
  max-width: 800px;
  padding: 20px;
  max-height: 80vh;
  overflow-y: auto;
}
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
</style>