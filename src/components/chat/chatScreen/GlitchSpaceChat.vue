<!-- filepath: vue-chat/src/components/chat/chatScreen/GlitchSpaceChat.vue -->
<template>
  <BaseChat
    chatId="glitch-space-chat"
    :chatTitle="$t('modes.glitch-space')"
    :defaultBg="glitchSpaceBg"
    :avatarPath="glitchSpaceAvatar"
    mode="glitch-space"
    @back="$emit('back')"
  />
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
import BaseChat from "./BaseChat.vue";
import glitchSpaceBg from '@assets/bg/baseBg.jpg';
import glitchSpaceAvatar from '@assets/avatar/glitch-space.jpg';
</script>
