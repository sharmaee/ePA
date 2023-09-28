import api from "@/services/api";

const { post } = api.getPrefixedMethods("ux");

export const denialService = {
  submitFeedback(feedbackData) {
    return post("", feedbackData);
  },
};
