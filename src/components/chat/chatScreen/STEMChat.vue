<!-- filepath: vue-chat/src/components/chat/chatScreen/STEMChat.vue -->
<template>
  <BaseChat
    chatId="stem-chat"
    :chatTitle="$t('modes.stem')"
    :defaultBg="stemBg"
    :avatarPath="stemAvatar"
    mode="stem"
    @back="$emit('back')"
  />
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
import BaseChat from "./BaseChat.vue";
import stemBg from '@assets/bg/baseBg.jpg';
import stemAvatar from '@assets/avatar/stem.jpg';
</script>