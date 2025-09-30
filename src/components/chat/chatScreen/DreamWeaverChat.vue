<!-- filepath: vue-chat/src/components/chat/chatScreen/DreamWeaverChat.vue -->
<template>
  <BaseChat
    chatId="dream-weaver-chat"
    :chatTitle="$t('modes.dream-weaver')"
    :defaultBg="dreamTowerBg"
    :avatarPath="dreamWeaverAvatar"
    mode="dream-weaver"
    @back="$emit('back')"
  />
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
import BaseChat from "./BaseChat.vue";
import dreamTowerBg from '@assets/bg/baseBg.jpg';
import dreamWeaverAvatar from '@assets/avatar/dream-weaver.jpg';
</script>
