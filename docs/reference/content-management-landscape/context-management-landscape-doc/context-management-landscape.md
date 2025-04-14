# Context Management and Structuring Strategies in LLM Systems

## Introduction

This research analysis explores the landscape of context management and structuring strategies in large language model (LLM) systems. Context management has emerged as a critical aspect of modern AI systems, directly impacting performance, accuracy, cost-efficiency, and user experience. As LLMs continue to evolve with larger context windows and more sophisticated reasoning capabilities, the approaches to authoring, storing, composing, and delivering context modules have similarly advanced.

This analysis aims to provide a comprehensive and practical knowledge framework to guide the design of future systems for modular, flexible, and efficient context management. Rather than prescribing a single solution, we explore alternative approaches and highlight the tradeoffs involved in various design decisions.

## 1. Conceptual Foundations

### What "Context" Means in LLM Architecture

In LLM systems, "context" refers to the input information provided to the model during inference that forms the basis for generating a response. This includes:

- **Prompt Instructions**: Guidance on how the LLM should respond, including its role, tone, format requirements, and constraints.
- **Background Knowledge**: Domain-specific information that may not be in the model's training data or requires emphasis.
- **Conversation History**: Previous exchanges between the user and the LLM that establish continuity.
- **External Data**: Information retrieved from knowledge bases, documents, or other sources to ground the model's responses.
- **User-Specific Information**: Personalization data or user preferences that shape responses.
- **System State**: Information about the current application state, available tools, or environmental factors.

Context acts as the "working memory" for the LLM, providing the information necessary to generate appropriate, accurate, and coherent responses to user queries.

### Why Managing Context is Important

Effective context management is crucial for several reasons:

1. **Response Quality**: The quality, accuracy, and relevance of LLM responses directly depend on the context provided. Better context leads to better outputs.

2. **Token Efficiency**: LLMs have finite context windows (token limits), making efficient use of this space critical for performance and cost management.

3. **Knowledge Integration**: Context management enables the integration of external, up-to-date information with the LLM's parametric knowledge.

4. **Hallucination Reduction**: Well-structured context grounds LLM responses in factual information, reducing fabrication and hallucination.

5. **Conversation Coherence**: Proper management of conversation history ensures consistent and coherent multi-turn interactions.

6. **Computational Efficiency**: Optimized context reduces unnecessary computation and improves response latency.

7. **Cost Control**: Most commercial LLM APIs charge based on token usage, making context optimization directly tied to operational costs.

### Tradeoffs with Large vs. Small Context Windows

The evolution of LLMs has seen a dramatic increase in context window sizes, from 2K tokens in early GPT-3 to 128K or more in recent models. However, this expansion introduces important tradeoffs:

**Large Context Windows (32K-128K+ tokens)**

*Advantages:*
- Can process entire documents without chunking
- Maintain full conversation history for complex interactions
- Reduce the need for complex retrieval mechanisms
- Better understanding of long-form content with cross-references
- Support for complex multi-step reasoning with all information available

*Disadvantages:*
- Higher computational costs and inference latency
- Greater token consumption leading to increased API costs
- Attention dilution across very large contexts (recency bias)
- Difficulty in prioritizing important information
- Challenges in maintaining focus on the most relevant parts
- Memory and computational resource limitations

**Small Context Windows (2K-8K tokens)**

*Advantages:*
- Lower computational costs and faster inference
- Forced prioritization of most important information
- Lower API costs due to reduced token consumption
- Simpler management of attention focus
- Better performance on hardware-constrained devices

*Disadvantages:*
- Requires sophisticated chunking and retrieval mechanisms
- Limited ability to maintain conversation history
- Difficulty handling complex, multi-step reasoning
- May miss important cross-document connections
- More complex context management infrastructure needed

**Key Insight:** Rather than simply defaulting to the largest available context window, systems should match context size to the task complexity and user needs, employing strategic context management regardless of the maximum window size.

## 2. Context Structuring Strategies

### Flat Document vs. Modular Files

**Flat Document Approach**

The flat document approach stores all context information in a single, consolidated file or data structure.

*Advantages:*
- Simplicity of maintenance and updates
- Easy to visualize the entire context
- No need for complex composition logic
- Reduced overhead in simple applications

*Disadvantages:*
- Limited reusability of content sections
- Difficult to prioritize or selectively include information
- Challenges in maintaining large documents
- Inefficiency when only portions are relevant

**Modular Files Approach**

The modular approach breaks context into smaller, purpose-specific files or components that can be dynamically composed.

*Advantages:*
- Reusability across different use cases
- Easier maintenance and updates of specific modules
- Selective inclusion based on relevance
- Better organization of domain knowledge
- Support for collaborative authoring
- Dynamic composition based on query needs

*Disadvantages:*
- Increased complexity in management
- Overhead of composition systems
- Potential for inconsistencies between modules
- More sophisticated retrieval requirements

**Hybrid Approaches**

Many mature systems adopt hybrid approaches:

- **Hierarchical Modularity**: Organizing modules in a hierarchy with different levels of granularity
- **Template-Based Systems**: Using templates with slots for dynamic content insertion
- **Domain-Specific Collections**: Grouping related modules into collection files while maintaining internal modularity

### Prioritization Techniques

Successful context management requires effective prioritization strategies:

**Token Budget Allocation**

Dividing the available context window into allocated "budgets" for different types of content:

```python
class ContextBudget:
    def __init__(self, total_tokens=8000):
        self.total_tokens = total_tokens
        self.allocations = {
            "system_instructions": 0.15,  # 15% for instructions
            "conversation_history": 0.30,  # 30% for conversation
            "retrieved_knowledge": 0.45,  # 45% for knowledge
            "user_query": 0.10,           # 10% for current query
        }
        
    def get_budget(self, category):
        """Return token budget for a category"""
        return int(self.total_tokens * self.allocations[category])
        
    def adjust_dynamically(self, query_complexity):
        """Adjust allocations based on query complexity"""
        if query_complexity == "high":
            self.allocations["retrieved_knowledge"] = 0.55
            self.allocations["conversation_history"] = 0.20
        elif query_complexity == "low":
            self.allocations["retrieved_knowledge"] = 0.35
            self.allocations["conversation_history"] = 0.40
```

**Priority Levels**

Assigning explicit priority levels to context components, as seen in the Model Context Protocol (MCP):

```
<context name="system_instructions" priority="high">
You are a helpful assistant specialized in financial analysis.
</context>

<context name="user_query" priority="high">
What was the GDP growth rate in Q1 2025?
</context>

<context name="retrieved_data" priority="medium">
According to official reports, Q1 2025 GDP growth was 2.7%.
</context>

<context name="conversation_history" priority="low">
User: Do you have the latest economic figures?
Assistant: Yes, I can provide recent economic indicators. What specific data are you looking for?
</context>
```

