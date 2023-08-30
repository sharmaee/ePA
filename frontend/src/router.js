// import Vue from 'vue'
/* eslint-disable */
import { createWebHistory, createRouter } from 'vue-router';


import HomePage from '@/pages/HomePage';
import InsuranceNavigatorPage from '@/pages/InsuranceNavigatorPage';
import RequirementsPage from '@/pages/RequirementsPage';
import RequestMissingRequirements from '@/pages/RequestMissingRequirements';
import RequestDenialReport from '@/pages/RequestDenialReport';
import SignUp from '@/pages/SignUp';
import SignIn from '@/pages/SignIn';
import PasswordReset from '@/pages/PasswordReset';


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
      name: "request-missing-requirements",
      component: RequestMissingRequirements,
      title: "request-missing-requirements",
    },
    {
      path: "/report-denial",
      name: "report-denial",
      component: RequestDenialReport,
      title: "report-denial",
    },
    {
      path: "/sign-up",
      name: "sign-up",
      component: SignUp,
      title: "sign-up",
    },
    {
      path: "/sign-in",
      name: "sign-in",
      component: SignIn,
      title: "sign-in",
    },
    {
      path: "/password-reset",
      name: "password-reset",
      component: PasswordReset,
      title: "password-reset",
    }
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
