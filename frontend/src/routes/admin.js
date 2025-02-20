import ad_home from '@/components/admin/ad_home.vue'
import ad_requests from '@/components/admin/ad_requests.vue'

export default [
    {
        path: '/admin',
        component: ad_home,
        name: 'admin',
    },
    {
        path: '/admin/requests',
        component: ad_requests,
        name: 'adminRequest',
    }
]