**Recency Weighting**

Prioritizing more recent information, especially in conversation history:

- **Sliding Window**: Keeping only the most recent N turns of conversation
- **Hierarchical Summarization**: Summarizing older turns while keeping recent ones verbatim
- **Decay Functions**: Applying a decay function to reduce the inclusion probability of older content

**Attention-Based Prioritization**

Structuring context to work with, rather than against, the attention mechanisms of LLMs:

- **Position-Based Importance**: Placing critical information near the query or at the beginning
- **Explicit Markers**: Using formatting, headers, or special tokens to direct attention
- **Repetition of Key Points**: Strategic repetition of critical information

### Chunking, Summarization, and Retrieval Strategies

**Chunking Strategies**

Breaking large documents into manageable pieces is crucial for effective retrieval:

1. **Fixed-Size Chunking**: Dividing documents into chunks of consistent token size
   - Simple but may break semantic units

2. **Semantic Chunking**: Respecting natural document boundaries
   - Preserving paragraphs, sections, or semantic units
   - Variable chunk sizes but more meaningful content

3. **Overlapping Chunks**: Including overlap between adjacent chunks
   - Prevents information loss at chunk boundaries
   - Typically 10-20% overlap between chunks

4. **Hierarchical Chunking**: Creating chunks at multiple granularity levels
   - Document-level summary
   - Section-level chunks
   - Paragraph-level details

5. **Late Chunking**: Processing the full document with a long-context embedding model before chunking
   - Preserves broader document context in the embeddings
   - Enables more contextually aware retrieval

6. **Recursive Chunking**: Dynamic chunk size determination based on content complexity
   ```python
   def recursive_chunk(document, max_size=1000, min_size=100):
       if len(tokenize(document)) <= max_size:
           return [document]
       
       # Find natural boundaries to split
       sections = split_by_headers(document)
       
       chunks = []
       for section in sections:
           if len(tokenize(section)) <= max_size:
               chunks.append(section)
           else:
               # Recursively split large sections
               paragraphs = split_by_paragraphs(section)
               for para in paragraphs:
                   if len(tokenize(para)) <= max_size:
                       chunks.append(para)
                   elif len(tokenize(para)) > min_size:
                       # Split very large paragraphs by sentences
                       chunks.extend(split_by_sentences(para, max_size))
                   else:
                       chunks.append(para)
       
       return chunks
   ```

**Summarization Approaches**

Summarization reduces context size while preserving key information:

1. **Extractive Summarization**: Selecting the most important sentences or passages
   - Faster and more factually accurate
   - Less coherent than abstractive approaches

2. **Abstractive Summarization**: Generating new text that captures the essence
   - More coherent but risk of hallucination
   - Better for conversation history

3. **Hierarchical Summarization**: Creating summaries at different levels of detail
   - High-level overview for general context
   - Detailed summaries for relevant sections

4. **Query-Focused Summarization**: Generating summaries relevant to a specific query
   - More effective for RAG systems
   - Reduces irrelevant information

5. **Progressive Summarization**: Incrementally condensing information over time
   - Useful for long-running conversations
   - Preserves key points while reducing token usage

**Retrieval Mechanisms**

Effective retrieval selects the most relevant context for a given query:

1. **Vector Similarity Search**: Using embeddings to find semantically relevant content
   - Cosine similarity or other distance metrics
   - Benefits from domain-adapted embedding models

2. **Hybrid Search**: Combining vector search with keyword or BM25 approaches
   - Better handling of technical terms and rare words
   - More robust across different query types

3. **Multi-Stage Retrieval**: Using a cascading approach to refine results
   - Initial broad retrieval followed by reranking
   - More computationally intensive but higher precision

4. **Query Expansion**: Enhancing queries to improve retrieval quality
   - Adding synonyms or related concepts
   - Decomposing complex queries into sub-queries

5. **Contextual Retrieval**: Using previous context to inform retrieval
   - Incorporating conversation history in retrieval queries
   - Maintaining topical consistency

### Composability and Context Orchestration

**Composition Patterns**

Approaches to dynamically assembling context from modules:

1. **Template-Based Composition**: Using templates with placeholders for dynamic content
   ```python
   template = """
   <context name="system" priority="high">
   {system_instructions}
   </context>
   
   <context name="user_query" priority="high">
   {query}
   </context>
   
   <context name="knowledge" priority="medium">
   {retrieved_knowledge}
   </context>
   
   <context name="history" priority="low">
   {conversation_history}
   </context>
   """
   
   context = template.format(
       system_instructions=get_system_instructions(),
       query=user_query,
       retrieved_knowledge=retrieve_relevant_knowledge(user_query),
       conversation_history=get_conversation_history()
   )
   ```

2. **Rule-Based Assembly**: Using rules to determine which modules to include
   - IF-THEN rules based on query type, user preferences, etc.
   - Decision trees for context selection

3. **Dynamic Scoring**: Assigning relevance scores to modules and selecting top-scoring ones
   - Similar to retrieval but with predefined modules
   - Can incorporate user feedback over time

4. **Graph-Based Composition**: Representing context modules as a knowledge graph
   - Traversing the graph based on query needs
   - Capturing relationships between information pieces

5. **Agent-Driven Composition**: Using an LLM-based agent to determine context needs
   - Meta-prompting to analyze what context is needed
   - More adaptive but adds latency and complexity

**Orchestration Systems**

Systems that manage the end-to-end context lifecycle:

1. **Pipeline Orchestrators**: Managing the flow from query to context to response
   - LangChain, LlamaIndex, Semantic Kernel
   - Sequential processing with hooks for customization

2. **Context Managers**: Dedicated components for context handling
   - Token accounting and budgeting
   - Module selection and composition
   - Caching and persistence

3. **Feedback Loops**: Systems that learn from interaction outcomes
   - Tracking which context components led to good responses
   - Iterative refinement of context strategy

4. **Hybrid Human-AI Orchestration**: Systems with human-in-the-loop components
   - Human review and editing of critical context
   - Escalation paths for uncertain context needs

## 3. Best Practices and Implementation Patterns

### File Organization Models

**Topic-Based Organization**

Organizing context files around specific topics or domains:

```
/context
  /financial_analysis
    financial_terms.md
    market_indicators.md
    economic_concepts.md
  /customer_support
    common_issues.md
    troubleshooting_steps.md
    product_features.md
  /programming
    python_concepts.md
    javascript_patterns.md
    git_workflows.md
```

