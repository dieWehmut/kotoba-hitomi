<template>
  <BaseChat
    chatId="game-word-chat"
    :chatTitle="$t('modes.game-word')"
    :defaultBg="gameWordBg"
    :avatarPath="gameWordAvatar"
    mode="game-word"
    @back="$emit('back')"
  />
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
import BaseChat from "./BaseChat.vue";
import gameWordBg from '@assets/bg/baseBg.jpg';
import gameWordAvatar from '@assets/avatar/game-word.jpg';
</script>