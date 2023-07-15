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
      path: "/flow-requirements",
      name: "flow-requirements",
      component: FlowRequirementsPage,
      title: "flow-requirements",
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
