import { createRouter, createWebHistory } from "vue-router";

import TestRoutes from "./test"
import Attenddance from "./attendance"

const routes = [
{
    path: '/',
    redirect: '/attendance'
},
...TestRoutes,
...Attenddance,
];

const router = createRouter({
history: createWebHistory(),
routes,
});

export default router;
