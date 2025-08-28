<!-- filepath: vue-chat/src/components/chat/chatScreen/FantasyMasterChat.vue -->
<template>
  <BaseChat
    chatId="fantasy-master-chat"
    :chatTitle="$t('modes.fantasy-master')"
    :defaultBg="fantasyWorldBg"
    :avatarPath="fantasyMasterAvatar"
    mode="fantasy-master"
    @back="$emit('back')"
  />
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
import BaseChat from "./BaseChat.vue";
import fantasyWorldBg from '@assets/bg/baseBg.jpg';
import fantasyMasterAvatar from '@assets/avatar/fantasy-master.jpg';
</script>
