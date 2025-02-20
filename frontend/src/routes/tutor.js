import status_page from '@/components/tutor/status.vue'
import t_course from '@/components/tutor/t_course.vue'
import tutor from '@/components/tutor/main_tutor.vue'
export default [
    {
        path: '/tutor/status',
        component: status_page,
        name: 'status',
    },
    {
        path: '/tutor/course',
        component: t_course,
        name: 'tutor-course',
    },
    {
        path: '/tutor/portal/:courseId/:courseName',
        component: tutor,
        name: 'tutor',
        props: true,
    },
]