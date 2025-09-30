<!-- filepath: vue-chat/src/components/WelcomeScreen.vue -->
<template>
  <section id="welcome-screen" class="screen">
    <!-- 设置按钮 -->
    <div class="lefttop-container">
      <button class="settings-btn" @click="showSettings = true">
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z"
            stroke="currentColor"
            stroke-width="2"
          />
          <path
            d="M19.4 15C18.85 13.75 18.85 12.25 19.4 11L21.5 7.5C19.5 5.25 16.5 4 13.4 4L10.6 4C7.5 4 4.5 5.25 2.5 7.5L4.6 11C5.15 12.25 5.15 13.75 4.6 15L2.5 18.5C4.5 20.75 7.5 22 10.6 22L13.4 22C16.5 22 19.5 20.75 21.5 18.5L19.4 15Z"
            stroke="currentColor"
            stroke-width="2"
          />
        </svg>
      </button>
      <button class="settings-btn" style="top: 50px" @click="showHelp = true">
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z"
            stroke="currentColor"
            stroke-width="2"
          />
          <path
            d="M12 16V12"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
          />
          <path
            d="M12 8H12.01"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
          />
        </svg>
      </button>
    </div>
    <div class="leftbottom-container">
      <button class="download-btn" @click="showDownload = true">
        <i class="fas fa-android"></i>
      </button>
    </div>
    <div class="container">
      <h1>{{ $t("welcome.title") }}</h1>
      <p class="subtitle">{{ $t("welcome.subtitle") }}</p>
      <div class="welcome-group-btn">
              <button
       id="smart-parallel-btn"
        class="anime-btn"
        @click="$emit('smart-parallel')"
      >
        {{ $t("welcome.smartParallelBtn") }}
      </button>
        <button id="start-btn" class="anime-btn" @click="$emit('start')">
          {{ $t("welcome.startBtn") }}
        </button>
        <button
          id="quick-chat-btn"
          class="anime-btn"
          @click="$emit('quick-chat')"
        >
          {{ $t("welcome.quickChatBtn") }}
        </button>
    </div>
    </div>
    <div class="footer-copyright">
      ©️CabbageGroup-All Rights Reserved,led by HC
    </div>
    <!-- 设置弹窗 -->
    <SettingsModal v-if="showSettings" @close="showSettings = false" />
    <HelpModal v-if="showHelp" @close="showHelp = false" />
    <DownloadModal v-if="showDownload" @close="showDownload = false" />
  </section>
</template>

<script setup>
import { ref } from "vue";
import SettingsModal from "./function/SettingsModal.vue";
import HelpModal from "./function/HelpModal.vue";
const showSettings = ref(false);
const showHelp = ref(false);
import DownloadModal from "./function/DownloadModal.vue";
const showDownload = ref(false);
import { useI18n } from "vue-i18n";
const { t } = useI18n();
</script>
<style scoped>
.settings-btn {
  position: absolute;
  top: 0px;
  left: 0px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(138, 40, 40, 0.3);
  cursor: pointer;
  padding: 10px;
  color: rgba(106, 76, 17, 0.8);
  transition: transform 0.3s, opacity 0.3s, background 0.3s;
  z-index: 2;
}

.settings-btn:hover {
  transform: rotate(90deg);
  opacity: 1;
  background: rgba(255, 255, 255, 0.2);
}

.settings-btn:active {
  transform: scale(0.9);
  background: rgba(255, 255, 255, 0.3);
}
.download-btn {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(138, 40, 40, 0.3);
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  color: rgba(106, 76, 17, 0.8);
}

.download-btn:hover {
  transform: scale(1.1);
  background: rgba(255, 255, 255, 0.2);
}

.download-btn:active {
  transform: scale(0.95);
}
.welcome-group-btn {
  flex-direction: column;
  display: flex;
  gap: 2px; /* 设置按钮间距为20px，可根据需要调整 */
  z-index: 10;
}
/* 欢迎界面样式 */
#welcome-screen {
  background-image: url("@assets/bg/baseBg.jpg");
}

#welcome-screen h1 {
  font-size: 3.5rem;
  margin-bottom: 1.5rem;
  color: #030100;
  text-align: center;
  letter-spacing: 1px;
  animation: glow 1.5s ease-in-out infinite alternate;
}
.subtitle {
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
  color: #8331cb;
  text-align: center;
  animation: neon-pulse 1.5s infinite alternate;
}

.anime-btn {
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
  display: inline-block;
  min-width: 20px;
  text-align: center;
  margin: 1px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.anime-btn:hover {
  transform: translateY(-5px) scale(1.05);
  box-shadow: 0 12px 25px rgba(205, 176, 218, 0.12);
  background: #edeae4;
}

.anime-btn:active {
  transform: translateY(1px) scale(0.98);
  box-shadow: 0 2px 5px rgba(142, 68, 173, 0.08);
  background: #dcd6cb;
}

.anime-btn::before {
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

/* 容器样式 */
.container {
  width: 100%;
  max-width: 1200px;
  padding: 0 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  gap: 20px;
}

#start-btn {
  margin-top: 20px;
}

#quick-chat-btn {
  margin-top: 10px;
}
/* 适配手机屏幕 */
@media (max-width: 768px) {
  #welcome-screen h1 {
    font-size: 2.5rem !important;
    margin-bottom: 1rem; /* 减小外边距 */
  }

  .subtitle {
    font-size: 1.3rem; /* 减小副标题字体大小 */
    margin-bottom: 0.3rem; /* 减小外边距 */
  }

  .anime-btn {
    font-size: 1.5rem !important;
    padding: 1rem 1.5rem !important;
    margin: 10px 0 !important;
  }

  .anime-btn:hover {
    transform: translateY(-3px) scale(1.03); /* 减小悬停效果 */
    box-shadow: 0 8px 15px rgba(205, 176, 218, 0.5); /* 减小阴影 */
  }

  .anime-btn:active {
    transform: translateY(1px) scale(0.99); /* 减小按下效果 */
  }

  .container {
    padding: 0 15px; /* 减小容器内边距 */
  }
}
</style>
