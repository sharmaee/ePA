import { FORM_ERRORS_TEXT } from "@/utils/constants";

export function generateRandom4DigitNumber() {
  return Math.floor(Math.random() * (9999 - 1000 + 1)) + 1000;
}

export function sendFormByEnterClicking(event, sendRequest) {
  if (event.code === "Enter" || event.code === 76) {
    sendRequest();
  }
}

export function tryParseApiErrors(error) {
  let resultErrors = [];

  const validationErrors = error.response.data.validation_errors;

  if (validationErrors) {
    for (let key in validationErrors) {
      resultErrors.push(...validationErrors[key]);
    }
  } else if (error.response.data.source_error) {
    resultErrors = [error.response.data.source_error];
  } else {
    resultErrors = [FORM_ERRORS_TEXT.UNKNOWN_SERVER_ERROR];
  }

  return resultErrors;
}
