import api from "@/services/api";

const { get, post } = api.getPrefixedMethods("requirements");

export const mainServices = {
  availableSearchOptions() {
    return get("");
  },
  searchRequirements(searchTerm) {
    return post(`search/`, searchTerm);
  },
};
