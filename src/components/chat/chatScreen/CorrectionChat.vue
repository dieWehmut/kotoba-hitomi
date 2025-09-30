<!-- filepath: vue-chat/src/components/chat/chatScreen/CorrectionChat.vue -->
<template>
  <BaseChat
    chatId="correction-chat"
    :chatTitle="$t('modes.correction')"
:defaultBg="correctionBg"
    :avatarPath="correctionAvatar"
    mode="correction"
    @back="$emit('back')"
  />
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
import BaseChat from "./BaseChat.vue";
import correctionBg from '@assets/bg/baseBg.jpg';
import correctionAvatar from '@assets/avatar/correction.jpg';
</script>