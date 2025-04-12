import fs from 'fs-extra';
import path from 'path';
import { v4 as uuidv4 } from 'uuid';
import { format } from 'date-fns';
import { getPaths } from './paths.js';
import os from 'os';
import { execSync } from 'child_process';

// Define log entry types
export enum LogEntryType {
  SESSION_START = 'session_start',
  SESSION_END = 'session_end',
  NOTE = 'note',
  CHALLENGE = 'challenge',
  SOLUTION = 'solution',
  DECISION = 'decision',
  DISCOVERY = 'discovery'
}

// Define the log entry structure
export interface LogEntry {
  id: string;
  timestamp: string;
  type: LogEntryType;
  content: string;
  tags?: string[];
  metadata?: Record<string, any>;
}

// Define the session structure
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

// Define the daily log structure
export interface DailyLog {
  date: string;
  sessions: LogSession[];
  tags?: string[];
  summary?: string;
}

// Session state data stored in the user's config directory
interface SessionState {
  currentSession?: string;
  lastSessionTime?: string;
}

/**
 * Get the path to the logs directory
 */
export function getLogsPath(): string {
  const { logsDir } = getPaths();
  return logsDir;
}

/**
 * Get the path to the daily logs directory
 */
export function getDailyLogsPath(): string {
  return path.join(getLogsPath(), 'daily');
}

/**
 * Get the path to the sessions directory
 */
export function getSessionsPath(): string {
  return path.join(getLogsPath(), 'sessions');
}

/**
 * Get the path to the project logs directory
 */
export function getProjectLogsPath(project: string): string {
  return path.join(getLogsPath(), 'projects', project);
}

/**
 * Get the path to the session state file
 */
export function getSessionStatePath(): string {
  const configDir = path.join(os.homedir(), '.config', 'superstack');
  return path.join(configDir, 'session-state.json');
}

/**
 * Ensure all log directories exist
 */
export async function ensureLogDirectories(): Promise<void> {
  await fs.ensureDir(getDailyLogsPath());
  await fs.ensureDir(getSessionsPath());
  
  // Ensure config directory for session state
  const configDir = path.join(os.homedir(), '.config', 'superstack');
  await fs.ensureDir(configDir);
}

/**
 * Get the current date in YYYY-MM-DD format
 */
export function getCurrentDate(): string {
  return format(new Date(), 'yyyy-MM-dd');
}

/**
 * Get the current time in ISO format
 */
export function getCurrentTimestamp(): string {
  return new Date().toISOString();
}

/**
 * Generate a session ID
 */
export function generateSessionId(): string {
  const timestamp = format(new Date(), 'yyyyMMdd-HHmmss');
  return `session-${timestamp}`;
}

/**
 * Get the current session state
 */
export async function getSessionState(): Promise<SessionState> {
  const statePath = getSessionStatePath();
  
  try {
    if (await fs.pathExists(statePath)) {
      const data = await fs.readFile(statePath, 'utf8');
      return JSON.parse(data);
    }
  } catch (error) {
    // If there's an error reading the state, return a default state
    console.error('Error reading session state:', error);
  }
  
  return {};
}

/**
 * Save the current session state
 */
export async function saveSessionState(state: SessionState): Promise<void> {
  const statePath = getSessionStatePath();
  await fs.writeFile(statePath, JSON.stringify(state, null, 2), 'utf8');
}

/**
 * Get the current session ID
 */
export async function getCurrentSessionId(): Promise<string | undefined> {
  const state = await getSessionState();
  return state.currentSession;
}

/**
 * Check if a session is currently active
 */
export async function isSessionActive(): Promise<boolean> {
  const sessionId = await getCurrentSessionId();
  return !!sessionId;
}

/**
 * Set the current session ID
 */
export async function setCurrentSessionId(sessionId?: string): Promise<void> {
  const state = await getSessionState();
  
  if (sessionId) {
    state.currentSession = sessionId;
    state.lastSessionTime = getCurrentTimestamp();
  } else {
    delete state.currentSession;
  }
  
  await saveSessionState(state);
}

/**
 * Create a new log entry
 */
