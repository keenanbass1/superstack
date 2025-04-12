/**
 * Common types used throughout the application
 */

/**
 * Basic user information
 */
export interface User {
  id: string
  name: string
  email: string
  image?: string
  role?: 'user' | 'admin'
}

/**
 * Navigation item structure
 */
export interface NavItem {
  title: string
  href: string
  disabled?: boolean
  external?: boolean
  icon?: string
}

/**
 * Simple API response structure
 */
export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  message?: string
}

/**
 * Pagination metadata
 */
export interface PaginationInfo {
  page: number
  pageSize: number
  totalItems: number
  totalPages: number
  hasNext: boolean
  hasPrev: boolean
}

/**
 * Paginated data response
 */
export interface PaginatedResponse<T> {
  items: T[]
  pagination: PaginationInfo
}
