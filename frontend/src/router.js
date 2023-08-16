// import Vue from 'vue'
/* eslint-disable */
import { createWebHistory, createRouter } from 'vue-router';


import HomePage from '@/pages/HomePage';
import RequirementsPage from '@/pages/RequirementsPage';
import RequestMissingRequirements from '@/pages/RequestMissingRequirements';


const publicAccessRoutes = [
    {
      path: "/",
      name: "home-page",
      component: HomePage,
      title: "home-page",
    },
    {
      path: "/check-my-coverage/:id",
      name: "check-my-coverage",
      component: RequirementsPage,
      title: "check-my-coverage",
    },
    {
      path: "/request-missing-requirements",
      name: "request-without-requirements",
      component: RequestMissingRequirements,
      title: "request-missing-requirements",
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
