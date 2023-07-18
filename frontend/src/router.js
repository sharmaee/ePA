// import Vue from 'vue'
/* eslint-disable */
import { createWebHistory, createRouter } from 'vue-router';


import HomePage from '@/pages/HomePage';
import FlowRequirementsPage from '@/pages/FlowRequirementsPage';


const publicAccessRoutes = [
    {
      path: "/",
      name: "home-page",
      component: HomePage,
      title: "home-page",
    },
    {
      path: "/check-my-coverage",
      name: "check-my-coverage",
      component: FlowRequirementsPage,
      title: "check-my-coverage",
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
