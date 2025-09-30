<!-- filepath: vue-chat/src/components/chat/chatScreen/SmartParallelChat.vue -->
<template>
  <BaseChat
    ref="baseChat"
    chatId="smart-parallel"
    :chatTitle="$t('smartParallel')"
    mode="smart-parallel"
    :selectedAgents="selectedAgents"
    :defaultBg="parallelBg"
    :avatarPath="zeroAvatar"
    @back="$emit('back')"
    :showThinkingIndicator="false"
  >
    <template #righttop>
      <transition name="slide">
        <div v-show="!agentCollapsed" class="agent-sidebar">
          <div class="sessions-header">
            <div class="sidebar-header-row">
              <button class="collapse-btn" @click="toggleSidebar">
                <i class="fas fa-chevron-right"></i>
              </button>
              <h2>
                {{
                  $t("smartParallelAgents", { count: selectedAgents.length })
                }}
              </h2>
            </div>
          </div>
          <div class="agent-list">
            <div
              v-for="agent in availableAgents"
              :key="agent.mode"
              class="agent-item"
              :class="{ selected: isAgentSelected(agent.mode) }"
              @click="toggleAgent(agent.mode)"
            >
              <img :src="agent.avatar" class="agent-avatar" />
              <div
                v-if="isAgentSelected(agent.mode)"
                class="selected-indicator"
              ></div>
              <div class="agent-info">
                <span class="agent-name">{{ agent.name }}</span>
                <span class="agent-mode">{{ agent.mode }}</span>
              </div>
              <i
                v-if="isAgentSelected(agent.mode)"
                class="fas fa-check selected-icon"
              ></i>
            </div>
          </div>
        </div>
      </transition>
      <button v-show="agentCollapsed" class="expand-btn" @click="toggleSidebar">
        <i class="fas fa-chevron-left"></i>
      </button>
    </template>
  </BaseChat>
</template>

<script setup>
import { ref } from "vue";
import BaseChat from "./BaseChat.vue";
import parallelBg from "@assets/bg/baseBg.jpg";
import zeroAvatar from "@assets/avatar/zero.gif";
import jingujiAvatar from "@assets/avatar/jinguji.jpg";
import fujiiAvatar from "@assets/avatar/fujii.jpg";
import yamadaAvatar from "@assets/avatar/yamada.jpg";
import yamamotoAvatar from "@assets/avatar/yamamoto.jpg";
import fujisakiAvatar from "@assets/avatar/fujisaki.jpg";
import nakamuraAvatar from "@assets/avatar/nakamura.jpg";
import tanakaAvatar from "@assets/avatar/tanaka.jpg";
import takahashiAvatar from "@assets/avatar/takahashi.jpg";
import satoAvatar from "@assets/avatar/sato.jpg";
import { useI18n } from "vue-i18n";

const { t } = useI18n();
const agentCollapsed = ref(true);
function toggleSidebar() {
  agentCollapsed.value = !agentCollapsed.value;
}
const emit = defineEmits(["back"]);
const baseChat = ref(null);

const selectedAgents = ref([]);
const availableAgents = ref([
  { mode: "jinguji", name: "神宮寺 朋哉", avatar: jingujiAvatar },
  { mode: "fujii", name: "藤井 匠", avatar: fujiiAvatar },
  { mode: "yamada", name: "山田 しおり", avatar: yamadaAvatar },
  { mode: "yamamoto", name: "山本ゴロー", avatar: yamamotoAvatar },
  { mode: "fujisaki", name: "藤崎メイ", avatar: fujisakiAvatar },
  { mode: "nakamura", name: "中村カナ", avatar: nakamuraAvatar },
  { mode: "tanaka", name: "田中ユウト", avatar: tanakaAvatar },
  { mode: "takahashi", name: "高橋 唯", avatar: takahashiAvatar },
  { mode: "sato", name: "佐藤リク", avatar: satoAvatar },
]);

const toggleAgent = (mode) => {
  const agent = availableAgents.value.find((a) => a.mode === mode);
  if (!agent) return;

  const index = selectedAgents.value.findIndex((a) => a.mode === mode);
  if (index > -1) {
    selectedAgents.value.splice(index, 1);
  } else if (selectedAgents.value.length < 9) {
    selectedAgents.value.push(agent); // 存储完整的agent对象
  }

  // 强制更新数组以触发响应
  selectedAgents.value = [...selectedAgents.value];
  if (baseChat.value) {
    baseChat.value.selectedAgents = [...selectedAgents.value];
  }
};

const isAgentSelected = (mode) =>
  selectedAgents.value.some((agent) => agent.mode === mode);
</script>

<style scoped>
.selected-indicator {
  position: absolute;
  right: 8px;
  top: 8px;
  width: 15px;
  height: 15px;
  border-radius: 50%;
  background: #04e60b;
  border: 5px solid rgb(16, 213, 177);
  z-index: 1001;
}
.slide-enter-active,
.slide-leave-active {
  transition: transform 0s ease-out, opacity 0s ease-in-out;
  transform-origin: left;
}
.slide-enter-from,
.slide-leave-to {
  transform: translateX(-20px);
  opacity: 0;
}

