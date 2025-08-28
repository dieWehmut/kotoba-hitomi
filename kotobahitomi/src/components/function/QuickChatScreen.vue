<!-- filepath: vue-chat/src/components/function/QuickChatScreen.vue -->
<template>
  
  <section class="screen quick-chat-screen" id="quick-chat">
    <div class="lefttop-container">
      <button class="anime-btn" @click="$emit('back')">
        <i class="fas fa-arrow-left"></i>
      </button>
    </div>

      <div 
    class="scroll-container" 
    :style="scrollContainerStyle"
    ref="scrollContainer"
  >
      <div class="chat-grid">
        <div
          v-for="(chat, index) in chatList"
          :key="index"
          class="chat-item anime-btn"
          @click="$emit('select-chat', chat.type)"
        >
          <div class="chat-icon">{{ chat.icon }}</div>
          <div class="chat-title">{{ chat.title }}</div>
        </div>
      </div>
    </div>
  </section>
    <div class="footer-copyright">
    ©️CabbageGroup-All Rights Reserved,led by HC
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, onBeforeUnmount } from 'vue'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
// 在组件中添加滚动位置记录
const scrollContainer = ref(null)
const scrollPosition = ref(0)

// 保存滚动位置
onBeforeUnmount(() => {
  if (scrollContainer.value) {
    scrollPosition.value = scrollContainer.value.scrollTop
  }
})

// 恢复滚动位置
onMounted(() => {
  nextTick(() => {
    if (scrollContainer.value && scrollPosition.value) {
      scrollContainer.value.scrollTop = scrollPosition.value
    }
  })
})
onMounted(() => {
  scrollContainer.value?.addEventListener('scroll', saveScrollPosition)
  restoreScrollPosition() // 恢复滚动位置
})

onBeforeUnmount(() => {
  scrollContainer.value?.removeEventListener('scroll', saveScrollPosition)
})
const saveScrollPosition = () => {
  if (scrollContainer.value) {
    sessionStorage.setItem('quickChatScroll', scrollContainer.value.scrollTop)
  }
}
// 恢复滚动位置
const restoreScrollPosition = () => {
  const savedPosition = sessionStorage.getItem('quickChatScroll')
  if (scrollContainer.value && savedPosition) {
    scrollContainer.value.scrollTop = savedPosition
  }
}
const scrollContainerStyle = {
  maxHeight: '90vh',
  overflowY: 'auto',
  padding: '1rem',
  width: '100%',
  height: '100%',
  scrollBehavior: 'smooth'
}
// 添加滚动事件监听
onMounted(() => {
  scrollContainer.value?.addEventListener('scroll', saveScrollPosition)
})

onBeforeUnmount(() => {
  scrollContainer.value?.removeEventListener('scroll', saveScrollPosition)
})
const chatList = [
  // 原有项
  { type: "soul", title: t('modes.soul'), icon: "💖" },
  { type: "correction", title: t('modes.correction'), icon: "✏️" },
  { type: "misheard", title: t('modes.misheard'), icon: "🎧" },
  { type: "dialect", title: t('modes.dialect'), icon: "🗺️" },
  { type: "super-translate", title: t('modes.super-translate'), icon: "🚀" },
  { type: "culture", title: t('modes.culture'), icon: "🎎" },
  { type: "game-misheard", title: t('modes.game-misheard'), icon: "🎮" },
  { type: "game-word", title: t('modes.game-word'), icon: "🔠" },
  { type: "stem", title: t('modes.stem'), icon: "🧪" },
  { type: "dream-weaver", title: t('modes.dream-weaver'), icon: "🌌" },
  { type: "fantasy-master", title: t('modes.fantasy-master'), icon: "🌈" },
  { type: "glitch-space", title: t('modes.glitch-space'), icon: "🌀" },
  { type: "ln-factory", title: t('modes.ln-factory'), icon: "📚" },
  { type: "proto-jin", title: t('modes.proto-jin'), icon: "✨" },
  { type: "self-splitter", title: t('modes.self-splitter'), icon: "✂️" },
  { type: "unconscious", title: t('modes.unconscious'), icon: "👻" }
];
</script>

<style scoped>

.scroll-container {
  max-height: 90vh; /* 控制滚动区域高度 */
  overflow-y: auto;  /* 启用垂直滚动 */
  padding: 1rem;
  width: 100%;
    height: 100%;
}
.scroll-container {
  max-height: 90vh;
  overflow-y: auto;
  /* 新增滚动行为优化 */
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
}
.chat-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
  max-width: 400px;
  width: 100%;
  margin: 2rem auto;
}
.chat-item {
  background: #dcd6cb;
  color: #333;
  font-size: 1.5rem;
  padding: 1rem 1rem;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.2s, background 0.2s;
  box-shadow: 0 6px 20px rgba(103, 30, 135, 0.08);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  min-height: 150px;
  text-align: center;
  margin: 1px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.chat-item:hover {
  transform: translateY(-5px) scale(1.05);
  box-shadow: 0 12px 25px rgba(205, 176, 218, 0.12);
  background: #edeae4;
}

.chat-item:active {
  transform: translateY(1px) scale(0.98);
  box-shadow: 0 2px 5px rgba(142, 68, 173, 0.08);
  background: #dcd6cb;
}

.chat-item::before {
  content: "";
  position: absolute;
  top: -100%;
  left: -100%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    to right,
    transparent,
    rgba(255, 255, 255, 0.15),
    transparent
  );
  background-size: 200% 200%;
  animation: shine 2s infinite;
}

.chat-icon {
  font-size: 3.5rem;
  margin-bottom: 0rem;
}

.chat-title {
  font-size: 1.2rem;
  color: #000000;
  font-weight: bold;
  text-align: center;
}
/* 自定义滚动条样式 */
.scroll-container::-webkit-scrollbar {
  width: 8px;
}

.scroll-container::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.scroll-container::-webkit-scrollbar-thumb {
  background: rgba(128, 121, 228, 0.8);
  border-radius: 4px;
}

#quick-chat {
  background-image: url("@assets/bg/baseBg.jpg");
}
</style>