export default [
    {
        path: '/test',
        component: () => import('@/views/TestViews.vue'),
        children: [
        ],
    },
];