*Best for:* Domain-specific applications with clear topic boundaries

**Functional Organization**

Organizing by the function each context serves in the system:

```
/context
  /system_instructions
    general_assistant.md
    expert_financial.md
    customer_support.md
  /domain_knowledge
    finance.md
    technology.md
    healthcare.md
  /examples
    financial_analysis_examples.md
    code_examples.md
    query_response_pairs.md
```

*Best for:* Multi-purpose assistants with different operational modes

**Granularity-Based Organization**

Organizing by the level of detail or specificity:

```
/context
  /high_level
    domain_overviews.md
    concept_definitions.md
  /detailed
    specific_procedures.md
    technical_details.md
  /examples
    case_studies.md
    step_by_step_guides.md
```

*Best for:* Systems that need to adjust detail level based on query complexity

**User-Centric Organization**

Organizing around user types or personas:

```
/context
  /beginner_users
    basic_concepts.md
    getting_started.md
  /advanced_users
    technical_details.md
    advanced_features.md
  /administrator
    system_management.md
    troubleshooting.md
```

*Best for:* Applications serving different user segments with varying expertise

### Metadata and Tagging Systems

Effective metadata enhances context management and retrieval:

**Core Metadata Fields**

- **Title**: Descriptive name of the context module
- **Description**: Brief summary of the content
- **Category/Tags**: Topic classifications for organization
- **Priority**: Importance level (high/medium/low)
- **Last Updated**: Timestamp for freshness assessment
- **Author**: Creator or maintainer
- **Version**: Version number for tracking changes
- **Dependencies**: Related context modules
- **Token Count**: Pre-computed token size for budgeting
- **Usage Scope**: When this context should be used

**Tagging Strategies**

1. **Hierarchical Tags**: Using parent-child relationships
   - `programming:python:data-science`
   - Enables both broad and specific retrieval

2. **Faceted Classification**: Multi-dimensional categorization
   - Domain: `finance`
   - Complexity: `advanced`
   - Content type: `procedure`

3. **Semantic Tagging**: Using embedding-based topic modeling
   - Automatically generated tags based on content
   - Reduces manual tagging burden

4. **Usage-Based Tagging**: Tracking how modules are actually used
   - Most frequently retrieved for which query types
   - Success rate when included in context

**Metadata Implementation Example**

```yaml
---
title: "Python Exception Handling"
description: "Guide to handling exceptions in Python with examples"
category: "programming/python"
tags: ["error-handling", "try-except", "best-practices"]
priority: "medium"
last_updated: "2025-03-15"
author: "dev-team"
version: "1.2"
dependencies: ["python-basics", "functions-guide"]
token_count: 1250
usage_scope: "python-related queries, error troubleshooting"
embedding_vector: "base64-encoded-vector-here"
---

# Python Exception Handling

Exception handling in Python allows you to gracefully manage errors...
```

### Examples of Dynamic Composition Systems

**LangChain Implementation**

LangChain provides components for building context-aware applications:

```python
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.retrievers import VectorStoreRetriever
from langchain.schema.runnable import RunnablePassthrough
from langchain.memory import ConversationBufferMemory

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4")

# Create a retriever
retriever = VectorStoreRetriever(vector_store=vector_store)

# Set up conversation memory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# Create a context-aware prompt template
prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant with expertise in {topic}.

Chat History:
{chat_history}

Relevant Information:
{retrieved_docs}

User Question: {question}

Please provide a helpful answer based on the provided information.
""")

# Create a chain that composes context dynamically
context_chain = (
    {
        "topic": lambda x: x["topic"],
        "question": lambda x: x["question"],
        "chat_history": lambda x: memory.load_memory_variables(x)["chat_history"],
        "retrieved_docs": lambda x: retriever.get_relevant_documents(x["question"])
    }
    | prompt
    | llm
)

# Use the chain
response = context_chain.invoke({
    "topic": "python programming",
    "question": "How do I handle file I/O exceptions?"
})

# Update memory
memory.save_context(
    {"input": "How do I handle file I/O exceptions?"},
    {"output": response.content}
)
```

**LlamaIndex Implementation**

LlamaIndex specializes in knowledge integration and retrieval:

```python
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import MetadataMode
from llama_index.core import PromptTemplate
from llama_index.llms.openai import OpenAI

# Initialize the LLM
Settings.llm = OpenAI(model="gpt-4")

# Load and parse documents
documents = SimpleDirectoryReader("./data").load_data()
parser = SentenceSplitter(chunk_size=1024, chunk_overlap=100)
nodes = parser.get_nodes_from_documents(documents)

# Create a vector index
index = VectorStoreIndex(nodes)

# Custom query template with structured context
custom_prompt = PromptTemplate("""
<context name="system_instructions" priority="high">
You are a knowledge assistant answering questions based on the provided information.
If information is not available, acknowledge this rather than speculating.
</context>

<context name="relevant_information" priority="medium">
{context_str}
</context>

<context name="user_query" priority="high">
{query_str}
</context>
""")

# Create query engine with custom prompt
query_engine = index.as_query_engine(
    text_qa_template=custom_prompt,
    similarity_top_k=5
)

# Execute query with dynamic context composition
response = query_engine.query("How does Python handle file permissions?")
```

**RAG Pipeline Implementation**

A custom implementation focusing on context management:

