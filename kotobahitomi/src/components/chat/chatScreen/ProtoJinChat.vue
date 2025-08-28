<!-- filepath: vue-chat/src/components/chat/chatScreen/ProtoJinChat.vue -->
<template>
  <BaseChat
    chatId="proto-jin-chat"
    :chatTitle="$t('modes.proto-jin')"
    :defaultBg="languageEssenceBg"
    :avatarPath="protoJinAvatar"
    mode="proto-jin"
    @back="$emit('back')"
  />
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
import BaseChat from "./BaseChat.vue";
import languageEssenceBg from '@assets/bg/baseBg.jpg';
import protoJinAvatar from '@assets/avatar/proto-jin.jpg';
</script>
