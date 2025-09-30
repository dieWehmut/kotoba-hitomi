import { createI18n } from 'vue-i18n'
import zhHans from './locales/zh-Hans.json'
import en from './locales/en.json'
import zhHant from './locales/zh-Hant.json'
import jp from './locales/jp.json'

const messages = {
  'zh-Hans': zhHans,
  'en': en,
  'zh-Hant': zhHant,
  'jp': jp
}

// 从localStorage读取保存的语言设置
const savedLocale = localStorage.getItem('selectedLanguage') || 'zh-Hans'

export default createI18n({
  legacy: false,
  locale: savedLocale,  // 使用保存的语言
  fallbackLocale: 'en',
  messages
})