export function createLogEntry(
  type: LogEntryType,
  content: string,
  tags?: string[],
  metadata?: Record<string, any>
): LogEntry {
  return {
    id: uuidv4(),
    timestamp: getCurrentTimestamp(),
    type,
    content,
    tags,
    metadata
  };
}

/**
 * Get the path to a daily log file
 */
export function getDailyLogPath(date: string = getCurrentDate()): string {
  return path.join(getDailyLogsPath(), `${date}.md`);
}

/**
 * Get the path to a session log file
 */
export function getSessionLogPath(sessionId: string): string {
  return path.join(getSessionsPath(), `${sessionId}.md`);
}

/**
 * Start a new log session
 */
export async function startSession(
  description: string,
  project?: string,
  tags?: string[]
): Promise<LogSession> {
  // Ensure log directories exist
  await ensureLogDirectories();
  
  // Check if there's already an active session
  if (await isSessionActive()) {
    throw new Error('A session is already active. End it before starting a new one.');
  }
  
  // Create session ID
  const sessionId = generateSessionId();
  const startTime = getCurrentTimestamp();
  
  // Create session object
  const session: LogSession = {
    id: sessionId,
    startTime,
    description,
    project,
    entries: [],
    tags
  };
  
  // Add start entry
  const startEntry = createLogEntry(
    LogEntryType.SESSION_START,
    description,
    tags,
    { project }
  );
  
  session.entries.push(startEntry);
  
  // Save session to file
  await saveSession(session);
  
  // Update session state
  await setCurrentSessionId(sessionId);
  
  // Add session to daily log
  await addSessionToDailyLog(session);
  
  // If project is specified, add to project logs
  if (project) {
    await addSessionToProjectLog(session, project);
  }
  
  return session;
}

/**
 * End the current log session
 */
export async function endSession(summary?: string): Promise<LogSession | undefined> {
  // Get current session ID
  const sessionId = await getCurrentSessionId();
  
  if (!sessionId) {
    throw new Error('No active session to end.');
  }
  
  // Load the session
  const session = await loadSession(sessionId);
  
  if (!session) {
    throw new Error(`Could not load session: ${sessionId}`);
  }
  
  // Update session end time
  session.endTime = getCurrentTimestamp();
  
  // Add summary if provided
  if (summary) {
    session.summary = summary;
    
    // Add summary as a log entry
    const summaryEntry = createLogEntry(
      LogEntryType.SESSION_END,
      summary,
      session.tags
    );
    
    session.entries.push(summaryEntry);
  } else {
    // Add a simple end entry
    const endEntry = createLogEntry(
      LogEntryType.SESSION_END,
      'Session ended',
      session.tags
    );
    
    session.entries.push(endEntry);
  }
  
  // Save updated session
  await saveSession(session);
  
  // Update daily log
  await updateSessionInDailyLog(session);
  
  // If project is specified, update project log
  if (session.project) {
    await updateSessionInProjectLog(session, session.project);
  }
  
  // Clear current session
  await setCurrentSessionId();
  
  return session;
}

/**
 * Add an entry to the current session
 */
export async function addEntryToCurrentSession(
  type: LogEntryType,
  content: string,
  tags?: string[]
): Promise<LogEntry | undefined> {
  // Get current session ID
  const sessionId = await getCurrentSessionId();
  
  if (!sessionId) {
    throw new Error('No active session. Start a session first with "dev log start".');
  }
  
  // Load the session
  const session = await loadSession(sessionId);
  
  if (!session) {
    throw new Error(`Could not load session: ${sessionId}`);
  }
  
  // Create new entry
  const entry = createLogEntry(type, content, tags);
  
  // Add to session
  session.entries.push(entry);
  
  // Save session
  await saveSession(session);
  
  // Update daily log
  await updateSessionInDailyLog(session);
  
  // If project is specified, update project log
  if (session.project) {
    await updateSessionInProjectLog(session, session.project);
  }
  
  return entry;
}

/**
 * Save a session to file
 */
export async function saveSession(session: LogSession): Promise<void> {
  // Convert session to markdown
  const markdown = formatSessionAsMarkdown(session);
  
  // Write to session file
  const sessionPath = getSessionLogPath(session.id);
  await fs.writeFile(sessionPath, markdown, 'utf8');
}

