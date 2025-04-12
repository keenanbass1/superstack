/**
 * Context Formatters Index
 * Export all available formatters for use in the CLI and API
 */

// Import formatters, handling both named exports and default exports
const claudeMCP = require('./claude-mcp');
const formatForClaudeMCP = claudeMCP.formatForClaudeMCP || claudeMCP;

const anthropicMessages = require('./anthropic-messages');
const formatForAnthropicMessages = anthropicMessages.formatForAnthropicMessages || anthropicMessages;

const openaiAssistant = require('./openai-assistant');
const formatForOpenAIAssistant = openaiAssistant.formatForOpenAIAssistant || openaiAssistant;

const claudeCompletion = require('./claude-completion');
const formatForClaudeCompletion = claudeCompletion.formatForClaudeCompletion || claudeCompletion;

/**
 * Get list of available formatters with metadata
 * @returns {Object} Object containing formatter information
 */
function getAvailableFormatters() {
  return {
    'claude-mcp': {
      name: 'Claude MCP',
      description: 'Formats context for Claude Multi-Context Protocol',
      targetModel: 'claude',
      options: [
        { name: 'includeInactive', type: 'boolean', default: false },
        { name: 'includeMetadata', type: 'boolean', default: true },
        { name: 'defaultDomain', type: 'string', default: null },
        { name: 'wrapWithXML', type: 'boolean', default: true }
      ]
    },
    'anthropic-messages': {
      name: 'Anthropic Messages',
      description: 'Formats context for Anthropic Messages API',
      targetModel: 'claude',
      options: [
        { name: 'includeInactive', type: 'boolean', default: false },
        { name: 'defaultDomain', type: 'string', default: null },
        { name: 'addPreface', type: 'boolean', default: true },
        { name: 'addMetadata', type: 'boolean', default: false }
      ]
    },
    'openai-assistant': {
      name: 'OpenAI Assistant',
      description: 'Formats context for OpenAI Assistants API',
      targetModel: 'gpt',
      options: [
        { name: 'includeInactive', type: 'boolean', default: false },
        { name: 'defaultDomain', type: 'string', default: null },
        { name: 'formatAsFiles', type: 'boolean', default: false },
        { name: 'addMetadata', type: 'boolean', default: false }
      ]
    },
    'claude-completion': {
      name: 'Claude Completion',
      description: 'Formats context for Claude Completion API',
      targetModel: 'claude',
      options: [
        { name: 'includeInactive', type: 'boolean', default: false },
        { name: 'defaultDomain', type: 'string', default: null },
        { name: 'addMetadata', type: 'boolean', default: false },
        { name: 'preface', type: 'string', default: null },
        { name: 'systemPrompt', type: 'string', default: null }
      ]
    }
  };
}

module.exports = {
  formatForClaudeMCP,
  formatForAnthropicMessages,
  formatForOpenAIAssistant,
  formatForClaudeCompletion,
  getAvailableFormatters
};