<template>
  <div class="usefulness-questionnaire-wrapper">
    <div class="buttons-wrapper">
      <h2>Was this helpful ?</h2>
      <span class="action-btn like-button" :class="{ green: likeButtonClicked }" @click="sendQuestionnaireResult(true)">
        <img src="@/assets/images/thumbs-up.svg" alt="like" />
        <span>Yes</span>
      </span>
      <span
        class="action-btn dislike-button"
        :class="{ red: dislikeButtonClicked }"
        @click="sendQuestionnaireResult(false)">
        <img src="@/assets/images/thumbs-up.svg" alt="dislike" />
        <span>No</span>
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const likeButtonClicked = ref(false);
const dislikeButtonClicked = ref(false);

async function sendQuestionnaireResult(result) {
  if (result) {
    likeButtonClicked.value = ref(true);
    setTimeout(() => (likeButtonClicked.value = false), 1000);
  } else {
    dislikeButtonClicked.value = true;
    setTimeout(() => (dislikeButtonClicked.value = false), 1000);
  }
}
</script>

<style lang="scss" scoped>
@import "../styles/components/_content-usefulness-questionnaire.scss";
</style>
