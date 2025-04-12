/**
 * Format a date using Intl.DateTimeFormat
 */
export function formatDate(date: Date | string | number, options?: Intl.DateTimeFormatOptions) {
  const defaultOptions: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }
  
  const dateToFormat = date instanceof Date ? date : new Date(date)
  
  return new Intl.DateTimeFormat(
    'en-US', 
    options || defaultOptions
  ).format(dateToFormat)
}

/**
 * Truncate a string to a maximum length
 */
export function truncate(str: string, maxLength: number) {
  if (str.length <= maxLength) return str
  return `${str.slice(0, maxLength)}...`
}

/**
 * Delay execution for a given amount of milliseconds
 */
export function delay(ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

/**
 * Generate a random string ID
 */
export function generateId(length = 6) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  let result = ''
  
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  
  return result
}

/**
 * Merge class names with Tailwind
 * Simple version - for more advanced needs, use tailwind-merge or clsx
 */
export function cn(...classes: (string | undefined | boolean)[]) {
  return classes.filter(Boolean).join(' ')
}
