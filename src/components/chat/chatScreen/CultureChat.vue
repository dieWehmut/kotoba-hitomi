<template>
  <BaseChat
    chatId="culture-chat"
    :chatTitle="$t('modes.culture')"
    :defaultBg="cultureBg"
    :avatarPath="cultureAvatar"
    mode="culture"
    @back="$emit('back')"
  />
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
import BaseChat from "./BaseChat.vue";
import cultureBg from '@assets/bg/baseBg.jpg';
import cultureAvatar from '@assets/avatar/culture.jpg';
</script>