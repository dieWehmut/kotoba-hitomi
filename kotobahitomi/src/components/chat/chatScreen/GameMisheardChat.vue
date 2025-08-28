<template>
  <BaseChat
    chatId="game-misheard-chat"
    :chatTitle="$t('modes.game-misheard')"
    :defaultBg="gameMisheardBg"
    :avatarPath="gameMisheardAvatar"
    mode="game-misheard"
    @back="$emit('back')"
  />
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
import BaseChat from "./BaseChat.vue";
import gameMisheardBg from '@assets/bg/baseBg.jpg';
import gameMisheardAvatar from '@assets/avatar/game-misheard.jpg';
</script>