```python
class ContextManager:
    def __init__(self, max_tokens=8000):
        self.max_tokens = max_tokens
        self.embedding_model = SentenceTransformerEmbeddings()
        self.tokenizer = Tokenizer()
        self.vector_store = VectorStore()
        
    def create_context(self, query, conversation_history=None):
        """Dynamically compose context for a query"""
        # Allocate token budget
        budget = self._allocate_budget(query, conversation_history)
        
        # Retrieve relevant knowledge
        retrieved_docs = self._retrieve_knowledge(
            query, 
            max_tokens=budget["knowledge"]
        )
        
        # Process conversation history
        if conversation_history:
            history = self._process_history(
                conversation_history,
                max_tokens=budget["history"]
            )
        else:
            history = ""
        
        # Select appropriate system instructions
        instructions = self._select_instructions(query)
        
        # Compose final context
        context = f"""
<context name="system_instructions" priority="high">
{instructions}
</context>

<context name="user_query" priority="high">
{query}
</context>

<context name="relevant_knowledge" priority="medium">
{retrieved_docs}
</context>
"""

        if history:
            context += f"""
<context name="conversation_history" priority="low">
{history}
</context>
"""
        
        return context
    
    def _allocate_budget(self, query, conversation_history):
        """Allocate token budget based on query complexity"""
        # Calculate query complexity
        complexity = self._assess_complexity(query)
        
        # Adjust allocation based on complexity and history
        if complexity == "high":
            return {
                "instructions": int(self.max_tokens * 0.10),
                "knowledge": int(self.max_tokens * 0.60),
                "history": int(self.max_tokens * 0.20),
                "query": int(self.max_tokens * 0.10)
            }
        elif complexity == "medium":
            return {
                "instructions": int(self.max_tokens * 0.15),
                "knowledge": int(self.max_tokens * 0.45),
                "history": int(self.max_tokens * 0.30),
                "query": int(self.max_tokens * 0.10)
            }
        else:
            return {
                "instructions": int(self.max_tokens * 0.15),
                "knowledge": int(self.max_tokens * 0.30),
                "history": int(self.max_tokens * 0.45),
                "query": int(self.max_tokens * 0.10)
            }
    
    def _retrieve_knowledge(self, query, max_tokens):
        """Retrieve relevant knowledge within token budget"""
        # Generate query embedding
        query_embedding = self.embedding_model.embed(query)
        
        # Get relevant documents
        docs = self.vector_store.similarity_search(
            query_embedding,
            k=10  # Get more than needed to allow filtering
        )
        
        # Select documents within token budget
        selected_docs = []
        current_tokens = 0
        
        for doc in docs:
            doc_tokens = self.tokenizer.count_tokens(doc.text)
            if current_tokens + doc_tokens <= max_tokens:
                selected_docs.append(doc.text)
                current_tokens += doc_tokens
            else:
                break
        
        return "\n\n".join(selected_docs)
    
    def _process_history(self, history, max_tokens):
        """Process conversation history to fit token budget"""
        # If history is short enough, use as is
        total_tokens = self.tokenizer.count_tokens(history)
        if total_tokens <= max_tokens:
            return history
        
        # Otherwise, use sliding window + summarization
        turns = history.split("\n\n")
        
        if len(turns) <= 4:
            # Keep only last few turns if not many
            recent_turns = turns[-4:]
            return "\n\n".join(recent_turns)
        else:
            # Summarize older turns, keep recent ones verbatim
            older_turns = turns[:-4]
            recent_turns = turns[-4:]
            
            older_summary = self._summarize("\n\n".join(older_turns))
            
            processed_history = f"Previous conversation summary: {older_summary}\n\n"
            processed_history += "\n\n".join(recent_turns)
            
            return processed_history
    
    def _select_instructions(self, query):
        """Select appropriate system instructions based on query"""
        # Identify query intent
        if "code" in query.lower() or "programming" in query.lower():
            return self._load_module("instructions/programming_assistant.md")
        elif "data" in query.lower() or "analysis" in query.lower():
            return self._load_module("instructions/data_analyst.md")
        else:
            return self._load_module("instructions/general_assistant.md")
    
    def _assess_complexity(self, query):
        """Assess query complexity for budget allocation"""
        tokens = self.tokenizer.count_tokens(query)
        has_technical_terms = any(term in query.lower() for term in [
            "how", "why", "explain", "compare", "analyze", "difference"
        ])
        
        if tokens > 30 and has_technical_terms:
            return "high"
        elif tokens > 15 or has_technical_terms:
            return "medium"
        else:
            return "low"
    
    def _load_module(self, path):
        """Load a context module from file"""
        with open(path, "r") as f:
            return f.read()
    
    def _summarize(self, text):
        """Summarize text to reduce tokens"""
        # In a real implementation, would use an LLM or specialized summarizer
        return f"[Summary of conversation with {len(text.split())} words]"
```

### Embedding-Based Selection vs. Rule-Based Logic

**Embedding-Based Selection**

Using vector embeddings to select relevant context:

*Advantages:*
- Captures semantic relationships beyond keyword matching
- Better handles varied phrasing and synonyms
- More adaptable to novel queries
- Scales well with large context libraries

*Disadvantages:*
- Computationally more expensive
- May miss exact matches that are semantically unusual
- Difficult to predict or debug selection logic
- Quality depends on embedding model quality

**Rule-Based Logic**

Using explicit rules to determine context inclusion:

*Advantages:*
- Predictable and transparent selection logic
- Better handling of critical information that must always be included
- Can enforce business rules and compliance requirements
- Less computational overhead
- Easier to debug and test

*Disadvantages:*
- Less flexible for novel or unexpected queries
- Requires manual rule creation and maintenance
- Difficult to scale with growing context libraries
- May miss semantic connections

**Hybrid Approaches**

Most sophisticated systems combine both approaches:

1. **Rule-First, Embedding-Second**: Apply rules for critical context, then use embeddings for additional relevant content
2. **Embedding-First, Rule-Filter**: Use embeddings for initial selection, then apply rules to filter or prioritize results
3. **Parallel Processing**: Use both methods independently and combine results with weighting
4. **Staged Selection**: Use rules for high-level module selection, embeddings for fine-grained content within modules

Example hybrid implementation:

```python
def select_context(query, context_modules, embedding_model):
    """Select context using hybrid approach"""
    # 1. Rule-based selection of required modules
    required_modules = []
    
    # Always include system instructions
    required_modules.append("system_instructions")
    
    # Include compliance information for financial queries
    if any(term in query.lower() for term in ["finance", "invest", "money", "portfolio"]):
        required_modules.append("compliance_information")
    
    # Include safety guidelines for health queries
    if any(term in query.lower() for term in ["health", "medical", "disease", "symptom"]):
        required_modules.append("medical_disclaimer")
    
    # 2. Embedding-based selection for domain knowledge
    query_embedding = embedding_model.embed(query)
    
    # Filter to knowledge modules only
    knowledge_modules = [m for m in context_modules if m.category == "knowledge"]
    
    # Calculate relevance scores
    scored_modules = []
    for module in knowledge_modules:
        if not hasattr(module, 'embedding'):
            module.embedding = embedding_model.embed(module.content)
        
        similarity = cosine_similarity(query_embedding, module.embedding)
        scored_modules.append((module, similarity))
    
    # Select top-k most relevant knowledge modules
    top_modules = sorted(scored_modules, key=lambda x: x[1], reverse=True)[:5]
    
    # 3. Combine selections with token budget enforcement
    selected_modules = []
    current_tokens = 0
    max_tokens = 7000  # Leave room for query and response
    
    # Add required modules first
    for module_name in required_modules:
        module = next((m for m in context_modules if m.name == module_name), None)
        if module:
            token_count = len(module.content.split())  # Simplified token counting
            if current_tokens + token_count <= max_tokens:
                selected_modules.append(module)
                current_tokens += token_count
    
    # Add knowledge modules with remaining budget
    for module, score in top_modules:
        token_count = len(module.content.split())
        if current_tokens + token_count <= max_tokens:
            selected_modules.append(module)
            current_tokens += token_count
    
    return selected_modules
```

