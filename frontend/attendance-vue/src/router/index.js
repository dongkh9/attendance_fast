import { createRouter, createWebHistory } from "vue-router";

import TestRoutes from "./test"

const routes = [
{
    path: '/',
    redirect: '/attendance'
},
...TestRoutes,
];

const router = createRouter({
history: createWebHistory(),
routes,
});

export default router;
