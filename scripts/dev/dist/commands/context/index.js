import { init } from './init.js';
import { push } from './push.js';
import { validate } from './validate.js';
import { edit } from './edit.js';
export function contextCommand(program) {
    const contextCmd = program
        .command('context')
        .description('Manage project context');
    contextCmd
        .command('init')
        .description('Initialize project context')
        .action(init);
    contextCmd
        .command('push')
        .description('Push context to AI assistants')
        .option('-t, --target <target>', 'Target AI assistant (claude, gpt, cursor)', 'all')
        .action(push);
    contextCmd
        .command('validate')
        .description('Validate project context against schema')
        .action(validate);
    contextCmd
        .command('edit')
        .description('Edit project context')
        .action(edit);
}
//# sourceMappingURL=index.js.map