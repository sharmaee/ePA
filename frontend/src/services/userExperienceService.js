import api from "@/services/api";

const { post } = api.getPrefixedMethods("ux");

export const userExperienceService = {
  submitFeedback(feedbackData) {
    return post("", feedbackData);
  },
};