/**
 * Load a session from file
 */
export async function loadSession(sessionId: string): Promise<LogSession | undefined> {
  const sessionPath = getSessionLogPath(sessionId);
  
  if (!await fs.pathExists(sessionPath)) {
    return undefined;
  }
  
  // Read session file
  const markdown = await fs.readFile(sessionPath, 'utf8');
  
  // Parse markdown to session object
  return parseSessionFromMarkdown(markdown, sessionId);
}

/**
 * Add a session to the daily log
 */
export async function addSessionToDailyLog(session: LogSession): Promise<void> {
  const date = format(new Date(session.startTime), 'yyyy-MM-dd');
  const dailyLogPath = getDailyLogPath(date);
  
  // Create daily log if it doesn't exist
  if (!await fs.pathExists(dailyLogPath)) {
    const header = `# Development Log: ${date}\n\n`;
    await fs.writeFile(dailyLogPath, header, 'utf8');
  }
  
  // Add session reference to daily log
  const sessionRef = `\n## Session: ${session.id}\n\n${session.description}\n\n`;
  await fs.appendFile(dailyLogPath, sessionRef, 'utf8');
}

/**
 * Update a session in the daily log
 */
export async function updateSessionInDailyLog(session: LogSession): Promise<void> {
  // This is a simplified implementation
  // In a real implementation, you would update the existing session entry
  // For now, we'll just call addSessionToDailyLog which will append the session
  
  // In a real implementation, you would:
  // 1. Read the daily log file
  // 2. Find the section for this session
  // 3. Update that section with the new session data
  // 4. Write the updated file
  
  // For this MVP, we'll skip this complexity
}

/**
 * Add a session to the project log
 */
export async function addSessionToProjectLog(session: LogSession, project: string): Promise<void> {
  const projectDir = getProjectLogsPath(project);
  const projectSessionsDir = path.join(projectDir, 'sessions');
  
  // Ensure project directories exist
  await fs.ensureDir(projectSessionsDir);
  
  // Create a link to the session file
  const sessionPath = getSessionLogPath(session.id);
  const projectSessionPath = path.join(projectSessionsDir, `${session.id}.md`);
  
  // Copy session file to project directory
  await fs.copy(sessionPath, projectSessionPath);
}

/**
 * Update a session in the project log
 */
export async function updateSessionInProjectLog(session: LogSession, project: string): Promise<void> {
  // Similar to updateSessionInDailyLog, this is simplified
  // In a real implementation, you would update the existing file
  
  // For this MVP, we'll just do a direct copy which will overwrite the file
  const projectDir = getProjectLogsPath(project);
  const projectSessionsDir = path.join(projectDir, 'sessions');
  const sessionPath = getSessionLogPath(session.id);
  const projectSessionPath = path.join(projectSessionsDir, `${session.id}.md`);
  
  await fs.copy(sessionPath, projectSessionPath, { overwrite: true });
}

/**
 * Format a session as markdown
 */
