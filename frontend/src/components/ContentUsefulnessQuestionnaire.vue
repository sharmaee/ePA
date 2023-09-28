<template>
  <div class="usefulness-questionnaire-wrapper">
    <div class="buttons-wrapper">
      <h2>Was this helpful ?</h2>
      <span
        class="action-btn like-button"
        :class="{ 'active-questionnaire-btn': likeButtonClicked }"
        @click="selectInformationUsefulness(true)">
        <img v-if="!likeButtonClicked" src="@/assets/images/thumbs-up-blue.svg" alt="like" />
        <img v-else src="@/assets/images/thumbs-up-white.svg" alt="like" />
        <span>Yes</span>
      </span>
      <span
        class="action-btn dislike-button"
        :class="{ 'active-questionnaire-btn': dislikeButtonClicked }"
        @click="selectInformationUsefulness(false)">
        <img v-if="!dislikeButtonClicked" src="@/assets/images/thumbs-up-blue.svg" alt="dislike" />
        <img v-else src="@/assets/images/thumbs-up-white.svg" alt="dislike" />
        <span>No</span>
      </span>
    </div>
    <div v-if="likeButtonClicked || dislikeButtonClicked" class="questionnaire-text-wrapper">
      <textarea
        v-model="userComment"
        class="textarea"
        rows="8"
        placeholder="Leave a comment, question or suggestion here."></textarea>
      <br />
      <div class="questionnaire-text-btn-wrapper">
        <span class="action-btn" @click="sendQuestionnaireResult">Submit</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const likeButtonClicked = ref(false);
const dislikeButtonClicked = ref(false);
const userComment = ref(null);

function selectInformationUsefulness(result) {
  if (result && !likeButtonClicked.value && !dislikeButtonClicked.value) {
    likeButtonClicked.value = ref(true);
  } else if (!result && !dislikeButtonClicked.value && !likeButtonClicked.value) {
    dislikeButtonClicked.value = true;
  }
}

async function sendQuestionnaireResult() {
  console.log(userComment.value);
}
</script>

<style lang="scss" scoped>
@import "../styles/components/_content-usefulness-questionnaire.scss";
</style>
