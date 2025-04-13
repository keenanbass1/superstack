DSPy Reference Documentation

Essential DSPy documentation integrated with the Superstack Context Optimization System

Overview
This reference documentation covers the core concepts and components of DSPy that are utilized within the Superstack Context Optimization System. DSPy is a framework for programming with foundation models that allows for systematic prompt optimization, consistent output structure, and chain-of-thought reasoning.
Core Concepts
What is DSPy?
DSPy is a programming framework that provides abstractions for working with large language models. It allows developers to:

Define structured prompts and expected response formats
Create reasoning chains that build on intermediate responses
Optimize prompts for specific models and tasks
Evaluate model responses against defined metrics

Unlike raw prompt engineering, DSPy provides programmatic control over language model interactions, enabling more reliable and consistent outcomes.
Key Components
The DSPy framework consists of several key components:

Signatures: Define input/output specifications
Modules: Encapsulate prompt logic and reasoning patterns
Optimizers: Improve prompts through systematic techniques
Teleprompters: Specialized prompt optimizers
Metrics: Evaluate model performance

Signatures
Signatures define the structure of inputs and outputs for language model tasks. They are the building blocks of DSPy programs.
InputField and OutputField
pythonclass OptimizeContext(dspy.Signature):
    """Optimize a context module for AI consumption"""
    original_content = dspy.InputField(desc="Original context module content")
    target_model = dspy.InputField(desc="Target AI model (claude, gpt)")
    optimized_content = dspy.OutputField(desc="Optimized context module")
In this example:

original_content and target_model are inputs
optimized_content is the expected output

Field Descriptors
Each field includes a description that guides the language model. Additional properties can include:

prefix: Text to prepend to the field value
desc: Detailed description of the field
format: Expected format of the output (e.g., JSON, Markdown)

Using Signatures
Signatures are used with modules to create executable language model tasks:
pythonoptimizer = dspy.ChainOfThought(OptimizeContext)
result = optimizer(
    original_content="...",
    target_model="claude"
)
optimized_content = result.optimized_content
Modules
Modules implement different reasoning patterns and prompt strategies.
ChainOfThought
pythonoptimizer = dspy.ChainOfThought(OptimizeContext)
The ChainOfThought module instructs the language model to show its reasoning before providing a final answer. This technique often improves the quality of responses by encouraging the model to think step-by-step.
Predict
pythonbasic_optimizer = dspy.Predict(OptimizeContext)
The Predict module is simpler than ChainOfThought and doesn't explicitly request reasoning steps. It's suitable for straightforward tasks where detailed reasoning isn't necessary.
ReAct
pythonreactive_optimizer = dspy.ReAct(OptimizeContext)
The ReAct module combines reasoning and action in an iterative process. It's useful for tasks that benefit from reflection on intermediate results.
MultiStagePrompt
pythonmulti_stage = dspy.MultiStagePrompt(
    stage1_module,
    stage2_module,
    stage3_module
)
The MultiStagePrompt module chains multiple modules together, using the output of each stage as input to the next. It's useful for complex tasks that benefit from breaking down the reasoning process.
Optimization
DSPy provides tools for systematically improving prompts based on examples and feedback.
Teleprompters
pythonteleprompter = dspy.teleprompt.BootstrapFewShot(
    demo_examples,
    metric=dspy.teleprompt.AccuracyMetric(),
    max_bootstrapped_demos=3
)

# Optimize a module using examples
optimized_module = teleprompter.compile(base_module)
Teleprompters use successful examples to generate improved prompts. They analyze what works well and incorporate those patterns into new prompts.
Tracing and Introspection
pythonwith dspy.context(trace=True):
    result = optimizer(...)

# Access the trace
print(dspy.trace.get())
Tracing allows you to inspect the complete interaction with the language model, including intermediate reasoning steps.
Evaluation
DSPy includes tools for evaluating model performance against defined metrics.
Basic Metrics
pythonaccuracy = dspy.evaluate(
    module=optimizer,
    examples=test_examples,
    metric=dspy.metrics.Accuracy()
)
Common metrics include:

Accuracy: Binary correct/incorrect assessment
RougeMetric: Measures overlap between generated and reference text
F1Metric: Balances precision and recall

Custom Metrics
pythonclass OptimizationImprovement(dspy.Metric):
    def __call__(self, example, prediction, trace=None):
        # Custom logic to evaluate improvement
        original_quality = assess_quality(example.original_content)
        optimized_quality = assess_quality(prediction.optimized_content)
        return optimized_quality - original_quality
Custom metrics allow you to define task-specific evaluation criteria.
Integration with Superstack
The Superstack Context Optimization System leverages DSPy in the following ways:
Context Module Optimization
Our system uses ChainOfThought for intelligent optimization of context modules:
pythondef optimize_module(self, module_name, target_model="claude"):
    # Load module content
    content = self.load_context_module(module_path)
    
    # Create DSPy signature and optimizer
    OptimizeContext = self.create_signature(target_model)
    optimizer = dspy.ChainOfThought(OptimizeContext)
    
    # Run optimization
    result = optimizer(
        original_content=content,
        target_model=target_model
    )
    
    return result.optimized_content
Multi-Stage Optimization Pipeline
For advanced optimization, we implement a multi-stage approach:
pythondef create_improved_optimizer(self, target_model):
    # First stage - analyze structure and format
    structure_analyzer = dspy.Predict(AnalyzeStructure)
    
    # Second stage - refine content with reasoning
    content_refiner = dspy.ChainOfThought(OptimizeContent)
    
    # Final stage - ensure format compliance
    format_validator = dspy.Predict(ValidateFormat)
    
    # Create pipeline
    optimizer = dspy.MultiStagePrompt(
        structure_analyzer,
        content_refiner,
        format_validator
    )
    
    return optimizer
Evaluation Framework
Our evaluation system leverages DSPy metrics and PromptFoo integration:
pythondef evaluate_optimization(self, original_content, optimized_content):
    evaluation_metrics = [
        dspy.metrics.RougeMetric(),
        self.custom_improvement_metric
    ]
    
    results = {}
    for metric in evaluation_metrics:
        score = metric(original_content, optimized_content)
        results[metric.__class__.__name__] = score
    
    return results
Resources

Official DSPy Documentation
DSPy GitHub Repository
Stanford DSPy Research Paper
DSPy Examples

Version Information
This documentation is based on DSPy v2.0.0, which is the version integrated in the Superstack Context Optimization System.

Note: This reference documentation focuses specifically on DSPy concepts relevant to our context optimization system. For comprehensive DSPy documentation, refer to the official resources.