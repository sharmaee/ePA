// import Vue from 'vue'
/* eslint-disable */
import { createWebHistory, createRouter } from 'vue-router';

import HomePage from '@/pages/HomePage';

const publicAccessRoutes = [
    {
      path: "/",
      name: "home-page",
      component: HomePage,
      title: "home-page",
    },
  ];

const protectedRoutes = [];

for (const r of publicAccessRoutes) {
  r.meta = { title: r.title || 'Lamar Health' }
}

for (const r of protectedRoutes) {
  r.meta = { loginRequired: true, title: r.title || 'Lamar Health' }
}

const router = createRouter({
  history: createWebHistory(),
  linkActiveClass: 'active',
  routes: publicAccessRoutes.concat(protectedRoutes),
})

export default router
