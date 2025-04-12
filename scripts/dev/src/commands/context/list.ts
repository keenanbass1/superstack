import { Command } from 'commander';
import ora from 'ora';
import chalk from 'chalk';
import { getAllContextModules, getActiveContext, ContextModule } from '../../utils/contextModules.js';
import { logger } from '../../utils/logger.js';

export const listCommand = new Command('list')
  .description('List available context modules')
  .option('-d, --domain <domain>', 'Filter by domain')
  .option('-t, --type <type>', 'Filter by type')
  .option('-a, --active', 'Show only active modules', false)
  .option('-j, --json', 'Output as JSON', false)
  .action(async (options) => {
    const spinner = ora('Loading context modules...').start();
    
    try {
      // Get all modules
      const modules = await getAllContextModules();
      
      // Get active modules if needed
      let activeModules: string[] = [];
      if (options.active) {
        const activeContext = await getActiveContext();
        activeModules = activeContext.modules;
      }
      
      spinner.stop();
      
      // Apply filters
      let filtered = modules;
      
      if (options.domain) {
        filtered = filtered.filter(m => m.domain === options.domain);
      }
      
      if (options.type) {
        filtered = filtered.filter(m => m.type === options.type);
      }
      
      if (options.active) {
        filtered = filtered.filter(m => activeModules.includes(m.path));
      }
      
      // Handle no results
      if (filtered.length === 0) {
        console.log(chalk.yellow('No context modules found matching your criteria.'));
        return;
      }
      
      // Output as JSON if requested
      if (options.json) {
        console.log(JSON.stringify(filtered, null, 2));
        return;
      }
      
      // Group by domain and type
      const grouped = filtered.reduce((acc, module) => {
        const key = `${module.domain}/${module.type}`;
        acc[key] = acc[key] || [];
        acc[key].push(module);
        return acc;
      }, {} as Record<string, ContextModule[]>);
      
      // Output as table
      console.log(chalk.cyan(`\nFound ${filtered.length} context modules:`));
      
      Object.entries(grouped).forEach(([key, modules]) => {
        console.log(chalk.cyan(`\n${key}`));
        console.log(chalk.cyan('─'.repeat(key.length)));
        
        modules.forEach(module => {
          const relativePath = module.path.replace(`${module.domain}/${module.type}/`, '');
          const isActive = activeModules.includes(module.path);
          const statusIndicator = isActive ? chalk.green('●') : ' ';
          
          console.log(`${statusIndicator} ${chalk.green(relativePath)} - ${module.description}`);
        });
      });
      
      // If showing active context, display summary
      if (options.active && activeModules.length > 0) {
        console.log(chalk.cyan(`\nCurrently active: ${activeModules.length} modules`));
      }
      
    } catch (error) {
      spinner.fail('Failed to list context modules');
      logger.error('Error listing context modules', error as Error);
    }
  });
