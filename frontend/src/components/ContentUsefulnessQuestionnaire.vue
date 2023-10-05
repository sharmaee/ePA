<template>
  <div class="usefulness-questionnaire-wrapper">
    <div v-if="!showPreloader && !requestSentSuccessfuly">
      <div class="buttons-wrapper">
        <h2>Was this helpful ?</h2>
        <div class="action-btn">
          <span
            class="like-button"
            :class="{ 'active-questionnaire-btn': feedbackData.isHelpful }"
            @click="changeIsHelpfulData(true)">
            <img v-if="feedbackData.isHelpful" src="@/assets/images/thumbs-up-white.svg" alt="like" />
            <img v-else src="@/assets/images/thumbs-up-blue.svg" alt="like" />
            <span>Yes</span>
          </span>
        </div>
        <div class="action-btn">
          <span
            class="dislike-button"
            :class="{ 'active-questionnaire-btn': !feedbackData.isHelpful && isHelpfullButtonClicked }"
            @click="changeIsHelpfulData(false)">
            <img
              v-if="!feedbackData.isHelpful && isHelpfullButtonClicked"
              src="@/assets/images/thumbs-up-white.svg"
              alt="dislike" />
            <img v-else src="@/assets/images/thumbs-up-blue.svg" alt="dislike" />
            <span>No</span>
          </span>
        </div>
      </div>
      <div v-if="isHelpfullButtonClicked" class="questionnaire-text-wrapper">
        <textarea
          v-model="feedbackData.comment"
          class="textarea"
          rows="8"
          placeholder="Leave a comment, question or suggestion here"></textarea>
        <br />
        <div class="questionnaire-text-btn-wrapper">
          <span class="action-btn" @click="sendQuestionnaireResult">Submit</span>
        </div>
      </div>
    </div>
    <GreenCirclePreloader v-if="showPreloader && !requestSentSuccessfuly" />
    <div v-if="requestSentSuccessfuly" class="final-request-message-wrapper">
      <span>Submission received, we are on it!</span>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRoute } from "vue-router";
import { userExperienceService } from "@/services/userExperienceService";
import { tryParseApiErrors } from "@/utils";
import GreenCirclePreloader from "@/components/GreenCirclePreloader";

const appVersion = process.env.VUE_APP_VERSION;
const isHelpfullButtonClicked = ref(false);
const route = useRoute();
const errors = ref([]);
const requestSentSuccessfuly = ref(false);
const showPreloader = ref(false);

const feedbackData = ref({
  isHelpful: "",
  releaseVersion: appVersion,
  comment: "",
  priorAuthRequirements: route.params.id,
});

function changeIsHelpfulData(value) {
  isHelpfullButtonClicked.value = true;
  feedbackData.value.isHelpful = value;
}

async function sendQuestionnaireResult() {
  try {
    showPreloader.value = true;
    await userExperienceService.submitFeedback(feedbackData.value);
    requestSentSuccessfuly.value = true;
    errors.value = [];
  } catch (error) {
    errors.value = tryParseApiErrors(error);
  }

  showPreloader.value = false;
}
</script>

<style lang="scss" scoped>
@import "../styles/components/_content-usefulness-questionnaire.scss";
</style>
