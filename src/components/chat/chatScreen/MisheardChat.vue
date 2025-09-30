<template>
  <BaseChat
    chatId="misheard-chat"
    :chatTitle="$t('modes.misheard')"
    :defaultBg="misheardBg"
    :avatarPath="misheardAvatar"
    mode="misheard"
    @back="$emit('back')"
  />
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
import BaseChat from "./BaseChat.vue";
import misheardBg from '@assets/bg/baseBg.jpg';
import misheardAvatar from '@assets/avatar/misheard.jpg';
</script>