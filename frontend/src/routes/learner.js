import l_courses from '@/components/learner/myCourse.vue'
import learner from '@/components/learner/learner_course.vue'
import aiTutor from '@/components/learner/aiTutor.vue'
export default [
    {
        path: '/learner/my-courses',
        component: l_courses,
        name: 'learner-courses',
    },
    {
        path: '/learner/portal/:courseId/:courseName',
        component: learner,
        name: 'learner',
        props: true,
    },
    {
        path: '/learner/portal/use-aiTutor',
        component: aiTutor,
        name: 'AiTutor',
    },
]