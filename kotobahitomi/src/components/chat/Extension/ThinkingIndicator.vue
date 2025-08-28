<!-- filepath: vue-chat/src/components/chat/Extension/ThinkingIndicator.vue -->
<template>
  <div class="thinking-indicator" v-show="show">
    <img :src="avatar" class="thinking-avatar" alt="Agent Avatar" />
    <span class="thinking-text">{{ $t('thinking') }}🧠</span>
    <span class="thinking-time">{{ time }}</span>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
defineProps(['show', 'avatar', 'time'])
</script>
<style scoped>
  /* 思考时间徽章样式 */
  .thinking-time-badge {
    margin-top: 5px;
    font-size: 0.8rem;
    color: #666;
    text-align: right;
  }
  /* 思考指示器样式 */
  .thinking-indicator {
    position: absolute;
    top: calc(20px + env(safe-area-inset-top));
    left: calc(50px + env(safe-area-inset-left));
    display: flex;
    align-items: center;
    background-color: rgba(255, 255, 255, 0.7);
    border-radius: 20px;
    padding: 8px 15px;
    font-size: 0.9rem;
    color: #333;
    opacity: 1;
    transition: opacity 0.3s ease;
    z-index: 5;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }

  .thinking-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 10px;
  }

  .thinking-text {
    font-weight: bold;
    animation: blink 1s infinite;
  }

  .thinking-time {
    margin-left: 10px;
    font-weight: bold;
  }

  @keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
  }
</style>