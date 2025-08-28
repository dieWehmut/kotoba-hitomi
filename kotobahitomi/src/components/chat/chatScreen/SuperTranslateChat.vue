<template>
  <BaseChat
    chatId="super-translate-chat"
    :chatTitle="$t('modes.super-translate')"
    :defaultBg="superTranslateBg"
    :avatarPath="superTranslateAvatar"
    mode="super-translate"
    @back="$emit('back')"
  />
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
import BaseChat from "./BaseChat.vue";
import superTranslateBg from '@assets/bg/baseBg.jpg';
import superTranslateAvatar from '@assets/avatar/super-translate.jpg';
</script>