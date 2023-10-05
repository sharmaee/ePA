export const FORM_ERRORS_TEXT = {
  UNKNOWN_SERVER_ERROR: "Something went wrong. Please contact us at founders@lamarhealth.com",
};

export const FORM_VALIDATION_PATTERNS = {
  PASSWORD_PATTERN: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[ !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~]).{11,}$/,
  EMAIL_PATTERN: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  DOB_PATTERN: /^(0[1-9]|1[0-2])\/(0[1-9]|[12][0-9]|3[01])\/\d{4}$/,
  COVER_MY_MEDS_KEY_PATTERN: /^[A-Za-z0-9]{6,8}$/,
  PATIENT_MEMBER_ID_PATTERN: /^[A-Za-z0-9]{3,20}$/,
};
