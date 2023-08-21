import api from "@/services/api";

const { post } = api.getPrefixedMethods("");

export const denialService = {
  requestDenialReport(data) {
    return post(`denials/`, data);
  },
};
