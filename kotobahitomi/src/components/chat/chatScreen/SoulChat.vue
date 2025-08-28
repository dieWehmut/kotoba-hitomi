<!-- filepath: vue-chat/src/components/chat/chatScreen/SoulChat.vue -->
<template>
  <BaseChat
    chatId="soul-chat"
    :chatTitle="$t('modes.soul')"
    :defaultBg="soulBg"
    :avatarPath="soulAvatar"
    mode="soul"
    @back="$emit('back')"
  />
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
import BaseChat from "./BaseChat.vue";
import soulBg from '@assets/bg/baseBg.jpg';
import soulAvatar from '@assets/avatar/soul.jpg';
</script>