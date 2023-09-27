import api from "@/services/api";

const { post } = api.getPrefixedMethods("ux");

export const denialService = {
  requestDenialReport(bool) {
    return post(`is_helpful`, bool);
  },
};

// поля які треба/можна відправляти:
// is_helpful - булеве значення
// comment - якщо будемо додавати поле, опційно
// release_version - зі енв змінної
// prior_auth_requirements - слаг з урли
