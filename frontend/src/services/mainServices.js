import api from "@/services/api";

const { get, post } = api.getPrefixedMethods("requirements");

export const mainServices = {
  availableSearchOptions() {
    return get("");
  },
  searchRequirements(searchTerm) {
    return post(`search/`, searchTerm);
  },
  getRequirementsData(id) {
    return get(`detail/${id}`);
  },
  requestRequirements(data) {
    return post(`request-requirements/`, data);
  },
  submitPriorAuthorization(data) {
    return post(`complete/`, data);
  },
};
