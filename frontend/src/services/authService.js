import api from "@/services/api";

const noAuthCfg = { _noAuthHeader: true };

const { post } = api.getPrefixedMethods("auth");

export default {
  register(userInfo) {
    return post("register", userInfo, noAuthCfg);
  },
  login(userCreds) {
    return post("sign-in", userCreds, noAuthCfg);
  },
  refreshToken(data) {
    return post("sign-in/refresh", data, { _isRefreshTokenRequest: true });
  },
  logout(refresh_token) {
    return post("sign-out", { refresh_token });
  },
  confirmEmail(user_id, otp) {
    return post(`activate/${user_id}/${otp}`, null, noAuthCfg);
  },
  passwordResetRequest(email) {
    return post("password_reset", { email }, noAuthCfg);
  },
  passwordReset(password, token) {
    return post("password_reset/confirm", { password, token }, noAuthCfg);
  },
  loginStep2(code) {
    return post("sign-in-step2", { code });
  },
};
