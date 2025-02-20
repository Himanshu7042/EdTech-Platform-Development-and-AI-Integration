import { createApp } from 'vue'
import App from './App.vue'
import { createWebHistory, createRouter } from 'vue-router'
import landingPage from './routes/landingPage.js'
import auth from './routes/auth.js'
import admin from './routes/admin.js'
import tutor from './routes/tutor.js'
import learner from './routes/learner.js'

const router = createRouter({
    history: createWebHistory(),
    routes:[
        ...landingPage,
        ...auth,
        ...admin,
        ...tutor,
        ...learner
    ]
})

const app = createApp(App)
app.use(router)
app.mount('#app')

