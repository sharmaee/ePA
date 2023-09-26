import { defineStore } from "pinia";
import { ref, computed } from "vue";

import authService from "@/services/authService";
import router from "@/router";

const userStorageKey = "user-auth-info";

export const useAuthStore = defineStore("auth", () => {
  const storedStr = localStorage.getItem(userStorageKey);
  const userInfo = ref(storedStr ? JSON.parse(storedStr) : {});
  const loggedIn = computed(
    () =>
      (userInfo.value.access && userInfo.value.secondStepCompleted) ||
      (userInfo.value.access && userInfo.value.secondStepNotRequired)
  );

  function setNewUserInfo(newUserInfo) {
    localStorage.setItem(userStorageKey, JSON.stringify(newUserInfo));
    userInfo.value = newUserInfo;
  }

  async function login(creds) {
    const { firstName, lastName, setupKey, otpAppUrl, access, refresh, secondStep } = await authService.login(creds);
    // login successful. save tokens to storage and use for API queries

    setNewUserInfo({ firstName, lastName, access, refresh });
    return { otpAppUrl, setupKey, secondStep };
  }

  async function loginStep2(code) {
    await authService.loginStep2(code);

    setNewUserInfo({ ...userInfo.value, secondStepCompleted: true });
  }

  async function loginStep2NotRequired() {
    setNewUserInfo({ ...userInfo.value, secondStepNotRequired: true });
  }

  async function refreshAccessToken() {
    const oldInfo = userInfo.value;
    try {
      const response = await authService.refreshToken(oldInfo);
      const newInfo = { ...oldInfo, ...response };

      // refresh successful. save tokens to storage and use for API queries
      setNewUserInfo(newInfo);
    } catch (error) {
      // refresh failed. clear local auth info
      clearUserInfo();
      // if refresh token is invalid, user is logged out, redirect to login page
      if ([401, 403].includes(error.response.status)) {
        router.push({ name: "login" });
      }
    }
  }

  async function logout() {
    try {
      await authService.logout(userInfo.value.refresh);
    } catch (error) {
      // if request failed with 401 or 403 user is already logged out and we can ignore it
      if (![401, 403].includes(error.response.status)) {
        // if it's an other problem, user is probably still logged in(refresh token is still valid)
        alert("Logout failed!");
        throw error;
      }
    }

    clearUserInfo();
  }

  function clearUserInfo() {
    // logout successful. forget token
    localStorage.removeItem(userStorageKey);
    userInfo.value = {};
  }

  return { login, logout, refreshAccessToken, userInfo, loggedIn, loginStep2, loginStep2NotRequired };
});
