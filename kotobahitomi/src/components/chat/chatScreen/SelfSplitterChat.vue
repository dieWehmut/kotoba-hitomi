<!-- filepath: vue-chat/src/components/chat/chatScreen/SelfSplitterChat.vue -->
<template>
  <BaseChat
    chatId="self-splitter-chat"
    :chatTitle="$t('modes.self-splitter')"
    :defaultBg="splitRoomBg"
    :avatarPath="selfSplitterAvatar"
    mode="self-splitter"
    @back="$emit('back')"
  />
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
import BaseChat from "./BaseChat.vue";
import splitRoomBg from '@assets/bg/baseBg.jpg';
import selfSplitterAvatar from '@assets/avatar/self-splitter.jpg';
</script>
