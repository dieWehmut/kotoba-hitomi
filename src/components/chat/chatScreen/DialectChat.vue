<template>
  <BaseChat
    chatId="dialect-chat"
    :chatTitle="$t('modes.dialect')"
    :defaultBg="dialectBg"
    :avatarPath="dialectAvatar"
    mode="dialect"
    @back="$emit('back')"
  />
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
import BaseChat from "./BaseChat.vue";
import dialectBg from '@assets/bg/baseBg.jpg';
import dialectAvatar from '@assets/avatar/dialect.jpg';
</script>