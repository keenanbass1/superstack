import { Command } from 'commander';
import contextCommand from '../context.js';

// Export the command registration function
export function registerContext(program) {
  return contextCommand(program);
}
