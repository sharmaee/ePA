export function generateRandom4DigitNumber() {
  return Math.floor(Math.random() * (9999 - 1000 + 1)) + 1000;
}

export function tryParseApiErrors(error) {
  let resultErrors = [];

  const validationErrors = error.response.data.validation_errors;

  if (validationErrors) {
    resultErrors.push("Followind validation errors detected: ");
    for (let key in validationErrors) {
      resultErrors.push(key + " " + "errors: " + validationErrors[key]);
    }
  } else if (error.response.data.error_details) {
    resultErrors = [error.response.data.error_details];
  } else {
    resultErrors = [FORM_ERRORS_TEXT.UNKNOWN_SERVER_ERROR];
  }
  return resultErrors;
}
