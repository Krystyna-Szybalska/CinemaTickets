export function useValidation() {
  function required(v, options = { errorMessage: '' }) {
    return !!v || options.errorMessage;
  }

  return {
    required,
  };
}
