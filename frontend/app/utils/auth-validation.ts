const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export interface PasswordChecks {
  hasLength: boolean
  hasUppercase: boolean
  hasLowercase: boolean
  hasNumber: boolean
  hasSymbol: boolean
  isValid: boolean
}

export function isValidEmail(value: string): boolean {
  return EMAIL_PATTERN.test(value.trim())
}

export function getPasswordChecks(value: string): PasswordChecks {
  const checks = {
    hasLength: value.length >= 8 && value.length <= 128,
    hasUppercase: /[A-Z]/.test(value),
    hasLowercase: /[a-z]/.test(value),
    hasNumber: /\d/.test(value),
    hasSymbol: /[^A-Za-z0-9]/.test(value),
  }
  const characterClasses = [
    checks.hasUppercase,
    checks.hasLowercase,
    checks.hasNumber,
    checks.hasSymbol,
  ].filter(Boolean).length

  return { ...checks, isValid: checks.hasLength && characterClasses >= 3 }
}