export function formatSessionAsMarkdown(session: LogSession): string {
  const lines: string[] = [];
  
  // Header
  lines.push(`# Development Log Session: ${session.id}`);
  lines.push('');
  
  // Session description
  lines.push(`## Description`);
  lines.push('');
  lines.push(session.description);
  lines.push('');
  
  // Session metadata
  lines.push(`## Metadata`);
  lines.push('');
  
  const startDateFormatted = format(new Date(session.startTime), 'yyyy-MM-dd HH:mm:ss');
  lines.push(`- **Start Time**: ${startDateFormatted}`);
  
  if (session.endTime) {
    const endDateFormatted = format(new Date(session.endTime), 'yyyy-MM-dd HH:mm:ss');
    lines.push(`- **End Time**: ${endDateFormatted}`);
    
    // Calculate duration
    const startDate = new Date(session.startTime);
    const endDate = new Date(session.endTime);
    const durationMs = endDate.getTime() - startDate.getTime();
    const durationMinutes = Math.floor(durationMs / 60000);
    
    lines.push(`- **Duration**: ${durationMinutes} minutes`);
  }
  
  if (session.project) {
    lines.push(`- **Project**: ${session.project}`);
  }
  
  if (session.tags && session.tags.length > 0) {
    lines.push(`- **Tags**: ${session.tags.join(', ')}`);
  }
  
  // Get git information if available
  try {
    const gitBranch = execSync('git branch --show-current', { encoding: 'utf8' }).trim();
    if (gitBranch) {
      lines.push(`- **Git Branch**: ${gitBranch}`);
    }
  } catch (error) {
    // Not in a git repository or git not available
  }
  
  lines.push('');
  
  // Log entries
  if (session.entries && session.entries.length > 0) {
    lines.push(`## Log Entries`);
    lines.push('');
    
    for (const entry of session.entries) {
      // Skip internal entries (SESSION_START, SESSION_END)
      if (entry.type === LogEntryType.SESSION_START || 
          (entry.type === LogEntryType.SESSION_END && !session.summary)) {
        continue;
      }
      
      const entryTime = format(new Date(entry.timestamp), 'HH:mm:ss');
      
      // Format based on entry type
      switch (entry.type) {
        case LogEntryType.NOTE:
          lines.push(`### ${entryTime} - Note`);
          break;
        case LogEntryType.CHALLENGE:
          lines.push(`### ${entryTime} - Challenge`);
          break;
        case LogEntryType.SOLUTION:
          lines.push(`### ${entryTime} - Solution`);
          break;
        case LogEntryType.DECISION:
          lines.push(`### ${entryTime} - Decision`);
          break;
        case LogEntryType.DISCOVERY:
          lines.push(`### ${entryTime} - Discovery`);
          break;
        case LogEntryType.SESSION_END:
          lines.push(`### ${entryTime} - Summary`);
          break;
        default:
          lines.push(`### ${entryTime} - Entry`);
      }
      
      lines.push('');
      lines.push(entry.content);
      
      if (entry.tags && entry.tags.length > 0) {
        lines.push('');
        lines.push(`Tags: ${entry.tags.join(', ')}`);
      }
      
      lines.push('');
    }
  }
  
  // Summary
  if (session.summary) {
    lines.push(`## Summary`);
    lines.push('');
    lines.push(session.summary);
    lines.push('');
  }
  
  return lines.join('\n');
}

/**
 * Parse a session from markdown
 * This is a simplified implementation that creates a basic session object
 */
export function parseSessionFromMarkdown(markdown: string, sessionId: string): LogSession {
  // This is a simplified parser - a real implementation would properly parse the markdown
  // For this MVP, we'll extract minimal information
  
  const lines = markdown.split('\n');
  
  // Extract description - first ## section
  let description = '';
  let inDescription = false;
  
  for (const line of lines) {
    if (line.startsWith('## Description')) {
      inDescription = true;
      continue;
    } else if (inDescription && line.startsWith('##')) {
      inDescription = false;
      break;
    }
    
    if (inDescription && line.trim() !== '') {
      description += line + '\n';
    }
  }
  
  description = description.trim();
  
  // Extract metadata
  let project: string | undefined;
  let tags: string[] | undefined;
  let startTime = '';
  let endTime: string | undefined;
  
  for (const line of lines) {
    if (line.includes('**Project**:')) {
      project = line.split('**Project**:')[1].trim();
    } else if (line.includes('**Tags**:')) {
      const tagsPart = line.split('**Tags**:')[1].trim();
      tags = tagsPart.split(',').map(tag => tag.trim());
    } else if (line.includes('**Start Time**:')) {
      const timeStr = line.split('**Start Time**:')[1].trim();
      startTime = new Date(timeStr).toISOString();
    } else if (line.includes('**End Time**:')) {
      const timeStr = line.split('**End Time**:')[1].trim();
      endTime = new Date(timeStr).toISOString();
    }
  }
  
  // Extract summary
  let summary: string | undefined;
  let inSummary = false;
  let summaryLines: string[] = [];
  
  for (const line of lines) {
    if (line.startsWith('## Summary')) {
      inSummary = true;
      continue;
    } else if (inSummary && line.startsWith('##')) {
      inSummary = false;
      break;
    }
    
    if (inSummary && line.trim() !== '') {
      summaryLines.push(line);
    }
  }
  
  if (summaryLines.length > 0) {
    summary = summaryLines.join('\n').trim();
  }
  
  // This is a simplified version - in a real implementation,
  // you would also parse the log entries
  const entries: LogEntry[] = [];
  
  return {
    id: sessionId,
    startTime: startTime || getCurrentTimestamp(),
    endTime,
    description,
    project,
    entries,
    tags,
    summary
  };
}

