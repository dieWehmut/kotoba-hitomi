<!-- filepath: vue-chat/src/App.vue -->
<template>
  <transition name="anime-fade-cross">
    <WelcomeScreen
      v-if="screen === 'welcome'"
      @start="screen = 'group-discussion'"
      @quick-chat="screen = 'quick-chat'"
      @smart-parallel="screen = 'smart-parallel'"
      key="welcome"
    />
    <SmartParallelChat
      v-else-if="screen === 'smart-parallel'"
      @back="screen = 'welcome'"
    />
    <GroupDiscussionChat
      v-else-if="screen === 'group-discussion'"
      @back="screen = 'welcome'"
    />
    <SoulChat v-else-if="screen === 'soul'" @back="screen = 'quick-chat'" />
    <MisheardChat
      v-else-if="screen === 'misheard'"
      @back="screen = 'quick-chat'"
    />
    <CorrectionChat
      v-else-if="screen === 'correction'"
      @back="screen = 'quick-chat'"
    />
    <GameMisheardChat
      v-else-if="screen === 'game-misheard'"
      @back="screen = 'quick-chat'"
    />
    <GameWordChat
      v-else-if="screen === 'game-word'"
      @back="screen = 'quick-chat'"
    />
    <CultureChat
      v-else-if="screen === 'culture'"
      @back="screen = 'quick-chat'"
    />
    <DialectChat
      v-else-if="screen === 'dialect'"
      @back="screen = 'quick-chat'"
    />
    <SuperTranslateChat
      v-else-if="screen === 'super-translate'"
      @back="screen = 'quick-chat'"
    />
    <STEMChat v-else-if="screen === 'stem'" @back="screen = 'quick-chat'" />

    <!-- 新增的7个聊天组件 -->
    <DreamWeaverChat
      v-else-if="screen === 'dream-weaver'"
      @back="screen = 'quick-chat'"
    />
    <FantasyChat
      v-else-if="screen === 'fantasy-master'"
      @back="screen = 'quick-chat'"
    />
    <GlitchSpaceChat
      v-else-if="screen === 'glitch-space'"
      @back="screen = 'quick-chat'"
    />
    <LNFactoryChat
      v-else-if="screen === 'ln-factory'"
      @back="screen = 'quick-chat'"
    />
    <ProtoJinChat
      v-else-if="screen === 'proto-jin'"
      @back="screen = 'quick-chat'"
    />
    <SelfSplitterChat
      v-else-if="screen === 'self-splitter'"
      @back="screen = 'quick-chat'"
    />
    <UnconsciousVisitorChat
      v-else-if="screen === 'unconscious'"
      @back="screen = 'quick-chat'"
    />

    <QuickChatScreen
      v-else-if="screen === 'quick-chat'"
      @back="screen = 'welcome'"
      @select-chat="handleSelectChat"
    />
  </transition>
  <Toast v-if="toast.show" :message="toast.message" />
</template>

<script setup>
import { ref, provide, watch, onMounted } from "vue";
import { useRouter } from "vue-router";
import WelcomeScreen from "./components/WelcomeScreen.vue";
import GroupDiscussionChat from "./components/chat/chatScreen/GroupDiscussionChat.vue";
import SoulChat from "./components/chat/chatScreen/SoulChat.vue";
import MisheardChat from "./components/chat/chatScreen/MisheardChat.vue";
import CorrectionChat from "./components/chat/chatScreen/CorrectionChat.vue";
import Toast from "./components/function/Toast.vue";
import GameMisheardChat from "./components/chat/chatScreen/GameMisheardChat.vue";
import GameWordChat from "./components/chat/chatScreen/GameWordChat.vue";
import CultureChat from "./components/chat/chatScreen/CultureChat.vue";
import DialectChat from "./components/chat/chatScreen/DialectChat.vue";
import SuperTranslateChat from "./components/chat/chatScreen/SuperTranslateChat.vue";
import QuickChatScreen from "./components/function/QuickChatScreen.vue";
import STEMChat from "./components/chat/chatScreen/STEMChat.vue";
import DreamWeaverChat from "./components/chat/chatScreen/DreamWeaverChat.vue";
import FantasyChat from "./components/chat/chatScreen/FantasyChat.vue";
import GlitchSpaceChat from "./components/chat/chatScreen/GlitchSpaceChat.vue";
import LNFactoryChat from "./components/chat/chatScreen/LNFactoryChat.vue";
import ProtoJinChat from "./components/chat/chatScreen/ProtoJinChat.vue";
import SelfSplitterChat from "./components/chat/chatScreen/SelfSplitterChat.vue";
import UnconsciousVisitorChat from "./components/chat/chatScreen/UnconsciousVisitorChat.vue";
import SmartParallelChat from "./components/chat/chatScreen/SmartParallelChat.vue";
const screen = ref("welcome");
const toast = ref({ show: false, message: "" });
const router = useRouter();
const handleSelectChat = (type) => {
  screen.value = type;
};
function showToast(message) {
  toast.value = { show: true, message };
  setTimeout(() => (toast.value.show = false), 3000);
}
// 保存路由状态到sessionStorage
router.afterEach((to) => {
  sessionStorage.setItem("currentRoute", to.path);
});
// 修改初始化逻辑
onMounted(() => {
  const savedRoute = sessionStorage.getItem("currentRoute") || "/";
  router.push(savedRoute);
});

// 修改现有的路由守卫
router.afterEach((to) => {
  sessionStorage.setItem("currentRoute", to.path);
  screen.value = to.name ? to.name : "welcome"; // 保持与路由名称同步
});
// 初始化时恢复路由
const savedRoute = sessionStorage.getItem("currentRoute");
if (savedRoute) {
  router.push(savedRoute);
}
provide("showToast", showToast);
</script>