.discussion-status {
  margin-left: 10px;
  padding: 4px 8px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 12px;
  font-size: 0.85em;
  color: #fff;
}
.agent-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid #1c0211;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  position: relative;
  z-index: 999;
}
.agent-avatar:hover {
  transform: scale(1.1);
}
.agent-info {
  flex: 1;
  min-width: 0;
}

.agent-name {
  font-weight: 600;
  color: #0404c5fe;
  font-size: 0.95em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.agent-mode {
  font-size: 0.75em;
  color: #c62536;
  margin-top: 2px;
}

.selected-icon {
  color: #7f4ab1;
  margin-left: 10px;
  font-size: 1.1em;
}

.input-control-area {
  position: relative;
  padding: 15px;
  background: rgba(225, 64, 64, 0.95);
  border-radius: 20px;
  margin: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}
.session-item {
  position: relative;
  padding: 12px;
  margin-bottom: 8px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.session-item.active {
  background: linear-gradient(135deg, #f7d6ff, #aee9ff);
}
.collapsed {
  width: 60px;
  overflow: hidden;
}

.collapsed .sessions-header h3,
.collapsed .sessions-list {
  display: none;
}
.discussion-sessions {
  width: 280px;
  flex-shrink: 0;
}
.toggle-sidebar-btn {
  width: 32px;
  height: 80px;
  background-color: #fff;
  border: 1px solid #ccc;
  border-right: none;
  border-radius: 6px 0 0 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: -2px 0 6px rgba(0, 0, 0, 0.1);
  margin-top: 16px;
}
/* 调整输入区域样式 */
.input-control-area {
  position: relative;
  padding: 15px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  margin-top: auto;
}
.agent-sidebar-wrapper {
  position: absolute;
  top: 0;
  right: 0;
  display: flex;
  height: 100%;
  align-items: flex-start;
  z-index: 10;
}


.agent-sidebar {
  width: 280px;
  background-color: #f8f8f8;
  height: 100%;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.1);
  padding: 12px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: all 0.3s ease;
}

.sidebar-header-row {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.sidebar-header-row h2 {
  margin: 0;
  font-size: 1.6em;
  margin-left: 8px;
  color: #8331cb !important; /* 紫色 */
  text-align: center;
  letter-spacing: 1px;
}

.sessions-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.circle-btn {
  background: linear-gradient(135deg, #4f3bd3);
  color: rgb(220, 218, 57);
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4);
}
.start-btn {
  background: linear-gradient(135deg, #4caf50, #45a049);
}

.pause-btn {
  background: linear-gradient(135deg, #ff9800, #f57c00);
}

.stop-btn {
  background: linear-gradient(135deg, #f44336, #d32f2f);
}
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
.agent-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin-top: 10px;
  flex: 1;
  overflow-y: auto;
}

.agent-item {
  display: flex;
  align-items: center;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}
.agent-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.agent-item.selected {
  border-color: #b48be4;
}
#smart-parallel h2 {
  font-size: 1.6em;
  margin-bottom: 0.2rem;
  color: #fff;
  text-align: center;
  letter-spacing: 1px;
}
/* 删除或调整媒体查询中的样式 */
@media (max-width: 768px) {
  /* 移除或调整这些样式，保持与电脑端一致 */
  .agent-item {
    padding: 12px !important; /* 保持与电脑端一致 */
    margin: 0 !important; /* 保持与电脑端一致 */
    transform: none !important; /* 保持与电脑端一致 */
    border: 1px solid #c63c3c !important; /* 保持与电脑端一致 */
  }

  .agent-avatar {
    width: 40px !important; /* 保持与电脑端一致 */
    height: 40px !important; /* 保持与电脑端一致 */
  }

  .agent-name {
    font-size: 0.95em !important; /* 保持与电脑端一致 */
  }

  .agent-mode {
    font-size: 0.75em !important; /* 保持与电脑端一致 */
  }
}
@keyframes glow {
  from {
    text-shadow: 0 0 5px #ff00ff, 0 0 10px #ff00ff, 0 0 15px #ff00ff,
      0 0 20px #ff00ff;
  }
  to {
    text-shadow: 0 0 10px #ff00ff, 0 0 20px #0ff0ff, 0 0 30px #ff00ff,
      0 0 40px #ff00ff;
  }
}
.agent-sidebar {
  position: relative;
  height: calc(100vh - 90px);
  border-radius: 1px;
  padding: 0px;
  overflow: hidden;
  background: linear-gradient(
    145deg,
    rgba(255, 255, 255, 0.05),
    rgba(255, 255, 255, 0.15)
  );
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

/* 保持两侧边栏折叠后对齐 */
.sessions-container.collapsed,
.agent-sidebar.collapsed {
  width: 60px;
  min-width: 60px;
  padding: 10px;
}

/* 折叠状态下的按钮位置调整 */
.sessions-container.collapsed .sessions-header,
.agent-sidebar.collapsed .sessions-header {
  justify-content: center;
}
.expand-btn {
  position: absolute;
  right: 0px;
  top: 0px;
}
</style>
