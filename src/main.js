import { createApp } from 'vue'
import App from './App.vue'
import './global.css'
import '@fortawesome/fontawesome-free/css/all.min.css'
import i18n from './i18n'
import router from './router' // Add this line

const app = createApp(App)
app.use(i18n)
app.use(router) // Add this line
app.mount('#app')