/**
 * Format a date for display
 */
export function formatDate(date: string): string {
  return format(new Date(date), 'yyyy-MM-dd');
}

/**
 * Format a time for display
 */
export function formatTime(time: string): string {
  return format(new Date(time), 'HH:mm:ss');
}

/**
 * Search for logs matching a term
 */
export async function searchLogs(
  term: string,
  options: {
    maxResults?: number;
    startDate?: string;
    endDate?: string;
    project?: string;
    tags?: string[];
  } = {}
): Promise<{ sessionId: string; match: string; context: string }[]> {
  const { maxResults = 10, startDate, endDate, project, tags } = options;
  
  // Get all session files
  let sessionsDir = getSessionsPath();
  
  // If project is specified, search in project directory
  if (project) {
    sessionsDir = path.join(getProjectLogsPath(project), 'sessions');
    if (!await fs.pathExists(sessionsDir)) {
      return [];
    }
  }
  
  // List all session files
  const files = await fs.readdir(sessionsDir);
  const sessionFiles = files.filter(file => file.endsWith('.md'));
  
  // Results array
  const results: { sessionId: string; match: string; context: string }[] = [];
  
  // Search through each file
  for (const file of sessionFiles) {
    // Extract session ID from filename
    const sessionId = path.basename(file, '.md');
    
    // Skip if before start date or after end date
    if (startDate || endDate) {
      const sessionDate = sessionId.split('-')[1].substring(0, 8); // Extract YYYYMMDD
      
      if (startDate && sessionDate < startDate.replace(/-/g, '')) {
        continue;
      }
      
      if (endDate && sessionDate > endDate.replace(/-/g, '')) {
        continue;
      }
    }
    
    // Read file content
    const filePath = path.join(sessionsDir, file);
    const content = await fs.readFile(filePath, 'utf8');
    
    // Check if content contains search term
    if (content.toLowerCase().includes(term.toLowerCase())) {
      // Find all lines with the term
      const lines = content.split('\n');
      const matchingLines: string[] = [];
      
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        
        if (line.toLowerCase().includes(term.toLowerCase())) {
          // Get context (lines before and after)
          const contextStart = Math.max(0, i - 2);
          const contextEnd = Math.min(lines.length - 1, i + 2);
          
          // Build context string
          const context: string[] = [];
          for (let j = contextStart; j <= contextEnd; j++) {
            if (j === i) {
              // Highlight the matching line
              context.push(`> ${lines[j]}`);
            } else {
              context.push(`  ${lines[j]}`);
            }
          }
          
          matchingLines.push(context.join('\n'));
          
          // If we have enough results, stop
          if (matchingLines.length >= maxResults) {
            break;
          }
        }
      }
      
      // Add each matching line as a separate result
      for (const match of matchingLines) {
        results.push({
          sessionId,
          match: term,
          context: match
        });
        
        // If we have enough total results, stop
        if (results.length >= maxResults) {
          break;
        }
      }
    }
    
    // If we have enough total results, stop
    if (results.length >= maxResults) {
      break;
    }
  }
  
  return results;
}

/**
 * Get a list of recent log sessions
 */
export async function getRecentSessions(
  limit: number = 5, 
  project?: string
): Promise<LogSession[]> {
  // Get all session files
  let sessionsDir = getSessionsPath();
  
  // If project is specified, use project directory
  if (project) {
    sessionsDir = path.join(getProjectLogsPath(project), 'sessions');
    if (!await fs.pathExists(sessionsDir)) {
      return [];
    }
  }
  
  // List all session files
  const files = await fs.readdir(sessionsDir);
  const sessionFiles = files.filter(file => file.endsWith('.md'));
  
  // Sort by filename (which includes timestamp)
  sessionFiles.sort().reverse();
  
  // Load recent sessions
  const sessions: LogSession[] = [];
  
  for (let i = 0; i < Math.min(limit, sessionFiles.length); i++) {
    const file = sessionFiles[i];
    const sessionId = path.basename(file, '.md');
    const session = await loadSession(sessionId);
    
    if (session) {
      sessions.push(session);
    }
  }
  
  return sessions;
}

