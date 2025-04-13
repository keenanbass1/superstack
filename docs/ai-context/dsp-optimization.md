# DSP Context Module Optimization System Documentation

## Overview

The DSP Context Module Optimization System is a comprehensive framework for optimizing AI context modules using Demonstration-Supervised Program synthesis (DSPy). It enables automated optimization, evaluation, and application of AI context modules with integrated feedback collection and performance tracking.

## Components

### Core Components

1. **ContextOptimizer**
   - Optimizes context modules using DSPy techniques
   - Supports multiple optimization strategies (token reduction, clarity improvement)
   - Generates diffs between original and optimized modules

2. **ContextEvaluator**
   - Evaluates optimized modules against originals
   - Generates test cases based on module content
   - Quantifies improvements in effectiveness and token usage

3. **ContextFeedback**
   - Collects and analyzes user feedback
   - Tracks module effectiveness metrics
   - Identifies modules needing optimization based on usage data

4. **DSPClient**
   - Interfaces with the DSPy framework
   - Manages LLM connections and prompts
   - Configures optimization strategies

### Utility Scripts

1. **batch_optimize_modules.py**
   - Optimizes multiple modules in batch mode
   - Prioritizes modules based on feedback
   - Supports auto-application of improvements

2. **evaluate_modules.py**
   - Evaluates optimization effectiveness
   - Generates performance reports
   - Supports single and batch evaluation

3. **apply_optimizations.py**
   - Applies optimized modules to production
   - Creates automatic backups
   - Supports dry-run testing

4. **collect_feedback.py**
   - Records and processes user feedback
   - Tracks optimization history
   - Calculates effectiveness metrics

### CI/CD Integration

1. **GitHub Actions Workflow**
   - Automates optimization in CI pipeline
   - Creates PRs for optimized modules
   - Schedules regular optimization runs

2. **Build Integration**
   - Integrates with build pipeline
   - Checks for modules needing optimization
   - Supports pre-build optimization

## Purpose & Functionality

The system addresses several key challenges in managing AI context modules:

1. **Token Optimization**: Reduces token usage while preserving information content
2. **Clarity Improvement**: Enhances module structure and readability
3. **Quality Assurance**: Evaluates optimizations against original modules
4. **Feedback Integration**: Uses real-world feedback to prioritize optimization efforts
5. **Automated Workflow**: Integrates with CI/CD for continuous improvement

## Usage Guide

### Basic Usage

#### Optimizing a Single Module

```bash
python scripts/optimize_context.py optimize --module module_name
```

#### Batch Optimization

```bash
python scripts/batch_optimize_modules.py --limit 10 --output results.json
```

#### Evaluating Optimizations

```bash
python scripts/evaluate_modules.py --module module_name
```

#### Applying Optimizations

```bash
python scripts/apply_optimizations.py --module module_name
```

### Configuration

The system uses a YAML-based configuration file (`config/dsp_config.yaml`) to define settings:

- Model configuration (GPT-4, Claude, etc.)
- Optimization strategies and parameters
- Evaluation criteria and thresholds
- Directory structures and file paths

### CI/CD Integration

1. **GitHub Actions Workflow**:
   - Automatically triggered on schedule or manually
   - Set `auto_apply` to true for automatic optimization application
   - Customize improvement thresholds for quality control

2. **Build Pipeline Integration**:
   - Add to your build process with `build_integration.js`
   - Configure optimization thresholds and module limits
   - Enable auto-application of successful optimizations

### Feedback System

1. **Initializing the Database**:
   ```bash
   python scripts/init_feedback_db.py
   ```

2. **Recording Feedback**:
   ```bash
   python scripts/collect_feedback.py add --module module_name --type effectiveness --score 8
   ```

3. **Identifying Improvement Candidates**:
   ```bash
   python scripts/collect_feedback.py identify-candidates --threshold 6.0
   ```

## Examples

### Example 1: Manual Optimization Workflow

```bash
# 1. List modules to optimize
python scripts/optimize_context.py list

# 2. Optimize a specific module
python scripts/optimize_context.py optimize --module state_management

# 3. Evaluate the optimization
python scripts/optimize_context.py evaluate --module state_management

# 4. Apply if improvement is significant
python scripts/apply_optimizations.py --module state_management
```

### Example 2: Automated Batch Processing

```bash
# Run automated batch optimization with evaluation and auto-apply
python scripts/batch_optimize_modules.py --evaluate --auto-apply
```

### Example 3: CI Integration

```bash
# Check for modules needing optimization during build
node build_integration.js --check-modules --optimize
```

## Requirements

- Python 3.10+
- Node.js 14+ (for build integration)
- DSPy framework
- OpenAI API access (for GPT models)
- Anthropic API access (for Claude models)
- SQLite (for feedback database)

## Best Practices

1. Always review optimizations before applying to production
2. Set reasonable improvement thresholds (10%+ recommended)
3. Collect sufficient feedback before optimizing modules
4. Use model-specific strategies for best results
5. Regularly export and analyze optimization metrics 