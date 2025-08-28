<!-- filepath: vue-chat/src/components/chat/chatScreen/LNFactoryChat.vue -->
<template>
  <BaseChat
    chatId="ln-factory-chat"
    :chatTitle="$t('modes.ln-factory')"
    :defaultBg="lnFactoryBg"
    :avatarPath="lnFactoryAvatar"
    mode="ln-factory"
    @back="$emit('back')"
  />
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
import BaseChat from "./BaseChat.vue";
import lnFactoryBg from '@assets/bg/baseBg.jpg';
import lnFactoryAvatar from '@assets/avatar/ln-factory.jpg';
</script>
