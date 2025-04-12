import { Command } from 'commander';
import { solve } from './solve.js';
import { generate } from './generate.js';
import { review } from './review.js';

export function aiCommand(program: Command): void {
  const aiCmd = program
    .command('ai')
    .description('AI assistance commands');
  
  aiCmd
    .command('solve <problem>')
    .description('Get AI help to solve a problem')
    .option('-m, --model <model>', 'AI model to use (claude, gpt)', 'claude')
    .option('-c, --context', 'Include project context', true)
    .option('-n, --no-context', 'Exclude project context')
    .action(solve);
  
  aiCmd
    .command('generate <type>')
    .description('Generate code/content using AI')
    .option('-d, --description <description>', 'Description of what to generate')
    .option('-m, --model <model>', 'AI model to use (claude, gpt)', 'claude')
    .option('-c, --context', 'Include project context', true)
    .option('-n, --no-context', 'Exclude project context')
    .action(generate);
  
  aiCmd
    .command('review <path>')
    .description('Get AI code review')
    .option('-m, --model <model>', 'AI model to use (claude, gpt)', 'claude')
    .option('-c, --context', 'Include project context', true)
    .option('-n, --no-context', 'Exclude project context')
    .action(review);
}