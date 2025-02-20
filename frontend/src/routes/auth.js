import auth from '@/components/auth.vue'
import create from '@/components/create.vue'
import t_register from '@/components/registeration/t_registeration.vue'
import le_register from '@/components/registeration/le_registeration.vue'

export default [
    {
        path: '/auth',
        component: auth,
        name: 'auth'
    },
    {
        path: '/create',
        component: create,
        name: 'create'
    },
    {
        path: '/tutor/registeration',
        component: t_register,
        name: 'tutorRegistration'
    },
    {
        path: '/learner/registeration',
        component: le_register,
        name: 'learnerRegistration'
    }
]