/**Contains interfaces for a generic API response. */

/**Interface for a generic API response */
export interface ApiSuccess {
  metadata: {
    [key: string]: any;
  },
  data: any;
}

/**Interface for a generic API error response */
export interface ApiError extends ApiSuccess {
  error: string | null
}