// This is a reference implementation to update the PROJECT_TEMPLATES object
// in scripts/dev/src/commands/new.ts

// Available project templates
const PROJECT_TEMPLATES = {
  'next-app': {
    description: 'Next.js application with TypeScript',
    generator: 'create-next-app',
    options: ['--typescript', '--eslint', '--tailwind', '--src-dir', '--app', '--import-alias="@/*"']
  },
  'api-service': {
    description: 'Express API service with TypeScript',
    generator: 'custom',
    source: 'api-service' // Source folder in templates/project-types
  },
  'cli-tool': {
    description: 'Command-line tool with TypeScript',
    generator: 'custom',
    source: 'cli-tool' // Source folder in templates/project-types
  },
  // Add the new fullstack-app template
  'fullstack-app': {
    description: 'Complete fullstack application with Next.js, Prisma, NextAuth and shadcn/ui',
    generator: 'custom',
    source: 'fullstack-app', // Source folder in templates/project-types
    postInstall: async (targetPath: string) => {
      // After template is copied, run these steps
      console.log('Setting up fullstack application...');
      
      // 1. Install dependencies
      await runCommand('npm', ['install'], targetPath);
      
      // 2. Initialize git repository
      await runCommand('git', ['init'], targetPath);
      await runCommand('git', ['add', '.'], targetPath);
      await runCommand('git', ['commit', '-m', 'Initial commit'], targetPath);
      
      // 3. Set up environment variables
      console.log('Creating .env file from example...');
      // Copy .env.example to .env if it doesn't exist
      if (!fs.existsSync(path.join(targetPath, '.env'))) {
        fs.copyFileSync(
          path.join(targetPath, '.env.example'),
          path.join(targetPath, '.env')
        );
      }
      
      console.log('Fullstack application setup complete! 🚀');
      console.log('');
      console.log('Next steps:');
      console.log('1. cd', path.basename(targetPath));
      console.log('2. npm run dev');
      console.log('3. Open http://localhost:3000 in your browser');
    }
  }
};