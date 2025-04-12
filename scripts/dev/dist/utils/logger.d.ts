type LogLevel = 'info' | 'success' | 'warning' | 'error' | 'debug';
/**
 * Log a message with color and formatting
 */
export declare function log(message: string, level?: LogLevel): void;
/**
 * Create and return a spinner
 */
export declare function spinner(text: string): import("ora").Ora;
/**
 * Create a section header
 */
export declare function section(title: string): void;
export {};
