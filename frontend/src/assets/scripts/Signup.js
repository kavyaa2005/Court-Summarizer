// src/utils/validateSignup.js

/**
 * Validate Name
 * Rules:
 * - Only alphabets and spaces
 * - Length 3–50 characters
 */
export const validateName = (name) => {
  const re = /^[a-zA-Z\s]{3,50}$/;
  return re.test(name.trim());
};

/**
 * Validate Email
 * Rules:
 * - Only Gmail addresses allowed
 * - Format: username@gmail.com
 * - Username can include letters, numbers, dots, underscores
 */
export const validateEmail = (email) => {
  const re = /^[a-zA-Z0-9._%+-]+@gmail\.com$/;
  return re.test(email.trim().toLowerCase());
};

/**
 * Validate Password
 * Rules:
 * - Minimum 8 characters
 * - At least one uppercase, one lowercase, one number, one special character
 */
export const validatePassword = (password) => {
  const re =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$/;
  return re.test(password);
};

/**
 * Validate Occupation
 * Rules:
 * - Must not be empty
 */
export const validateOccupation = (occupation) => {
  return typeof occupation === "string" && occupation.trim().length > 0;
};

/**
 * Full Signup Validation
 */
export const validateSignup = ({ name, email, password, occupation }) => {
  return {
    name: validateName(name),
    email: validateEmail(email),
    password: validatePassword(password),
    occupation: validateOccupation(occupation),
  };
};
