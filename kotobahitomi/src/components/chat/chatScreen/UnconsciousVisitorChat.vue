<!-- filepath: vue-chat/src/components/chat/chatScreen/UnconsciousVisitorChat.vue -->
<template>
  <BaseChat
    chatId="unconscious-visitor-chat"
    :chatTitle="$t('modes.unconscious')"
    :defaultBg="unconsciousBg"
    :avatarPath="unconsciousAvatar"
    mode="unconscious"
    @back="$emit('back')"
  />
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
import BaseChat from "./BaseChat.vue";
import unconsciousBg from '@assets/bg/baseBg.jpg';
import unconsciousAvatar from '@assets/avatar/unconscious.jpg';
</script>