## 4. Tradeoffs and Design Considerations

### Performance vs. Flexibility

One of the most fundamental tradeoffs in context management is between performance and flexibility:

**Performance-Optimized Approach**

*Characteristics:*
- Predefined context templates
- Minimal dynamic composition
- Optimized retrieval indexes
- Caching of common contexts
- Streamlined processing pipeline

*Advantages:*
- Lower latency
- Reduced computational overhead
- More predictable response times
- Lower operational costs

*Disadvantages:*
- Less adaptable to novel queries
- Limited personalization
- May include irrelevant information
- Requires precomputing for optimization

**Flexibility-Optimized Approach**

*Characteristics:*
- Highly dynamic context composition
- Fine-grained modularity
- Query-time optimization
- Multiple retrieval mechanisms
- Adaptive processing

*Advantages:*
- Better adaptation to diverse queries
- More precise context selection
- Greater personalization potential
- Easier to extend with new content

*Disadvantages:*
- Higher latency
- Increased computational costs
- More complex architecture
- Unpredictable performance

**Finding the Balance**

Most systems need to find a middle ground based on their specific requirements:

1. **Tiered Approach**: Using simpler, performance-optimized processing for common queries, with fallback to more flexible methods for complex or novel queries

2. **Pre-computation with Dynamic Supplementation**: Pre-computing common context components while dynamically adding specialized content at query time

3. **Adaptive Complexity**: Adjusting the sophistication of context management based on query complexity and user needs

4. **Caching Strategies**: Caching context compositions for similar queries while maintaining flexibility for new ones

### Reusability vs. Specificity

Another key tradeoff involves balancing reusability of context modules against their specificity:

**Highly Reusable Modules**

*Characteristics:*
- Generic, broadly applicable content
- Minimal dependencies on other modules
- Abstract concepts and principles
- Limited domain-specific terminology

*Advantages:*
- Used across many different queries
- Easier to maintain and update
- More efficient content management
- Better resource utilization

*Disadvantages:*
- May lack precision for specific queries
- Often require supplementation
- Potential for irrelevance in specific cases
- Risk of being too generic to be useful

**Highly Specific Modules**

*Characteristics:*
- Narrowly focused content
- Domain-specific information
- Detailed explanations and examples
- Targeted use cases

*Advantages:*
- Precise, highly relevant information
- Better quality for specific queries
- More comprehensive coverage of topics
- Often contain unique information

*Disadvantages:*
- Limited reuse potential
- Higher maintenance burden
- More storage and management overhead
- Risk of content duplication

**Balancing Approaches**

Effective systems typically employ a spectrum of module types:

1. **Layered Specificity**: Creating modules at different levels of specificity, from general to highly specific

2. **Composable Components**: Designing modules to work together, with general modules providing foundations and specific ones adding detail

3. **Dynamic Specificity**: Generating query-specific context by combining and transforming more general modules

4. **Hierarchical Organization**: Organizing modules in a hierarchy from general to specific, enabling navigation to the appropriate level

### Manual Curation vs. Automated Generation

The approach to creating and maintaining context modules presents another significant tradeoff:

**Manual Curation**

*Characteristics:*
- Human-authored context modules
- Editorial review processes
- Explicit organization and tagging
- Deliberate design decisions

*Advantages:*
- Higher quality and accuracy
- Better handling of nuanced information
- More consistent tone and style
- Explicit consideration of ethical and safety concerns
- Fine-grained control over content

*Disadvantages:*
- Time-consuming to create and maintain
- Doesn't scale well for large knowledge bases
- May lag behind rapidly changing information
- Subject to human biases and oversights
- Higher operational costs

**Automated Generation**

*Characteristics:*
- LLM-generated or extracted context
- Automated organization and tagging
- Algorithmic knowledge extraction
- Continuous updating processes

*Advantages:*
- Scales to cover vast knowledge domains
- Faster creation and updating
- Can process and integrate large volumes of information
- Adapts quickly to new information
- Lower operational costs

*Disadvantages:*
- Quality and accuracy concerns
- Risk of propagating errors or hallucinations
- Less control over content
- Potential for unexpected biases
- Difficulty with highly specialized knowledge

**Hybrid Approaches**

Most effective systems use hybrid approaches:

1. **Human-in-the-Loop**: Automated generation with human review for critical modules

2. **Tiered Verification**: Different levels of human oversight based on content importance and risk

3. **Automated Draft, Manual Finalization**: Using automation to create initial drafts that humans refine

4. **Dynamic vs. Static Split**: Manually curating core, stable knowledge while automating more dynamic or peripheral content

5. **Continuous Improvement Cycle**: Using automation with feedback loops where human review improves generation quality over time