/**
 * Get all projects that have logs
 */
export async function getProjectsWithLogs(): Promise<string[]> {
  const projectsDir = path.join(getLogsPath(), 'projects');
  
  if (!await fs.pathExists(projectsDir)) {
    return [];
  }
  
  const files = await fs.readdir(projectsDir);
  return files.filter(async file => {
    const stats = await fs.stat(path.join(projectsDir, file));
    return stats.isDirectory();
  });
}

/**
 * Gather context information for a log session
 */
export function gatherSessionContext(): Record<string, any> {
  const context: Record<string, any> = {
    os: os.platform(),
    hostname: os.hostname(),
    username: os.userInfo().username,
    directory: process.cwd()
  };
  
  // Try to get git information
  try {
    context.git = {
      branch: execSync('git branch --show-current', { encoding: 'utf8' }).trim(),
      lastCommit: execSync('git log -1 --pretty=%B', { encoding: 'utf8' }).trim(),
      modifiedFiles: execSync('git diff --name-only', { encoding: 'utf8' }).trim().split('\n')
    };
  } catch (error) {
    // Not in a git repository or git not available
  }
  
  // Try to get package.json info if it exists
  try {
    const packageJsonPath = path.join(process.cwd(), 'package.json');
    if (fs.existsSync(packageJsonPath)) {
      const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
      context.package = {
        name: packageJson.name,
        version: packageJson.version,
        dependencies: packageJson.dependencies,
        devDependencies: packageJson.devDependencies
      };
    }
  } catch (error) {
    // No package.json or error reading it
  }
  
  return context;
}

/**
 * Generate a summary for a log session using pattern analysis
 * This is a simple implementation - a real implementation would be more sophisticated
 */
export function generateSessionSummary(session: LogSession): string {
  const lines: string[] = [];
  
  // Add basic info
  lines.push(`Session on ${formatDate(session.startTime)} focused on: ${session.description}`);
  lines.push('');
  
  // Count entry types
  const entryCounts: Record<LogEntryType, number> = {
    [LogEntryType.SESSION_START]: 0,
    [LogEntryType.SESSION_END]: 0,
    [LogEntryType.NOTE]: 0,
    [LogEntryType.CHALLENGE]: 0,
    [LogEntryType.SOLUTION]: 0,
    [LogEntryType.DECISION]: 0,
    [LogEntryType.DISCOVERY]: 0
  };
  
  for (const entry of session.entries) {
    entryCounts[entry.type] = (entryCounts[entry.type] || 0) + 1;
  }
  
  // Add entry summary
  if (entryCounts[LogEntryType.CHALLENGE] > 0) {
    lines.push(`Faced ${entryCounts[LogEntryType.CHALLENGE]} challenge(s)`);
  }
  
  if (entryCounts[LogEntryType.SOLUTION] > 0) {
    lines.push(`Found ${entryCounts[LogEntryType.SOLUTION]} solution(s)`);
  }
  
  if (entryCounts[LogEntryType.DECISION] > 0) {
    lines.push(`Made ${entryCounts[LogEntryType.DECISION]} decision(s)`);
  }
  
  if (entryCounts[LogEntryType.DISCOVERY] > 0) {
    lines.push(`Documented ${entryCounts[LogEntryType.DISCOVERY]} discovery/discoveries`);
  }
  
  // Add duration if available
  if (session.endTime) {
    const startDate = new Date(session.startTime);
    const endDate = new Date(session.endTime);
    const durationMs = endDate.getTime() - startDate.getTime();
    const durationMinutes = Math.floor(durationMs / 60000);
    
    lines.push(`\nSession duration: ${durationMinutes} minutes`);
  }
  
  return lines.join('\n');
}
