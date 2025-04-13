"""
DSP Client for Context Module Optimization

This module provides an integration layer between DSPy and context modules,
handling the optimization process through DSPy's programming model.
"""

import os
import json
import yaml
import logging
from typing import Dict, Any, Optional, List, Tuple
import dspy

class DSPClient:
    """
    Client for interacting with DSPy to optimize context modules.
    Configures DSPy with appropriate models and optimization strategies.
    """
    
    def __init__(self, config_path: str = "config/dsp_config.yaml"):
        """
        Initialize the DSP client with the specified configuration.
        
        Args:
            config_path: Path to the DSP configuration file
        """
        self.logger = logging.getLogger(__name__)
        self.config = self._load_config(config_path)
        self._configure_dspy()
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load the DSP configuration from a YAML file.
        
        Args:
            config_path: Path to the configuration file
            
        Returns:
            Dict containing the configuration
        """
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                self.logger.info(f"Successfully loaded DSP configuration from {config_path}")
                return config
        except Exception as e:
            self.logger.error(f"Failed to load DSP configuration: {str(e)}")
            raise RuntimeError(f"Failed to load DSP configuration: {str(e)}")
    
    def _configure_dspy(self) -> None:
        """
        Configure DSPy with the models specified in the configuration.
        """
        try:
            for model_name, model_config in self.config['models'].items():
                self.logger.info(f"Configuring model: {model_name}")
                
                if model_config['api_type'] == 'openai':
                    lm = dspy.OpenAI(
                        model=model_config['model_name'],
                        max_tokens=model_config['max_tokens'],
                        temperature=model_config['temperature']
                    )
                elif model_config['api_type'] == 'anthropic':
                    lm = dspy.Anthropic(
                        model=model_config['model_name'],
                        max_tokens=model_config['max_tokens'],
                        temperature=model_config['temperature']
                    )
                else:
                    self.logger.warning(f"Unsupported API type: {model_config['api_type']}")
                    continue
                    
                # Register the language model with DSPy
                dspy.settings.configure(lm=lm)
                self.logger.info(f"Successfully configured DSPy with model {model_name}")
                
        except Exception as e:
            self.logger.error(f"Error configuring DSPy: {str(e)}")
            raise RuntimeError(f"Error configuring DSPy: {str(e)}")
    
    def get_strategy(self, strategy_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get optimization strategy configuration.
        
        Args:
            strategy_name: Name of the strategy to use, defaults to the default strategy
            
        Returns:
            Dictionary containing strategy configuration
        """
        if not strategy_name:
            strategy_name = self.config['dsp']['default_strategy']
            
        for strategy in self.config['dsp']['strategies']:
            if strategy['name'] == strategy_name:
                return strategy
                
        # If strategy not found, use default
        self.logger.warning(f"Strategy {strategy_name} not found, using default")
        default_strategy = self.config['dsp']['default_strategy']
        for strategy in self.config['dsp']['strategies']:
            if strategy['name'] == default_strategy:
                return strategy
                
        raise ValueError(f"Default strategy {default_strategy} not found in configuration")
    
    def _create_context_optimizer_module(self) -> dspy.Module:
        """
        Create a DSPy module for optimizing context content.
        
        Returns:
            A configured DSPy module
        """
        class ContextOptimizer(dspy.Module):
            """DSPy module for optimizing context module content"""
            
            def __init__(self):
                super().__init__()
                self.generate_optimized_content = dspy.ChainOfThought(
                    "original_content -> optimized_content"
                )
            
            def forward(self, original_content: str) -> Dict[str, str]:
                """
                Optimize the given context module content.
                
                Args:
                    original_content: The original content of the context module
                    
                Returns:
                    Dictionary with optimized content
                """
                result = self.generate_optimized_content(
                    original_content=original_content
                )
                return {"optimized_content": result.optimized_content}
        
        return ContextOptimizer()
    
    def _create_teleprompter(self, strategy: Dict[str, Any]) -> dspy.Teleprompter:
        """
        Create a DSPy Teleprompter for the optimization process.
        
        Args:
            strategy: The strategy configuration to use
            
        Returns:
            Configured Teleprompter
        """
        if strategy['name'] == "token_reduction":
            teleprompter = dspy.Teleprompter(
                instructions="""
                You are an AI context module optimizer. Your task is to optimize the given context 
                module content to use fewer tokens while preserving all important information.
                
                Follow these guidelines:
                1. Maintain all technical information and accuracy
                2. Eliminate redundancy and verbose explanations
                3. Use concise language and clear structure
                4. Preserve code examples and technical details
                5. Keep the same general structure and sections
                6. Do not add new information not present in the original
                
                Your output should be the optimized content only, not including any explanations 
                or comparisons to the original.
                """
            )
        elif strategy['name'] == "clarity_improvement":
            teleprompter = dspy.Teleprompter(
                instructions="""
                You are an AI context module optimizer. Your task is to improve the clarity and 
                structure of the given context module content while preserving all information.
                
                Follow these guidelines:
                1. Maintain all technical information and accuracy
                2. Improve organization with clear headings and structure
                3. Use consistent terminology and formatting
                4. Ensure code examples are clear and well-explained
                5. Simplify complex explanations without losing technical detail
                6. Do not add new information not present in the original
                
                Your output should be the optimized content only, not including any explanations 
                or comparisons to the original.
                """
            )
        else:
            # Default teleprompter
            teleprompter = dspy.Teleprompter(
                instructions="""
                You are an AI context module optimizer. Your task is to optimize the given context 
                module content while preserving all important information.
                
                Follow these guidelines:
                1. Maintain all technical information and accuracy
                2. Eliminate redundancy and verbose explanations
                3. Use concise language and clear structure
                4. Preserve code examples and technical details
                5. Keep the same general structure and sections
                6. Do not add new information not present in the original
                
                Your output should be the optimized content only, not including any explanations 
                or comparisons to the original.
                """
            )
            
        return teleprompter
        
    def optimize_module_content(
        self, 
        content: str, 
        model_name: Optional[str] = None,
        strategy_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Optimize a context module's content using DSPy.
        
        Args:
            content: The original content of the context module
            model_name: Name of the model to use, defaults to config default
            strategy_name: Name of the strategy to use, defaults to config default
            
        Returns:
            Dictionary containing optimization results
        """
        try:
            # Use default model if not specified
            if not model_name:
                model_name = self.config['general']['default_model']
                
            # Configure DSPy with the specified model
            model_config = self.config['models'].get(model_name)
            if not model_config:
                self.logger.warning(f"Model {model_name} not found, using default")
                model_name = self.config['general']['default_model']
                model_config = self.config['models'].get(model_name)
                
            if model_config['api_type'] == 'openai':
                lm = dspy.OpenAI(
                    model=model_config['model_name'],
                    max_tokens=model_config['max_tokens'],
                    temperature=model_config['temperature']
                )
            elif model_config['api_type'] == 'anthropic':
                lm = dspy.Anthropic(
                    model=model_config['model_name'],
                    max_tokens=model_config['max_tokens'],
                    temperature=model_config['temperature']
                )
            else:
                raise ValueError(f"Unsupported API type: {model_config['api_type']}")
                
            # Configure DSPy with the language model
            dspy.settings.configure(lm=lm)
            
            # Get optimization strategy
            strategy = self.get_strategy(strategy_name)
            
            # Create the optimizer module
            optimizer = self._create_context_optimizer_module()
            
            # Create the teleprompter for the strategy
            teleprompter = self._create_teleprompter(strategy)
            
            # Optimize the content
            self.logger.info(f"Optimizing module with model {model_name} and strategy {strategy['name']}")
            optimized = teleprompter(optimizer)(content)
            
            # Calculate token reduction
            original_tokens = len(content.split())
            optimized_tokens = len(optimized["optimized_content"].split())
            token_reduction = 1 - (optimized_tokens / original_tokens)
            
            return {
                "success": True,
                "original_content": content,
                "optimized_content": optimized["optimized_content"],
                "model": model_name,
                "strategy": strategy['name'],
                "token_stats": {
                    "original": original_tokens,
                    "optimized": optimized_tokens,
                    "reduction": token_reduction,
                    "reduction_percentage": f"{token_reduction * 100:.2f}%"
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error optimizing module content: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "original_content": content,
                "optimized_content": None,
                "model": model_name,
                "strategy": strategy_name
            }

# For testing/development
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Create DSP client
    client = DSPClient()
    
    # Test optimization
    test_content = """
    # Context Module: Example
    
    This is an example context module that provides information about a specific topic.
    
    ## Overview
    
    The module contains information that can be used to assist in understanding the topic.
    It may include technical details, code examples, and best practices.
    
    ## Technical Details
    
    Here are some technical details about the topic:
    
    - Point 1: Important information about aspect 1
    - Point 2: Important information about aspect 2
    - Point 3: Important information about aspect 3
    
    ## Code Examples
    
    ```python
    def example_function():
        # This function demonstrates the topic
        result = perform_operation()
        return result
    ```
    
    ## Best Practices
    
    When working with this topic, consider the following best practices:
    
    1. Always validate inputs
    2. Handle errors appropriately
    3. Document your code thoroughly
    
    ## References
    
    - Reference 1: [Link to reference 1](https://example.com/ref1)
    - Reference 2: [Link to reference 2](https://example.com/ref2)
    """
    
    result = client.optimize_module_content(test_content)
    
    if result["success"]:
        print("Optimization successful!")
        print(f"Token reduction: {result['token_stats']['reduction_percentage']}")
        print("\nOriginal content:")
        print(result["original_content"])
        print("\nOptimized content:")
        print(result["optimized_content"])
    else:
        print("Optimization failed!")
        print(f"Error: {result['error']}") 