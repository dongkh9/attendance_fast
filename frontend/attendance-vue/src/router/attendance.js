export default [
    {
        path: '/attendance',
        component: () => import('@/views/attendance/AttendanceRoot.vue'),
        children: [
        ],
    },
];