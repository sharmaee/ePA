// import Vue from 'vue'
/* eslint-disable */
import { createWebHistory, createRouter } from 'vue-router';


import HomePage from '@/pages/HomePage';
import InsuranceNavigatorPage from '@/pages/InsuranceNavigatorPage';
import RequirementsPage from '@/pages/RequirementsPage';
import RequestMissingRequirements from '@/pages/RequestMissingRequirements';
import RequestDenialReport from '@/pages/RequestDenialReport';


const publicAccessRoutes = [
    {
      path: "/",
      name: "home-page",
      component: HomePage,
      title: "home-page",
    },
    {
      path: "/insurance-navigator-page",
      name: "insurance-navigator-page",
      component: InsuranceNavigatorPage,
      title: "insurance-navigator-page",
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
    {
      path: "/report-denial",
      name: "report-denial",
      component: RequestDenialReport,
      title: "report-denial",
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
