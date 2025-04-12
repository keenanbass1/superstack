export declare enum LogEntryType {
    SESSION_START = "session_start",
    SESSION_END = "session_end",
    NOTE = "note",
    CHALLENGE = "challenge",
    SOLUTION = "solution",
    DECISION = "decision",
    DISCOVERY = "discovery"
}
export interface LogEntry {
    id: string;
    timestamp: string;
    type: LogEntryType;
    content: string;
    tags?: string[];
    metadata?: Record<string, any>;
}
export interface LogSession {
    id: string;
    startTime: string;
    endTime?: string;
    description: string;
    project?: string;
    entries: LogEntry[];
    tags?: string[];
    summary?: string;
}
export interface DailyLog {
    date: string;
    sessions: LogSession[];
    tags?: string[];
    summary?: string;
}
interface SessionState {
    currentSession?: string;
    lastSessionTime?: string;
}
/**
 * Get the path to the logs directory
 */
export declare function getLogsPath(): string;
/**
 * Get the path to the daily logs directory
 */
export declare function getDailyLogsPath(): string;
/**
 * Get the path to the sessions directory
 */
export declare function getSessionsPath(): string;
/**
 * Get the path to the project logs directory
 */
export declare function getProjectLogsPath(project: string): string;
/**
 * Get the path to the session state file
 */
export declare function getSessionStatePath(): string;
/**
 * Ensure all log directories exist
 */
export declare function ensureLogDirectories(): Promise<void>;
/**
 * Get the current date in YYYY-MM-DD format
 */
export declare function getCurrentDate(): string;
/**
 * Get the current time in ISO format
 */
export declare function getCurrentTimestamp(): string;
/**
 * Generate a session ID
 */
export declare function generateSessionId(): string;
/**
 * Get the current session state
 */
export declare function getSessionState(): Promise<SessionState>;
/**
 * Save the current session state
 */
export declare function saveSessionState(state: SessionState): Promise<void>;
/**
 * Get the current session ID
 */
export declare function getCurrentSessionId(): Promise<string | undefined>;
/**
 * Check if a session is currently active
 */
export declare function isSessionActive(): Promise<boolean>;
/**
 * Set the current session ID
 */
export declare function setCurrentSessionId(sessionId?: string): Promise<void>;
/**
 * Create a new log entry
 */
export declare function createLogEntry(type: LogEntryType, content: string, tags?: string[], metadata?: Record<string, any>): LogEntry;
/**
 * Get the path to a daily log file
 */
export declare function getDailyLogPath(date?: string): string;
/**
 * Get the path to a session log file
 */
export declare function getSessionLogPath(sessionId: string): string;
/**
 * Start a new log session
 */
export declare function startSession(description: string, project?: string, tags?: string[]): Promise<LogSession>;
/**
 * End the current log session
 */
export declare function endSession(summary?: string): Promise<LogSession | undefined>;
/**
 * Add an entry to the current session
 */
export declare function addEntryToCurrentSession(type: LogEntryType, content: string, tags?: string[]): Promise<LogEntry | undefined>;
/**
 * Save a session to file
 */
export declare function saveSession(session: LogSession): Promise<void>;
/**
 * Load a session from file
 */
export declare function loadSession(sessionId: string): Promise<LogSession | undefined>;
/**
 * Add a session to the daily log
 */
export declare function addSessionToDailyLog(session: LogSession): Promise<void>;
/**
 * Update a session in the daily log
 */
export declare function updateSessionInDailyLog(session: LogSession): Promise<void>;
/**
 * Add a session to the project log
 */
export declare function addSessionToProjectLog(session: LogSession, project: string): Promise<void>;
/**
 * Update a session in the project log
 */
export declare function updateSessionInProjectLog(session: LogSession, project: string): Promise<void>;
/**
 * Format a session as markdown
 */
export declare function formatSessionAsMarkdown(session: LogSession): string;
/**
 * Parse a session from markdown
 * This is a simplified implementation that creates a basic session object
 */
export declare function parseSessionFromMarkdown(markdown: string, sessionId: string): LogSession;
/**
 * Format a date for display
 */
export declare function formatDate(date: string): string;
/**
 * Format a time for display
 */
export declare function formatTime(time: string): string;
/**
 * Search for logs matching a term
 */
export declare function searchLogs(term: string, options?: {
    maxResults?: number;
    startDate?: string;
    endDate?: string;
    project?: string;
    tags?: string[];
}): Promise<{
    sessionId: string;
    match: string;
    context: string;
}[]>;
/**
 * Get a list of recent log sessions
 */
export declare function getRecentSessions(limit?: number, project?: string): Promise<LogSession[]>;
/**
 * Get all projects that have logs
 */
export declare function getProjectsWithLogs(): Promise<string[]>;
/**
 * Gather context information for a log session
 */
export declare function gatherSessionContext(): Record<string, any>;
/**
 * Generate a summary for a log session using pattern analysis
 * This is a simple implementation - a real implementation would be more sophisticated
 */
export declare function generateSessionSummary(session: LogSession): string;
export {};
