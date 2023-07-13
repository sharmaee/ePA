import api from "@/services/api";

const { get, post } = api.getPrefixedMethods("requirements");

export const mainServices = {
  availableSearchOptions() {
    return get("");
  },
  insuranceProvider(searchTerm) {
    return post(`search/`, searchTerm);
  },
};
