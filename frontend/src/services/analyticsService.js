import api from "@/services/api";

const { post } = api.getPrefixedMethods("analytics");

export const analyticsServices = {
  logRequirementsSearchAction(data) {
    return post(`log-requirements-search/`, data);
  },
};
