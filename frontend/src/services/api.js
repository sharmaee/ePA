import axios from "axios";
import Cookies from "js-cookie";
import { useAuthStore } from "@/stores";
import { decamelizeKeys, camelizeKeys } from "humps";
// The executor automatically converts the case of JSON props
// to match the python\javascript convention before\after
// sending the request. You can disable this behavior
// by setting config._skipPropsAdaptation to true.

const executor = axios.create({
  baseURL: "/api",
  timeout: 25000,
  headers: {
    "Content-Type": "application/json",
    "X-CSRFToken": Cookies.get("csrftoken"),
  },
});

const authHeader = "Authorization";
const ensureTrailingSlash = (s) => s + (s.endsWith("/") ? "" : "/");

executor.interceptors.request.use(
  (config) => {
    if (config._noAuthHeader) {
      return config;
    }

    const accessToken = useAuthStore().userInfo.access;

    if (accessToken) {
      config.headers[authHeader] = `Bearer ${accessToken}`;
    }

    if (!config._skipPropsAdaptation) {
      config.data = decamelizeKeys(config.data);
    }

    return config;
  },
  (error) => Promise.reject(error)
);

executor.interceptors.response.use(
  (res) => {
    // removing redundant data property

    if (res.config._returnFullResponse) return res;

    return res.config._skipPropsAdaptation ? res.data : camelizeKeys(res.data);
  },
  async (err) => {
    const config = err.config;

    // check if token has expired and needs refreshing
    // we do it only if request had a token and failed with Unauthorized
    // we don't do it if the failed request was Token Refresh request
    if (
      config.headers[authHeader] &&
      (err.response.status == 401 || err.response.status == 403) &&
      !config._isRefreshTokenRequest
    ) {
      // the token we use is not valid - we got "401 Unathorized" error
      if (config._refreshTokenAttempted) {
        throw err;
      }

      const authStore = useAuthStore();
      await authStore.refreshAccessToken();

      // trying to refresh the access token and repeat the call
      config._refreshTokenAttempted = true;

      // retry the previous API call with a new access token
      return executor(config);
    }

    throw err;
  }
);

executor.getPrefixedMethods = function (urlPrefix) {
  const newApi = {};
  urlPrefix = ensureTrailingSlash(urlPrefix);

  for (const m of ["get", "post", "put", "delete"]) {
    newApi[m] = (url, ...args) => executor[m](ensureTrailingSlash(urlPrefix + url), ...args);
  }

  return newApi;
};

export default executor;
