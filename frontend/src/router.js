// import Vue from 'vue'
/* eslint-disable */
import { createWebHistory, createRouter } from 'vue-router';
import { trackRouter } from "vue-gtag-next";
import { useAuthStore } from "@/stores";

import HomePage from '@/pages/HomePage';
import InsuranceNavigatorPage from '@/pages/InsuranceNavigatorPage';
import RequirementsPage from '@/pages/RequirementsPage';
import RequestMissingRequirements from '@/pages/RequestMissingRequirements';
import RequestDenialReport from '@/pages/RequestDenialReport';
import SignUp from '@/pages/SignUp';
import SignIn from '@/pages/SignIn';
import PasswordResetRequest from '@/pages/PasswordResetRequest';
import PasswordReset from '@/pages/PasswordReset';
import ConfirmEmail from '@/pages/ConfirmEmail'


const publicAccessRoutes = [
  {
    path: "/register",
    name: "register",
    component: SignUp,
    title: "Do Prior Auth",
  },
  {
    path: "/login",
    name: "login",
    component: SignIn,
    title: "Do Prior Auth",
  },
  {
    path: "/password-reset-request",
    name: "password-reset-request",
    component: PasswordResetRequest,
    title: "Rassword Reset Request",
  },
  {
    path: "/confirm-email/:user_id/:token",
    name: "confirmEmail",
    component: ConfirmEmail,
    title: "Lamar Health",
  },
  {
    path: "/password-reset/:token?",
    name: "password-reset",
    component: PasswordReset,
    title: "Password Reset",
  },
];

const protectedRoutes = [
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
];

for (const r of publicAccessRoutes) {
  r.meta = { title: r.title || 'Do Prior Auth' }
}

for (const r of protectedRoutes) {
  r.meta = { loginRequired: true, title: r.title || 'Do Prior Auth' }
}

const router = createRouter({
  history: createWebHistory(),
  linkActiveClass: "active",
  routes: publicAccessRoutes.concat(protectedRoutes),
});

router.beforeEach((to) => {
  const authManager = useAuthStore();
  document.title = to.meta.title;
  if (!authManager.loggedIn && to.meta.loginRequired) {
    return { name: "login" };
  }
});

trackRouter(router);

export default router;