```python
class ContextModuleManager:
    def __init__(self, llm_client, human_review_queue=None):
        self.llm_client = llm_client
        self.human_review_queue = human_review_queue
        self.modules_db = ModulesDatabase()
    
    def generate_or_update_module(self, topic, existing_module=None, require_review=False):
        """Generate or update a context module"""
        # Determine if this is high-risk content
        is_high_risk = self._assess_risk(topic)
        
        if existing_module:
            # Update existing module
            updated_content = self._generate_update(existing_module, topic)
            change_magnitude = self._assess_change_magnitude(
                existing_module.content, updated_content
            )
            
            # Determine if human review is needed
            needs_review = (
                is_high_risk or 
                change_magnitude > 0.3 or 
                require_review
            )
        else:
            # Generate new module
            metadata = self._generate_metadata(topic)
            content = self._generate_content(topic, metadata)
            updated_content = content
            
            # New modules for high-risk topics always need review
            needs_review = is_high_risk or require_review
        
        # Handle review process
        if needs_review and self.human_review_queue:
            # Send for human review
            review_id = self.human_review_queue.add_item({
                "topic": topic,
                "original": existing_module.content if existing_module else None,
                "generated": updated_content,
                "is_update": existing_module is not None,
                "risk_level": "high" if is_high_risk else "normal"
            })
            return {"status": "pending_review", "review_id": review_id}
        else:
            # Auto-approve and store
            module_id = self._store_module(topic, updated_content, existing_module)
            return {"status": "approved", "module_id": module_id}
    
    def _assess_risk(self, topic):
        """Assess if a topic is high-risk requiring human review"""
        high_risk_categories = [
            "medical", "legal", "financial", "safety", "security",
            "political", "controversial", "ethics"
        ]
        
        return any(category in topic.lower() for category in high_risk_categories)
    
    def _generate_update(self, existing_module, topic):
        """Generate updated content based on existing module"""
        prompt = f"""
        You are updating a context module on the topic of "{topic}".
        
        Here is the existing content:
        ---
        {existing_module.content}
        ---
        
        Please update this content to:
        1. Add any new or updated information
        2. Correct any outdated information
        3. Improve clarity and organization if needed
        4. Maintain the same general structure and purpose
        
        Return the complete updated module content.
        """
        
        response = self.llm_client.generate(prompt)
        return response.text
    
    def _assess_change_magnitude(self, original, updated):
        """Calculate how significant the changes are (0-1 scale)"""
        # Simple implementation using difflib
        import difflib
        
        matcher = difflib.SequenceMatcher(None, original, updated)
        return 1 - matcher.ratio()  # Higher number = more changes
    
    def _generate_metadata(self, topic):
        """Generate appropriate metadata for a new module"""
        prompt = f"""
        Create appropriate metadata for a context module on "{topic}".
        Include tags, categories, priority level, and usage scope.
        Format the response as a JSON object.
        """
        
        response = self.llm_client.generate(prompt)
        import json
        return json.loads(response.text)
    
    def _generate_content(self, topic, metadata):
        """Generate content for a new module"""
        prompt = f"""
        Create a comprehensive context module on the topic of "{topic}".
        
        This module will be used to provide context to an LLM system.
        
        The module should include:
        1. Clear definitions and explanations
        2. Key concepts and principles
        3. Practical examples where appropriate
        4. Common usage patterns
        5. Important considerations or limitations
        
        Metadata: {metadata}
        
        Format the content using Markdown with clear section headers.
        """
        
        response = self.llm_client.generate(prompt)
        return response.text
    
    def _store_module(self, topic, content, existing_module=None):
        """Store a new or updated module in the database"""
        if existing_module:
            module_id = existing_module.id
            self.modules_db.update_module(module_id, content)
        else:
            module_id = self.modules_db.create_module(topic, content)
        
        return module_id
```

## 5. Anti-Patterns and Common Pitfalls

Identifying and avoiding common mistakes in context management is crucial for building effective systems:

### Monolithic Context Blocks with No Prioritization

**Anti-Pattern:** Creating large, undifferentiated context blocks without any prioritization or structure.

**Example:**
```python
# ❌ Poor context management with monolithic block
def generate_response(query, knowledge_base, conversation_history):
    # Dump everything into one big context block
    context = f"""
    System: You are a helpful assistant.
    
    Knowledge:
    {knowledge_base}
    
    Conversation:
    {conversation_history}
    
    User: {query}
    """
    
    return llm.generate(context)
```

**Why It Fails:**
- The LLM has no way to determine what information is most important
- Wastes tokens on potentially irrelevant information
- No accommodation for token limits
- Doesn't account for attention mechanisms in LLMs
- Often leads to ignored information, especially in the middle

**Better Approach:**
```python
def generate_response(query, knowledge_base, conversation_history):
    # Retrieve only relevant knowledge
    relevant_knowledge = retrieve_relevant_knowledge(query, knowledge_base)
    
    # Structure conversation history
    if len(conversation_history) > 5:
        recent_history = conversation_history[-5:]
        older_history = summarize_history(conversation_history[:-5])
        processed_history = f"Previous conversation summary: {older_history}\n\n" + recent_history
    else:
        processed_history = conversation_history
    
    # Create structured, prioritized context
    context = f"""
    <context name="system_instructions" priority="high">
    You are a helpful assistant. Provide accurate information based on the knowledge provided.
    </context>
    
    <context name="user_query" priority="high">
    {query}
    </context>
    
    <context name="relevant_knowledge" priority="medium">
    {relevant_knowledge}
    </context>
    
    <context name="conversation_history" priority="low">
    {processed_history}
    </context>
    """
    
    return llm.generate(context)
```

### Redundant or Low-Value Context Inclusion

**Anti-Pattern:** Including redundant, obvious, or low-value information that wastes tokens without improving responses.

**Example:**
```python
# ❌ Including obvious or redundant information
context = f"""
You are an AI assistant created by OpenAI. You run on a large language model
called GPT-4. You were trained on data up until 2023. You can't browse the 
internet. You can't access real-time information. You can only provide
information based on your training data.

Remember to be helpful, harmless, and honest. Always be polite and respectful.
Don't provide harmful, illegal, unethical or deceptive information.
Don't generate content like jokes, poems, stories, code, or essays unless asked.

The current date is {current_date}. The user's name is {user_name}.
The user's timezone is {timezone}. The user is located in {location}.
The user's device is {device}. The user's browser is {browser}.
The user's operating system is {os}.

{long_standard_disclaimer}

Now, please answer the following question: {query}
"""
```

