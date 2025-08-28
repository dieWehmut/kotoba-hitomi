import { createRouter, createWebHashHistory } from 'vue-router'
import WelcomeScreen from './components/WelcomeScreen.vue'
import GroupDiscussionChat from './components/chat/chatScreen/GroupDiscussionChat.vue'
import SoulChat from './components/chat/chatScreen/SoulChat.vue'
import MisheardChat from './components/chat/chatScreen/MisheardChat.vue'
import CorrectionChat from './components/chat/chatScreen/CorrectionChat.vue'
import GameMisheardChat from './components/chat/chatScreen/GameMisheardChat.vue'
import GameWordChat from './components/chat/chatScreen/GameWordChat.vue'
import CultureChat from './components/chat/chatScreen/CultureChat.vue'
import DialectChat from './components/chat/chatScreen/DialectChat.vue'
import SuperTranslateChat from './components/chat/chatScreen/SuperTranslateChat.vue'
import STEMChat from './components/chat/chatScreen/STEMChat.vue'
import DreamWeaverChat from './components/chat/chatScreen/DreamWeaverChat.vue'
import FantasyChat from './components/chat/chatScreen/FantasyChat.vue'
import GlitchSpaceChat from './components/chat/chatScreen/GlitchSpaceChat.vue'
import LNFactoryChat from './components/chat/chatScreen/LNFactoryChat.vue'
import ProtoJinChat from './components/chat/chatScreen/ProtoJinChat.vue'
import SelfSplitterChat from './components/chat/chatScreen/SelfSplitterChat.vue'
import UnconsciousVisitorChat from './components/chat/chatScreen/UnconsciousVisitorChat.vue'
import QuickChatScreen from './components/function/QuickChatScreen.vue'

const routes = [
  {
    path: '/',
    name: 'welcome',
    component: WelcomeScreen
  },
  {
    path: '/group-discussion',
    name: 'group-discussion',
    component: GroupDiscussionChat
  },
  {
    path: '/quick-chat',
    component: QuickChatScreen,
    children: [
      { path: 'soul', component: SoulChat },
      { path: 'misheard', component: MisheardChat },
      { path: 'correction', component: CorrectionChat },
      { path: 'game-misheard', component: GameMisheardChat },
      { path: 'game-word', component: GameWordChat },
      { path: 'culture', component: CultureChat },
      { path: 'dialect', component: DialectChat },
      { path: 'super-translate', component: SuperTranslateChat },
      { path: 'stem', component: STEMChat },
      { path: 'dream-weaver', component: DreamWeaverChat },
      { path: 'fantasy-master', component: FantasyChat },
      { path: 'glitch-space', component: GlitchSpaceChat },
      { path: 'ln-factory', component: LNFactoryChat },
      { path: 'proto-jin', component: ProtoJinChat },
      { path: 'self-splitter', component: SelfSplitterChat },
      { path: 'unconscious', component: UnconsciousVisitorChat }
    ]
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})


export default router