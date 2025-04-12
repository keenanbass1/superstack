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
/**
 * Display a command suggestion
 */
export declare function command(cmd: string, description?: string): void;
export declare const logger: {
    log: typeof log;
    info: (message: string) => void;
    success: (message: string) => void;
    warn: (message: string) => void;
    error: (message: string, err?: Error) => void;
    debug: (message: string) => void;
    command: typeof command;
};
export {};