**Why It Fails:**
- Wastes tokens on information the model already knows (e.g., that it's an AI)
- Includes irrelevant user details (browser, OS) for most queries
- Redundantly states standard limitations
- Pushes more relevant information further from the query
- Reduces available tokens for actually useful context

**Better Approach:**
```python
def create_efficient_context(query, user_data):
    # Only include user-specific data that's relevant to the query
    relevant_user_info = extract_relevant_user_info(query, user_data)
    
    # Construct minimal but effective context
    context = f"""
    <context name="system_instructions" priority="high">
    You are a helpful assistant. Provide accurate, concise answers.
    Today is {current_date}.
    </context>
    """
    
    # Only add personal context if relevant
    if relevant_user_info:
        context += f"""
        <context name="user_information" priority="medium">
        {relevant_user_info}
        </context>
        """
    
    # Add the query
    context += f"""
    <context name="user_query" priority="high">
    {query}
    </context>
    """
    
    return context
```

### Uncontrolled Token Growth

**Anti-Pattern:** Allowing context size to grow unchecked, especially in ongoing conversations, until it exceeds token limits.

**Example:**
```python
# ❌ Uncontrolled token growth in conversation
class SimpleConversationManager:
    def __init__(self):
        self.conversation_history = ""
    
    def add_exchange(self, user_query, assistant_response):
        # Simply append each new exchange to history
        self.conversation_history += f"\nUser: {user_query}\nAssistant: {assistant_response}\n"
    
    def generate_response(self, query):
        # Use entire history without management
        context = f"""
        Conversation history:
        {self.conversation_history}
        
        Current query: {query}
        """
        
        # Will eventually exceed token limits
        response = llm.generate(context)
        self.add_exchange(query, response)
        return response
```

**Why It Fails:**
- Eventually exceeds model token limits
- Includes irrelevant historical exchanges
- Wastes tokens on old information
- Gives equal weight to all history
- Fails catastrophically rather than gracefully

**Better Approach:**
```python
class TokenAwareConversationManager:
    def __init__(self, max_history_tokens=4000):
        self.conversation_history = []
        self.max_history_tokens = max_history_tokens
        self.tokenizer = Tokenizer()
    
    def add_exchange(self, user_query, assistant_response):
        # Add new exchange as a discrete entry
        self.conversation_history.append({
            "user": user_query,
            "assistant": assistant_response,
            "tokens": self.tokenizer.count_tokens(f"User: {user_query}\nAssistant: {assistant_response}")
        })
        
        # Manage token budget
        self._enforce_token_limit()
    
    def _enforce_token_limit(self):
        """Ensure history stays within token budget"""
        current_total = sum(exchange["tokens"] for exchange in self.conversation_history)
        
        # If we're over budget, use sliding window with summarization
        if current_total > self.max_history_tokens:
            # Keep most recent exchanges intact
            keep_last_n = 3
            recent_exchanges = self.conversation_history[-keep_last_n:]
            recent_tokens = sum(exchange["tokens"] for exchange in recent_exchanges)
            
            # Summarize older exchanges to fit remaining budget
            remaining_budget = self.max_history_tokens - recent_tokens
            older_exchanges = self.conversation_history[:-keep_last_n]
            
            if remaining_budget > 500 and older_exchanges:  # Only summarize if enough budget and history
                older_text = "\n".join([
                    f"User: {ex['user']}\nAssistant: {ex['assistant']}" 
                    for ex in older_exchanges
                ])
                
                summary = self._summarize_history(older_text)
                summary_tokens = self.tokenizer.count_tokens(summary)
                
                # Replace older history with summary
                self.conversation_history = [{
                    "user": "Previous conversation",
                    "assistant": summary,
                    "tokens": summary_tokens
                }] + recent_exchanges
            else:
                # If budget too small for summary, just keep recent exchanges
                self.conversation_history = recent_exchanges
    
    def _summarize_history(self, history_text):
        """Summarize conversation history"""
        # In production, would use an LLM call
        return f"[Summary of previous conversation with {len(history_text.split())} words]"
    
    def get_formatted_history(self):
        """Get formatted history for context inclusion"""
        return "\n".join([
            f"User: {exchange['user']}\nAssistant: {exchange['assistant']}"
            for exchange in self.conversation_history
        ])
    
    def generate_response(self, query):
        history = self.get_formatted_history()
        
        context = f"""
        <context name="conversation_history" priority="medium">
        {history}
        </context>
        
        <context name="current_query" priority="high">
        {query}
        </context>
        """
        
        response = llm.generate(context)
        self.add_exchange(query, response)
        return response
```

### Ignoring Model Attention Behavior

**Anti-Pattern:** Failing to account for how LLMs actually process and attend to context, particularly the recency bias.

**Example:**
```python
# ❌ Ignoring attention patterns
def create_instructional_context(query, critical_instructions, knowledge):
    # Places critical instructions far from the query
    context = f"""
    {critical_instructions}
    
    {knowledge}
    
    User query: {query}
    """
    
    return llm.generate(context)
```

**Why It Fails:**
- Places critical instructions too far from the query
- Doesn't account for recency bias in LLMs
- Fails to use formatting to direct attention
- Doesn't emphasize critical information
- Buries important instructions under other content

**Better Approach:**
```python
def create_attention_aware_context(query, critical_instructions, knowledge):
    # Structure with attention patterns in mind
    context = f"""
    <context name="critical_instructions" priority="high">
    # IMPORTANT INSTRUCTIONS
    {critical_instructions}
    </context>
    
    <context name="knowledge" priority="medium">
    {knowledge}
    </context>
    
    <context name="user_query" priority="high">
    {query}
    </context>
    
    <context name="final_reminder" priority="high">
    # REMINDER OF KEY INSTRUCTIONS
    {extract_key_points(critical_instructions)}
    </context>
    """
    
    return llm.generate(context)

def extract_key_points(instructions):
    """Extract 2-3 most critical points from instructions"""
    # In production would use more sophisticated extraction
    lines = instructions.split("\n")
    important_lines = [l for l in lines if "important" in l.lower() or "critical" in l.lower()]
    return "\n".join(important_lines[:3])
```

### Failing to Update Stale Context

**Anti-Pattern:** Using outdated or stale context modules without a systematic approach to freshness and updates.

**Example:**
```python
# ❌ No mechanism for context freshness
class StaticKnowledgeBase:
    def __init__(self, knowledge_files_path):
        # Load knowledge once at initialization
        self.knowledge = {}
        for filename in os.listdir(knowledge_files_path):
            with open(os.path.join(knowledge_files_path, filename), 'r') as f:
                self.knowledge[filename] = f.read()
    
    def get_knowledge(self, topic):
        # Simply return static knowledge with no freshness check
        return self.knowledge.get(topic, "No information available")
```

**Why It Fails:**
- No mechanism to detect outdated information
- No regular update process
- No tracking of information age
- Can lead to providing inaccurate or obsolete information
- No versioning or change history

**Better Approach:**
```python
class FreshnessAwareKnowledgeBase:
    def __init__(self, knowledge_files_path, max_age_days=90):
        self.knowledge_path = knowledge_files_path
        self.max_age_days = max_age_days
        self.knowledge_cache = {}
        self.last_updated = {}
        self.update_schedule = {}
    
    def get_knowledge(self, topic):
        """Get knowledge with freshness check"""
        # Check if we need to reload from disk
        self._ensure_loaded(topic)
        
        # Check freshness
        if topic in self.last_updated:
            age_days = (datetime.now() - self.last_updated[topic]).days
            
            # Add freshness metadata
            knowledge = self.knowledge_cache[topic]
            if age_days > self.max_age_days:
                knowledge = self._add_staleness_warning(knowledge, age_days)
                # Schedule for update
                self._schedule_update(topic, priority="high")
            elif age_days > self.max_age_days // 2:
                # Schedule for update but with lower priority
                self._schedule_update(topic, priority="medium")
            
            return knowledge
        
        return "No information available"
    
    def _ensure_loaded(self, topic):
        """Ensure topic is loaded in cache"""
        topic_path = os.path.join(self.knowledge_path, f"{topic}.md")
        
        # If not in cache or file has been modified, load it
        if topic not in self.knowledge_cache or self._file_modified(topic_path, self.last_updated.get(topic)):
            if os.path.exists(topic_path):
                with open(topic_path, 'r') as f:
                    self.knowledge_cache[topic] = f.read()
                self.last_updated[topic] = datetime.fromtimestamp(os.path.getmtime(topic_path))
    
    def _file_modified(self, filepath, last_updated):
        """Check if file has been modified since last loaded"""
        if not last_updated:
            return True
        
        file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
        return file_mtime > last_updated
    
    def _add_staleness_warning(self, knowledge, age_days):
        """Add warning about potentially stale information"""
        warning = f"""
        [NOTE: This information is {age_days} days old and may not reflect the latest developments.
        It will be updated soon.]
        """
        
        return warning + "\n\n" + knowledge
    
    def _schedule_update(self, topic, priority):
        """Schedule a topic for update"""
        self.update_schedule[topic] = {
            "priority": priority,
            "scheduled_at": datetime.now()
        }
        
        # In a real system, this would trigger an update workflow
        if priority == "high":
            # Could trigger immediate update process
            pass
```

## 6. Model-Specific Insights

Different LLMs handle context in subtly different ways, requiring adaptation of context management strategies:

### Context Window Handling Differences

**GPT-4 and GPT-4o (OpenAI)**

- **Context Window**: Up to 128K tokens (depending on model version)
- **Attention Pattern**: Shows recency bias but with stronger long-range capacity
- **Optimal Structure**: Responds well to clear headings and structured format
- **Key Consideration**: Benefits from explicit formatting and clear section demarcation
- **Recommended Pattern**:
  ```
  # System Instructions
  [instructions here]
  
  # Retrieved Information
  [information here]
  
  # User Query
  [query here]
  ```

**Claude 3 (Anthropic)**

- **Context Window**: Up to 200K tokens (Claude 3 Opus)
- **Attention Pattern**: Strong with MCP structure and explicit priorities
- **Optimal Structure**: MCP format with named context blocks and priorities
- **Key Consideration**: Very responsive to explicit priority signaling
- **Recommended Pattern**:
  ```
  <context name="system" priority="high">
  [instructions here]
  </context>
  
  <context name="knowledge" priority="medium">
  [information here]
  </context>
  
  <context name="query" priority="high">
  [query here]
  </context>
  ```

**Gemini (Google)**

- **Context Window**: Up to 128K tokens (Gemini Ultra)
- **Attention Pattern**: Good long-range attention with some recency bias
- **Optimal Structure**: Responds well to clearly delimited sections
- **Key Consideration**: Benefits from explicit examples of desired output format
- **Recommended Pattern**:
  ```
  SYSTEM INSTRUCTIONS:
  [instructions here]
  
  REFERENCE INFORMATION:
  [information here]
  
  USER QUESTION:
  [query here]
  ```

**Llama 3 (Meta)**

- **Context Window**: Up to 128K tokens
- **Attention Pattern**: Exhibits stronger recency bias than some other models
- **Optimal Structure**: Clear delimiters and repetition of key instructions
- **Key Consideration**: Benefits from "sandwiching" critical instructions
- **Recommended Pattern**:
  ```
  <instructions>
  [instructions here]
  </instructions>
  
  <information>
  [information here]
  </information>
  
  <question>
  [query here]
  </question>
  
  Remember to follow the instructions above.
  ```

### Recency Bias and Attention Decay

All LLMs exhibit some form of recency bias and attention decay, but with different characteristics:

**Common Patterns Across Models:**

1. **Proximity Effect**: Information closer to the query receives more attention
   - Position critical information either at the beginning or near the query
   - Consider repeating key instructions both early and late in context

2. **Attention Dilution**: Very long contexts cause attention to spread thin
   - For critical information, use explicit markers (e.g., "IMPORTANT:", "NOTE:")
   - Use formatting (bold, headers, bullet points) to enhance visibility

3. **Memory Degradation**: Information in the middle of long contexts tends to be forgotten
   - Avoid placing critical information in the middle of long contexts
   - Consider "chunking" information into distinct, labeled sections

**Model-Specific Strategies for Mitigating Attention Decay:**

```python
def optimize_context_for_model(context, model_name):
    """Apply model-specific optimization for attention patterns"""
    if model_name.lower() in ["gpt-4", "gpt-4o"]:
        # OpenAI models: Use markdown structure and headers
        return optimize_for_gpt(context)
    elif model_name.lower().startswith("claude"):
        # Anthropic models: Use MCP format
        return optimize_for_claude(context)
    elif model_name.lower().startswith("gemini"):
        # Google models: Use clear delimiters
        return optimize_for_gemini(context)
    elif model_name.lower().startswith("llama"):
        # Meta models: Use XML tags and instruction sandwiching
        return optimize_for_llama(context)
    else:
        # Default optimization
        return add_generic_attention_markers(context)

def optimize_for_gpt(context):
    """Optimize context for GPT models"""
    # Extract parts
    parts = extract_context_parts(context)
    
    # Reformat with markdown structure
    formatted = "# System Instructions\n\n"
    formatted += parts.get("instructions", "") + "\n\n"
    
    if "knowledge" in parts:
        formatted += "# Reference Information\n\n"
        formatted += parts["knowledge"] + "\n\n"
    
    if "history" in parts:
        formatted += "# Conversation History\n\n"
        formatted += parts["history"] + "\n\n"
    
    formatted += "# Current Query\n\n"
    formatted += parts.get("query", "") + "\n\n"
    
    # Add reminder of key instructions
    if "instructions" in parts:
        key_points = extract_key_points(parts["instructions"])
        formatted += "# Important Reminders\n\n"
        formatted += key_points
    
    return formatted

def optimize_for_claude(context):
    """Optimize context for Claude models using MCP"""
    # Extract parts
    parts = extract_context_parts(context)
    
    # Convert to MCP format
    formatted = ""
    
    if "instructions" in parts:
        formatted += f"""
<context name="system_instructions" priority="high">
{parts["instructions"]}
</context>

"""
    
    if "query" in parts:
        formatted += f"""
<context name="user_query" priority="high">
{parts["query"]}
</context>

"""
    
    if "knowledge" in parts:
        formatted += f"""
<context name="reference_information" priority="medium">
{parts["knowledge"]}
</context>

"""
    
    if "history" in parts:
        formatted += f"""
<context name="conversation_history" priority="low">
{parts["history"]}
</context>
"""
    
    return formatted.strip()

def optimize_for_gemini(context):
    """Optimize context for Gemini models"""
    # Extract parts
    parts = extract_context_parts(context)
    
    # Format with clear delimiters
    formatted = ""
    
    if "instructions" in parts:
        formatted += "SYSTEM INSTRUCTIONS:\n"
        formatted += parts["instructions"] + "\n\n"
    
    if "knowledge" in parts:
        formatted += "REFERENCE INFORMATION