<!-- filepath: vue-chat/src/components/function/Toast.vue -->
<template>
  <div class="toast show">
    <div class="toast-content">{{ message }}</div>
  </div>
</template>

<script setup>
defineProps(['message'])
</script>
<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

body {
  position: relative;
  overflow: hidden;
  min-height: 100vh;
}

/* 提示窗口样式 */
.toast {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) scale(0.9);
  background: linear-gradient(135deg, #ff99aa, #ffaaff);
  color: #333;
  padding: 20px 30px;
  border-radius: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  transform-origin: center;
  opacity: 0;
  transition: transform 0.3s ease, opacity 0.3s ease;
  z-index: 1000;
  border: 2px solid #ff66aa;
}

.toast.show {
  transform: translate(-50%, -50%) scale(1);
  opacity: 1;
}

.toast-content {
  font-size: 1.2rem;
  font-weight: bold;
  text-align: center;
}

@keyframes pulse {
  0% { transform: translate(-50%, -50%) scale(1); }
  50% { transform: translate(-50%, -50%) scale(1.05); }
  100% { transform: translate(-50%, -50%) scale(1); }
}

.toast.show {
  animation: pulse 0.5s infinite;
}
</style>