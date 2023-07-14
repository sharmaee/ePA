import axios from "axios";
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
  },
});

const ensureTrailingSlash = (s) => s + (s.endsWith("/") ? "" : "/");

executor.interceptors.request.use(
  (config) => {
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
