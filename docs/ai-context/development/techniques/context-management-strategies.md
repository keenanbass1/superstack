# ❌ Bad approach: Unstructured context dumping
def generate_response(query, knowledge, conversation):
    # Just concatenate everything without structure
    prompt = f"""
Document 1: {knowledge[0]}
Document 2: {knowledge[1]}
Document 3: {knowledge[2]}

Previous conversation:
{conversation}

Query: {query}

Please answer the query based on the information above.
"""
    
    return llm.generate(prompt)
```

**Why It Fails:**
- Makes it difficult for the LLM to distinguish between different types of information
- Fails to prioritize more important information for the model
- Creates confusion when information from different sources conflicts
- Lacks clear separation between instructions, knowledge, and history
- Reduces the model's ability to properly attribute information sources

**Better Approach:**
```python
def generate_response(query, knowledge, conversation):
    # Structure the context with clear delineation and hierarchy
    prompt = f"""
<context name="system_instructions" priority="high">
You are a helpful assistant. Answer questions accurately based on the provided knowledge.
When information is missing or unclear, acknowledge this rather than guessing.
</context>

<context name="user_query" priority="high">
{query}
</context>

<context name="relevant_knowledge" priority="medium">
# Knowledge Sources
## Document 1
{knowledge[0]}

## Document 2
{knowledge[1]}

## Document 3
{knowledge[2]}
</context>

<context name="conversation_history" priority="low">
{conversation}
</context>
"""
    
    return llm.generate(prompt)
```

**Severity:** Medium
**AI-Specific:** Yes

### 3. Static Context Management [AP-CONTEXT-003]

**Problem:**
Using a fixed context strategy regardless of the conversation state, query complexity, or available information, leading to inefficient token usage and suboptimal responses.

**Example:**
```python
# ❌ Static context approach
class SimpleContextManager:
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base
        self.conversation_history = []
    
    def add_turn(self, user, assistant):
        self.conversation_history.append({"user": user, "assistant": assistant})
    
    def create_prompt(self, query):
        # Always include entire knowledge base and full conversation history
        knowledge = "\n\n".join(self.knowledge_base)
        history = "\n".join([f"User: {t['user']}\nAssistant: {t['assistant']}" 
                           for t in self.conversation_history])
        
        prompt = f"""
Knowledge:
{knowledge}

Conversation history:
{history}

User query: {query}
"""
        return prompt
```

**Why It Fails:**
- Wastes tokens on irrelevant knowledge for simple queries
- Cannot adapt to the evolving focus of a conversation
- Eventually exceeds token limits as conversation grows
- Gives equal weight to all knowledge, regardless of relevance
- Unable to optimize for different query types

**Better Approach:**
```python
class AdaptiveContextManager:
    def __init__(self, knowledge_base, embedding_model):
        self.knowledge_base = knowledge_base
        self.knowledge_embeddings = {k: embedding_model.embed(v) for k, v in knowledge_base.items()}
        self.conversation_history = []
        self.embedding_model = embedding_model
    
    def add_turn(self, user, assistant):
        self.conversation_history.append({"user": user, "assistant": assistant})
    
    def create_prompt(self, query):
        # Determine query complexity and type
        query_complexity = self._assess_complexity(query)
        query_embedding = self.embedding_model.embed(query)
        
        # Retrieve relevant knowledge based on query
        relevant_knowledge = self._retrieve_relevant_knowledge(query_embedding)
        
        # Adapt history handling based on conversation length and query
        processed_history = self._process_conversation_history(query_complexity)
        
        # Build adaptive context with proper structure
        context = self._build_structured_context(
            query, 
            relevant_knowledge, 
            processed_history,
            query_complexity
        )
        
        return context
    
    def _assess_complexity(self, query):
        # Analyze query to determine complexity
        tokens = len(query.split())
        has_technical_terms = any(term in query.lower() for term in ["how", "why", "explain", "compare"])
        
        if tokens > 20 and has_technical_terms:
            return "high"
        elif has_technical_terms:
            return "medium"
        else:
            return "low"
    
    def _retrieve_relevant_knowledge(self, query_embedding, max_items=3):
        # Calculate relevance scores
        scores = {}
        for key, emb in self.knowledge_embeddings.items():
            scores[key] = cosine_similarity(query_embedding, emb)
        
        # Get top-k most relevant items
        relevant_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:max_items]
        return {k: self.knowledge_base[k] for k, _ in relevant_items}
    
    def _process_conversation_history(self, complexity):
        # For simple queries, we might only need recent history
        if complexity == "low" and len(self.conversation_history) > 2:
            return self.conversation_history[-2:]
        
        # For medium complexity, keep last 5 turns
        elif complexity == "medium" and len(self.conversation_history) > 5:
            return self.conversation_history[-5:]
        
        # For complex queries, summarize older history and keep recent verbatim
        elif complexity == "high" and len(self.conversation_history) > 8:
            recent = self.conversation_history[-5:]
            older = self.conversation_history[:-5]
            older_summary = self._summarize_history(older)
            return [{"user": "Previous conversation", "assistant": older_summary}] + recent
        
        # Default to full history if it's short enough
        return self.conversation_history
    
    def _build_structured_context(self, query, knowledge, history, complexity):
        # Structure varies based on complexity
        context_parts = []
        
        # Always add system instructions
        context_parts.append("""
<context name="system_instructions" priority="high">
You are a helpful assistant providing accurate information based on the available knowledge.
</context>
""")
        
        # Add current query
        context_parts.append(f"""
<context name="user_query" priority="high">
{query}
</context>
""")
        
        # Add knowledge with appropriate priority
        if knowledge:
            knowledge_text = "\n\n".join([f"# {k}\n{v}" for k, v in knowledge.items()])
            priority = "high" if complexity == "high" else "medium"
            context_parts.append(f"""
<context name="relevant_knowledge" priority="{priority}">
{knowledge_text}
</context>
""")
        
        # Add conversation history
        if history:
            history_text = "\n".join([f"User: {t['user']}\nAssistant: {t['assistant']}" for t in history])
            context_parts.append(f"""
<context name="conversation_history" priority="low">
{history_text}
</context>
""")
        
        return "\n".join(context_parts)
    
    def _summarize_history(self, history):
        # In a real implementation, this would use an LLM to create a summary
        return f"[Summary of {len(history)} previous conversation turns]"
```

**Severity:** Medium
**AI-Specific:** No

### 4. Ineffective Chunking Strategy [AP-CONTEXT-004]

**Problem:**
Using simplistic text chunking approaches that break semantic units, resulting in fragmented context and reduced retrieval effectiveness in RAG systems.

**Example:**
```python
# ❌ Bad chunking approach
def chunk_document(document, chunk_size=1000):
    # Simple character-based chunking with fixed size
    chunks = []
    for i in range(0, len(document), chunk_size):
        chunks.append(document[i:i + chunk_size])
    return chunks
```

**Why It Fails:**
- Creates arbitrary breaks that may split sentences, paragraphs or logical sections
- Destroys semantic coherence of the content
- Results in chunks that lack sufficient context to stand alone
- Makes it difficult for embedding models to create meaningful vector representations
- Reduces the effectiveness of similarity search for retrieving relevant information

**Better Approach:**
```python
def chunk_document(document, target_size=1000, overlap=100):
    """
    Chunk a document with intelligent boundary detection.
    
    Args:
        document: Text to be chunked
        target_size: Target chunk size in characters
        overlap: Overlap between chunks in characters
        
    Returns:
        List of text chunks
    """
    # Step 1: Split into paragraphs first
    paragraphs = document.split('\n\n')
    
    # Step 2: Combine paragraphs into chunks with semantic boundaries
    chunks = []
    current_chunk = []
    current_size = 0
    
    for paragraph in paragraphs:
        paragraph_size = len(paragraph)
        
        # If adding this paragraph exceeds target size and we already have content,
        # save current chunk and start a new one
        if current_size + paragraph_size > target_size and current_chunk:
            chunks.append('\n\n'.join(current_chunk))
            
            # Keep some paragraphs for overlap if available
            overlap_size = 0
            overlap_paragraphs = []
            
            # Work backwards through current chunk to create overlap
            for i in range(len(current_chunk) - 1, -1, -1):
                if overlap_size + len(current_chunk[i]) <= overlap:
                    overlap_paragraphs.insert(0, current_chunk[i])
                    overlap_size += len(current_chunk[i])
                else:
                    break
            
            current_chunk = overlap_paragraphs
            current_size = overlap_size
        
        # Add current paragraph to chunk
        current_chunk.append(paragraph)
        current_size += paragraph_size
    
    # Add the last chunk if there's anything left
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    
    # For documents with very large paragraphs, we might need to split paragraphs
    final_chunks = []
    for chunk in chunks:
        if len(chunk) <= target_size * 1.5:
            final_chunks.append(chunk)
        else:
            # Split large chunks at sentence boundaries
            sentences = split_into_sentences(chunk)
            sentence_chunks = []
            current_sentence_chunk = []
            current_size = 0
            
            for sentence in sentences:
                sentence_size = len(sentence)
                if current_size + sentence_size > target_size and current_sentence_chunk:
                    sentence_chunks.append(' '.join(current_sentence_chunk))
                    current_sentence_chunk = []
                    current_size = 0
                
                current_sentence_chunk.append(sentence)
                current_size += sentence_size
            
            if current_sentence_chunk:
                sentence_chunks.append(' '.join(current_sentence_chunk))
            
            final_chunks.extend(sentence_chunks)
    
    return final_chunks

def split_into_sentences(text):
    """Split text into sentences with basic heuristics."""
    # This is a simplified version - production code would use NLP libraries
    sentences = []
    current_sentence = ""
    
    for char in text:
        current_sentence += char
        if char in ['.', '!', '?'] and len(current_sentence.strip()) > 0:
            sentences.append(current_sentence.strip())
            current_sentence = ""
    
    if current_sentence.strip():
        sentences.append(current_sentence.strip())
    
    return sentences
```

**Severity:** High
**AI-Specific:** No

### 5. Context Amnesia [AP-CONTEXT-005]

**Problem:**
Failing to maintain important information across multiple interaction turns, forcing users to repeatedly provide the same context and resulting in conversations that lack continuity.

**Example:**
```python
# ❌ Bad approach: No context persistence
def chat_with_llm(user_message):
    # Each interaction is treated as a completely new context
    response = llm.generate(f"User: {user_message}")
    return response

# Usage example showing the issue
response1 = chat_with_llm("My name is Alex and I'm working on a Python project.")
# Response might be: "Hi Alex, what kind of Python project are you working on?"

response2 = chat_with_llm("I'm having an issue with asyncio.")
# Response shows amnesia: "Asyncio is a library for writing concurrent code in Python.
# Can you tell me more about your project and the specific issue you're facing?"
```

**Why It Fails:**
- Loses critical user information between interactions
- Forces users to repeatedly provide the same context
- Creates an unnatural conversation experience
- Makes it impossible to build on previous exchanges
- Prevents the model from learning about user preferences and needs

**Better Approach:**
```python
class ContextPersistenceManager:
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.conversation_history = []
        self.user_profile = {}
        self.critical_context = {}
    
    def update_user_profile(self, message):
        """Extract and persist important user information."""
        # In a real implementation, this would use NER and other techniques
        # This is a simplified example
        name_match = re.search(r"my name is (\w+)", message.lower())
        if name_match:
            self.user_profile["name"] = name_match.group(1)
        
        project_match = re.search(r"working on (a|an) ([^.]+)", message.lower())
        if project_match:
            self.user_profile["project"] = project_match.group(2)
        
        # Update other profile attributes similarly
    
    def extract_critical_context(self, message, response):
        """Identify information that should persist across turns."""
        # In production, this would use more sophisticated techniques
        if "issue with" in message.lower() or "problem with" in message.lower():
            problem_area = message.split("issue with ")[-1].split("problem with")[-1].split(".")[0]
            self.critical_context["current_problem"] = problem_area
    
    def create_persistent_context(self, user_message):
        """Create context with persistence of important information."""
        # Update user profile based on new message
        self.update_user_profile(user_message)
        
        # Prepare context components
        context_elements = []
        
        # Add user profile information
        if self.user_profile:
            profile_text = "\n".join([f"{k}: {v}" for k, v in self.user_profile.items()])
            context_elements.append(f"""
<context name="user_profile" priority="high">
{profile_text}
</context>
""")
        
        # Add critical persistent context
        if self.critical_context:
            critical_text = "\n".join([f"{k}: {v}" for k, v in self.critical_context.items()])
            context_elements.append(f"""
<context name="critical_information" priority="high">
{critical_text}
</context>
""")
        
        # Add conversation history
        if self.conversation_history:
            history_text = "\n".join([
                f"User: {turn['user']}\nAssistant: {turn['assistant']}" 
                for turn in self.conversation_history[-5:]  # Keep last 5 turns
            ])
            context_elements.append(f"""
<context name="conversation_history" priority="medium">
{history_text}
</context>
""")
        
        # Add current message
        context_elements.append(f"""
<context name="current_message" priority="high">
{user_message}
</context>
""")
        
        return "\n".join(context_elements)
    
    def chat(self, user_message):
        """Process a user message with persistent context."""
        # Create context with persistence
        context = self.create_persistent_context(user_message)
        
        # Generate response
        response = self.llm_client.generate(context)
        
        # Extract critical information from this exchange
        self.extract_critical_context(user_message, response)
        
        # Update conversation history
        self.conversation_history.append({
            "user": user_message,
            "assistant": response
        })
        
        return response

# Usage showing improved context persistence
context_manager = ContextPersistenceManager(llm_client)

response1 = context_manager.chat("My name is Alex and I'm working on a Python project.")
# Response: "Hi Alex, what kind of Python project are you working on?"

response2 = context_manager.chat("I'm having an issue with asyncio.")
# Improved response: "I understand you're having issues with asyncio in your Python project, Alex.
# Can you describe what specific problem you're encountering with asyncio?"
```

**Severity:** High
**AI-Specific:** Yes
</context>

<context name="context_management_reasoning_principles" priority="low">
## Reasoning Principles

Understanding why context management works helps create more effective implementations:

### 1. Information Relevance Principle
Context management effectiveness is directly proportional to the relevance of provided information to the current query. This explains why retrieval-based approaches that dynamically select content outperform static context approaches. Our brains work similarly—we don't recall every memory when answering a question, but selectively retrieve relevant information.

### 2. Working Memory Constraints
LLMs, like humans, have finite "working memory" (context window) that limits how much information they can process at once. Effective context management respects these constraints by prioritizing important information and structuring it for optimal processing. This explains why techniques like hierarchical summarization work well—they preserve key information while reducing token consumption.

### 3. Context Hierarchy and Structure
LLMs process information more effectively when it's organized in a clear hierarchy. This is why structured approaches like MCP outperform unstructured context—they provide explicit signals about information importance and relationships. Similar to how outlines help humans organize complex information, structured context helps LLMs understand what to pay attention to.

### 4. Temporal Recency Bias
LLMs tend to give more weight to information positioned later in the context window. This explains why putting the most important information near the user query often yields better results. Understanding this bias helps us design more effective context structures—similar to how speakers often save key points for the end of a presentation.

### 5. Semantic Coherence Principle
Context chunks maintain more meaningful embeddings when they preserve semantic boundaries (paragraphs, sections) rather than arbitrary splits. This explains why intelligent chunking outperforms naive approaches. Just as a human would struggle to understand a book with randomly inserted page breaks mid-sentence, LLMs process content more effectively when semantic units stay intact.

### 6. Query-Context Alignment
The effectiveness of a RAG system largely depends on the semantic alignment between queries and retrieved context. This explains why embedding models optimized for retrieval often outperform general-purpose embeddings. It's similar to how we might need to rephrase a question to get better answers when searching a database or asking a colleague.

### 7. Information Persistence Dynamics
Not all information should persist equally across conversation turns. Context management systems perform better when they selectively maintain critical information while allowing less important details to fade. This mimics human conversation, where certain key facts (names, main topics) persist while minor details drop away unless explicitly referenced.
</context>

<context name="context_management_model_specific_notes" priority="low">
## Model-Specific Implementation Notes

### For Claude (Anthropic)
- Claude responds particularly well to the Model Context Protocol (MCP) format with explicitly named context sections
- Strongly favors structured, hierarchical information with clear headers and section breaks
- Can handle more verbose and detailed context compared to some other models
- Benefits from explicit attribution and source references for knowledge
- For long conversations, use a sliding window approach with hierarchical summarization
- Example optimization:
  ```python
  # Claude-optimized context structure
  def claude_optimized_context(query, knowledge, history):
      return f"""
  <context name="system_instructions" priority="high">
  You are a helpful assistant answering questions based on the provided information.
  When information is cited from a source, include the source in your answer.
  </context>

  <context name="user_query" priority="high">
  {query}
  </context>

  <context name="relevant_knowledge" priority="medium">
  {knowledge}
  </context>

  <context name="conversation_history" priority="low">
  {history}
  </context>
  """
  ```

### For GPT (OpenAI)
- GPT models work well with multiple formats but benefit from clear hierarchical structure
- Very sensitive to instruction positioning—place critical instructions at the beginning and end
- Favors explicit role-based prompting ("You are an expert...")
- For RAG implementations, works best with smaller chunk sizes (around 512 tokens)
- Can benefit from "few-shot" examples of desired response formats within context
- Example optimization:
  ```python
  # GPT-optimized context structure  
  def gpt_optimized_context(query, knowledge, history):
      return f"""
  You are an expert assistant with access to the following information.
  
  # Relevant Knowledge
  {knowledge}
  
  # Conversation History
  {history}
  
  # User Query
  {query}
  
  Answer the user query based on the provided information. If you don't know, say so.
  """
  ```

### For Cursor AI
- Prioritize code-focused context and technical documentation
- Works best with explicit structure for code examples and technical explanations
- Benefits from API documentation and usage examples in context
- For code generation tasks, include relevant imports and setup code in context
- Example optimization:
  ```python
  # Cursor AI-optimized context for code tasks
  def cursor_optimized_context(query, code_documentation, examples):
      return f"""
  # System Instructions
  You are a coding assistant. Provide clear, well-commented code solutions.
  
  # Technical Documentation
  {code_documentation}
  
  # Example Usage
  {examples}
  
  # User Query
  {query}
  
  Provide a complete solution with proper imports and explanations.
  """
  ```

### For Local Models
- Focus on concise, token-efficient context to accommodate smaller context windows
- Provide more explicit instructions and examples as smaller models may require more guidance
- Chunk documents into smaller pieces (256-512 tokens) for retrieval
- Use more structured formats with explicit markers for different content types
- Adjust expectations for context handling capabilities accordingly
- Example optimization:
  ```python
  # Local model optimized context (more concise)
  def local_model_optimized_context(query, knowledge, history):
      return f"""
  INSTRUCTIONS: Answer the query using ONLY the information provided below.
  
  KNOWLEDGE:
  {knowledge}
  
  HISTORY:
  {history}
  
  QUERY: {query}
  
  ANSWER:
  """
  ```
</context>

<context name="context_management_related_concepts" priority="low">
## Related Concepts

- **Vector Embeddings** - Mathematical representations of text that capture semantic meaning, enabling similarity search for retrieval operations in context management systems. Vector embeddings allow the system to identify conceptually related information even when the exact wording differs.

- **Attention Mechanisms** - Core component of transformer-based models that determines which parts of input context to focus on when generating each output token. Understanding attention helps optimize context ordering and structuring to direct the model's focus appropriately.

- **Knowledge Graphs** - Structured knowledge representations that organize information as entities and relationships, often used alongside text-based context to provide structured domain knowledge to LLMs. They can enhance context management by adding explicit relational information.

- **Long-Term Memory for AI** - Systems that persist information beyond the immediate context window, creating an external "memory" that can be selectively retrieved based on relevance. These include vector databases, summarized conversation logs, and persistent user profiles.

- **Token Optimization** - Techniques to maximize information density while minimizing token usage, including compression, summarization, and selective context inclusion. This is critical for staying within context window limits while preserving key information.

- **Prompt Engineering** - The practice of designing effective prompts to guide LLM behavior, closely related to context management but focused more on instruction components than knowledge components. Well-engineered prompts can reduce the need for extensive context.

- **Retrieval Augmented Fine-Tuning** - Training approaches that adapt models to more effectively use retrieved information, bridging the gap between retrieval and generation capabilities. Models fine-tuned for RAG often require less explicit context structure.

- **Multi-Modal Context** - Integration of different data types (text, images, structured data) into a unified context representation for LLMs. This emerging area extends context management beyond text to include visual and structured information.

- **Agentic Frameworks** - Systems where LLMs act as agents with persistent state, tools, and long-term goals, requiring sophisticated context management to maintain coherence across complex, multi-step tasks. These frameworks require robust context management for state tracking.

- **Conversation Summarization** - Techniques for condensing conversation history to extract key points while reducing token usage, often used in conjunction with sliding window approaches for long interactions. This creates a hierarchical representation of conversation history.
</context>

<context name="context_management_practical_examples" priority="medium">
## Practical Examples

### Example 1: Implementing a Context-Aware Technical Support Bot

**Before:**
```python
def technical_support_bot(user_query):
    # Simple prompt with no context management
    prompt = f"""
You are a technical support bot. Answer the following query:

{user_query}
"""
    
    response = llm.generate(prompt)
    return response

# Example usage
query = "I'm getting a 'ModuleNotFoundError' when importing numpy."
response = technical_support_bot(query)
# Response likely to be generic due to lack of context
```

**After:**
```python
class TechnicalSupportBot:
    def __init__(self, knowledge_base_path, embedding_model, llm_model):
        # Load technical documentation
        self.knowledge_base = self._load_knowledge_base(knowledge_base_path)
        
        # Create vector embeddings for documentation
        self.embeddings = embedding_model
        self.vector_store = self._create_vector_store()
        
        # Initialize LLM
        self.llm = llm_model
        
        # Conversation tracking
        self.conversations = {}
    
    def _load_knowledge_base(self, path):
        """Load technical documentation from files."""
        knowledge_base = {}
        for filename in os.listdir(path):
            if filename.endswith('.md') or filename.endswith('.txt'):
                with open(os.path.join(path, filename), 'r') as f:
                    content = f.read()
                    knowledge_base[filename] = content
        return knowledge_base
    
    def _create_vector_store(self):
        """Create vector embeddings for knowledge base chunks."""
        chunks = []
        metadatas = []
        
        for doc_name, content in self.knowledge_base.items():
            # Chunk the document with semantic boundaries
            doc_chunks = self._chunk_document(content)
            
            for i, chunk in enumerate(doc_chunks):
                chunks.append(chunk)
                metadatas.append({"source": doc_name, "chunk": i})
        
        # Create embeddings and store in vector database
        embeddings = [self.embeddings.embed_query(chunk) for chunk in chunks]
        
        return {
            "chunks": chunks,
            "embeddings": embeddings,
            "metadata": metadatas
        }
    
    def _chunk_document(self, document, chunk_size=1000, overlap=100):
        """Split document into semantically coherent chunks."""
        paragraphs = document.split('\n\n')
        chunks = []
        current_chunk = []
        current_length = 0
        
        for para in paragraphs:
            para_length = len(para)
            
            if current_length + para_length > chunk_size and current_chunk:
                # Save current chunk and start a new one with overlap
                chunks.append('\n\n'.join(current_chunk))
                
                # Determine overlap paragraphs
                overlap_size = 0
                overlap_paragraphs = []
                
                for i in range(len(current_chunk) - 1, -1, -1):
                    if overlap_size + len(current_chunk[i]) <= overlap:
                        overlap_paragraphs.insert(0, current_chunk[i])
                        overlap_size += len(current_chunk[i])
                    else:
                        break
                
                current_chunk = overlap_paragraphs
                current_length = overlap_size
            
            current_chunk.append(para)
            current_length += para_length
        
        if current_chunk:
            chunks.append('\n\n'.join(current_chunk))
        
        return chunks
    
    def _get_relevant_documents(self, query, k=3):
        """Retrieve most relevant documentation for the query."""
        query_embedding = self.embeddings.embed_query(query)
        
        # Calculate cosine similarities
        similarities = []
        for i, emb in enumerate(self.vector_store["embeddings"]):
            similarity = self._cosine_similarity(query_embedding, emb)
            similarities.append((i, similarity))
        
        # Get top k results
        top_k = sorted(similarities, key=lambda x: x[1], reverse=True)[:k]
        
        relevant_docs = []
        for idx, score in top_k:
            chunk = self.vector_store["chunks"][idx]
            metadata = self.vector_store["metadata"][idx]
            relevant_docs.append({
                "content": chunk,
                "source": metadata["source"],
                "score": score
            })
        
        return relevant_docs
    
    def _cosine_similarity(self, v1, v2):
        """Calculate cosine similarity between two vectors."""
        dot_product = sum(a * b for a, b in zip(v1, v2))
        magnitude1 = math.sqrt(sum(a * a for a in v1))
        magnitude2 = math.sqrt(sum(b * b for b in v2))
        return dot_product / (magnitude1 * magnitude2)
    
    def _analyze_query(self, query):
        """Extract key information from the query."""
        # Simplified analysis - production would use more NLP
        error_match = re.search(r"'([^']+)'", query)
        error_type = error_match.group(1) if error_match else None
        
        module_match = re.search(r"importing (\w+)", query)
        module = module_match.group(1) if module_match else None
        
        return {
            "error_type": error_type,
            "module": module,
            "has_code": "```" in query or "    " in query,
            "is_error": "error" in query.lower() or "exception" in query.lower(),
            "complexity": "complex" if len(query.split()) > 20 else "simple"
        }
    
    def _create_structured_context(self, user_id, query, query_analysis):
        """Create MCP-structured context for the query."""
        # Get conversation history
        conversation = self.conversations.get(user_id, [])
        
        # Retrieve relevant documentation
        relevant_docs = self._get_relevant_documents(query)
        
        # Format documentation
        docs_text = ""
        for i, doc in enumerate(relevant_docs):
            docs_text += f"### Document {i+1}: {doc['source']}\nRelevance: {doc['score']:.2f}\n\n{doc['content']}\n\n"
        
        # Create system instructions based on query analysis
        instructions = "You are a technical support assistant specializing in Python programming."
        
        if query_analysis["is_error"]:
            instructions += " Focus on diagnosing and solving the error."
        
        if query_analysis["has_code"]:
            instructions += " Analyze the provided code carefully."
        
        if query_analysis["error_type"]:
            instructions += f" Pay special attention to '{query_analysis['error_type']}' errors."
        
        # Structure the context
        context = f"""
<context name="system_instructions" priority# Context Management Strategies for LLMs

> Effective strategies for managing, optimizing, and leveraging context in large language model interactions to improve performance, accuracy, and efficiency.

## Metadata
- **Priority:** high
- **Domain:** llm-integration
- **Target Models:** claude, gpt, llama, mistral
- **Related Modules:** retrieval-augmented-generation, prompt-engineering, token-optimization, knowledge-graphs

## Module Overview

This module provides comprehensive guidance on managing context effectively when working with large language models (LLMs). It covers foundational concepts of context windows, practical strategies for context optimization, retrieval techniques, and implementation patterns. The module addresses common challenges such as context limitations, information retrieval, and context structuring to maximize the effectiveness of LLM interactions while minimizing token usage and costs.

<!-- 
NOTE: This module is structured following optimal prompt engineering principles:
1. Each section begins with a clear conceptual foundation
2. Content is organized from most to least important
3. Examples use few-shot patterns to demonstrate application
4. Decision trees guide practical implementation
5. Anti-patterns show common mistakes to avoid
6. Model-specific notes provide tailored guidance
-->

<context name="context_management_definition" priority="high">
## Conceptual Foundation

Context management for Large Language Models (LLMs) refers to the systematic organization, optimization, and delivery of information to an LLM to enable it to generate accurate, relevant, and coherent responses to user queries. It encompasses strategies for structuring, retrieving, prioritizing, and segmenting information within the LLM's context window.

Context management is critical because it directly affects:
1. The quality and accuracy of LLM outputs
2. The efficient use of token limits and computational resources
3. The ability to provide LLMs with up-to-date and relevant information
4. The mitigation of hallucinations and knowledge gaps in LLM responses

The key characteristics of effective context management include:
- **Relevance**: Ensuring context contains information most pertinent to the current query
- **Efficiency**: Optimizing token usage to stay within context window constraints
- **Structure**: Organizing information in ways that help the LLM understand relationships and priority
- **Persistence**: Maintaining important context across multiple interactions
- **Adaptability**: Dynamically adjusting context based on conversation flow or task requirements
- **Retrieval Integration**: Combining external knowledge retrieval with in-context processing
</context>

<context name="context_management_core_principles" priority="high">
## Core Principles

### 1. Context Optimization
Context optimization involves strategically selecting, formatting, and organizing information to maximize the utility of the limited context window available to LLMs.

**Implementation Guidelines:**
- Prioritize information based on relevance to the current query
- Remove redundant or superfluous information to reduce token consumption
- Structure context to emphasize the most important information first
- Use formatting techniques like bullet points, headers, and emphasis to highlight key information
- Implement dynamic context management that adjusts based on conversation state

**Example: Query-Focused Context Selection**
```python
def optimize_context(query, available_context, max_tokens=8000):
    # Compute relevance scores for each context chunk
    relevance_scores = [(chunk, compute_relevance(query, chunk)) 
                         for chunk in available_context]
    
    # Sort chunks by relevance score (descending)
    sorted_chunks = sorted(relevance_scores, key=lambda x: x[1], reverse=True)
    
    # Select chunks until we reach the token limit
    selected_chunks = []
    token_count = 0
    
    for chunk, score in sorted_chunks:
        chunk_tokens = len(tokenize(chunk))
        if token_count + chunk_tokens <= max_tokens:
            selected_chunks.append(chunk)
            token_count += chunk_tokens
        else:
            break
    
    # Format the selected chunks with headers and structure
    formatted_context = format_context_chunks(selected_chunks)
    
    return formatted_context
```

### 2. Retrieval-Augmented Generation
Retrieval-Augmented Generation (RAG) combines external knowledge retrieval with the generative capabilities of LLMs to provide accurate, up-to-date information beyond the model's training data.

**Implementation Guidelines:**
- Implement vector-based search for finding relevant information from knowledge bases
- Create effective chunking strategies that preserve semantic coherence
- Balance retrieval precision with context breadth
- Ensure proper attribution and provenance of retrieved information
- Implement feedback loops to improve retrieval quality over time

**Example: Basic RAG Implementation**
```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

def create_rag_system(documents):
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    
    # Create vector embeddings and store
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    # Create a retrieval-based QA chain
    llm = OpenAI(temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # Simple approach that stuffs all retrieved docs into context
        retriever=vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}  # Retrieve top 5 most relevant chunks
        )
    )
    
    return qa_chain

# Usage
qa_system = create_rag_system(documents)
answer = qa_system.run("What is the capital of France?")
```

### 3. Effective Context Structuring
Context structuring involves formatting and organizing information to enhance the LLM's ability to understand, prioritize, and utilize the provided context.

**Implementation Guidelines:**
- Use clear headers and sections to delineate different types of information
- Apply consistent formatting patterns the LLM can recognize
- Implement priority signaling through explicit tagging or positioning
- Structure content from most to least important when possible
- Use Model Context Protocol (MCP) or similar standardized formatting for model-agnostic context management

**Example: Structured Context with MCP**
```python
def create_structured_context(user_query, system_instructions, 
                             knowledge_context, conversation_history):
    """
    Format context using Model Context Protocol (MCP) structure
    """
    structured_context = f"""
<context name="system_instructions" priority="high">
{system_instructions}
</context>

<context name="user_query" priority="high">
{user_query}
</context>

<context name="relevant_knowledge" priority="medium">
{knowledge_context}
</context>

<context name="conversation_history" priority="low">
{conversation_history}
</context>
"""
    return structured_context

# Usage example
context = create_structured_context(
    user_query="How do I implement a binary search tree in Python?",
    system_instructions="You are a helpful programming assistant...",
    knowledge_context="Binary search trees are data structures where each node...",
    conversation_history="User: Can you help with data structures?\nAssistant: Of course..."
)
```
</context>

<context name="context_management_implementation_patterns" priority="medium">
## Implementation Patterns

### Common Context Management Patterns

#### Sliding Window Context
```python
def sliding_window_context(conversation_history, max_tokens=4000):
    """
    Keeps the most recent conversation exchanges within the context window.
    Useful for maintaining continuity in ongoing conversations.
    """
    tokens = tokenize(conversation_history)
    
    # If we're within limits, return the full history
    if len(tokens) <= max_tokens:
        return conversation_history
        
    # Otherwise, trim from the beginning to fit the window
    # Always keep the most recent interactions
    trimmed_tokens = tokens[-max_tokens:]
    return detokenize(trimmed_tokens)
```

#### Hierarchical Context Summarization
```python
def hierarchical_summarization(conversation_history, query):
    """
    Summarizes older conversation turns while preserving recent exchanges.
    Creates a hierarchy of detail with most recent being most detailed.
    """
    # Split history into turns
    turns = conversation_history.split('\n\n')
    
    # If we have more than 5 turns, summarize older ones
    if len(turns) > 5:
        older_turns = turns[:-5]
        recent_turns = turns[-5:]
        
        # Summarize older turns
        summary = summarize_content('\n\n'.join(older_turns))
        
        # Combine summary with recent detailed turns
        return f"Previous conversation summary:\n{summary}\n\n" + '\n\n'.join(recent_turns)
    
    return conversation_history
```

### Typical Application Sequence

1. **Query Analysis** - Analyze user query to identify information needs
   - Example: Extract key entities, intents, and constraints from the query
   - Properties: Intent classification, entity extraction, query decomposition

2. **Context Retrieval** - Retrieve relevant information from knowledge sources
   - Example: Use semantic search to find documents matching query intent
   - Properties: Vector search, relevance ranking, multi-index querying

3. **Context Processing** - Format and structure retrieved information
   - Example: Chunk, prioritize, and format information for LLM consumption
   - Properties: Deduplication, merging related chunks, removing redundancy

4. **Context Injection** - Provide processed context to the LLM
   - Example: Format context using a standardized protocol (e.g., MCP)
   - Properties: Priority signaling, metadata inclusion, source attribution

5. **Response Generation** - Generate response using the provided context
   - Example: Prompt the LLM to synthesize information from context
   - Properties: Guided response format, explicit reasoning steps, attribution

### Practical Examples

#### Example 1: Customer Support Knowledge Base Integration

**Before:**
```python
def answer_customer_query(query):
    # Direct query to LLM without context
    prompt = f"Answer the following customer question: {query}"
    
    response = llm.generate(prompt)
    return response
```

**After:**
```python
def answer_customer_query(query):
    # Step 1: Query Analysis
    query_embedding = embeddings.embed_query(query)
    
    # Step 2: Context Retrieval
    relevant_docs = vector_db.similarity_search(
        query_embedding, 
        k=3,
        filter={"category": "customer_support"}
    )
    
    # Step 3: Context Processing
    processed_context = ""
    for i, doc in enumerate(relevant_docs):
        processed_context += f"Document {i+1}:\n{doc.content}\n\n"
    
    # Step 4: Context Injection
    prompt = f"""
<context name="customer_support_knowledge" priority="high">
{processed_context}
</context>

<context name="response_guidelines" priority="medium">
- Be friendly and helpful
- Reference specific information from the knowledge base
- If you're unsure, say so rather than making up information
</context>

Please answer the following customer question using the provided knowledge:
{query}
"""
    
    # Step 5: Response Generation
    response = llm.generate(prompt)
    return response
```

**Key Improvements:**
- Adds relevant knowledge context for accurate responses
- Implements structured context with priority levels
- Includes guidelines for response formatting
- Retrieves information from external knowledge base
- Reduces hallucinations by grounding responses in documentation

#### Example 2: Long Document Analysis

**Before:**
```python
def analyze_document(document, question):
    # Try to push the entire document into context
    prompt = f"""
Document: {document}

Based on the document, answer this question: {question}
"""
    
    # Will fail for long documents exceeding context window
    try:
        response = llm.generate(prompt)
        return response
    except TokenLimitError:
        return "Document too long to process."
```

**After:**
```python
def analyze_document(document, question):
    # Step 1: Chunk the document
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_text(document)
    
    # Step 2: Create embeddings for chunks and question
    chunk_embeddings = [embeddings.embed_text(chunk) for chunk in chunks]
    question_embedding = embeddings.embed_query(question)
    
    # Step 3: Find most relevant chunks
    chunk_scores = [cosine_similarity(question_embedding, chunk_emb) 
                   for chunk_emb in chunk_embeddings]
    sorted_chunks = [chunks[i] for i in np.argsort(chunk_scores)[-5:]]
    
    # Step 4: Create context with relevant chunks
    context = "\n\n".join(sorted_chunks)
    
    # Step 5: Structure the prompt with context
    prompt = f"""
<context name="document_excerpt" priority="high">
{context}
</context>

Based on the provided document excerpts, please answer this question: {question}

If the information needed is not in the provided excerpts, please state that clearly.
"""
    
    response = llm.generate(prompt)
    return response
```

**Key Improvements:**
- Handles documents of any length through chunking
- Uses semantic search to find most relevant sections
- Optimizes token usage by including only relevant parts
- Adds clear instructions on handling missing information
- Structures context with explicit priority
</context>

<context name="context_management_decision_logic" priority="medium">
## Decision Logic for Implementation

### Step 1: Select Context Management Approach
```
START
│
├─ IF task requires external knowledge beyond LLM's training
│  └─ Use Retrieval-Augmented Generation (RAG)
│
├─ IF managing ongoing conversation
│  └─ Use Sliding Window + Summarization
│
├─ IF dealing with large documents
│  └─ Use Chunking + Semantic Search
│
├─ IF building an agent system
│  └─ Use Tool-Augmented Context
│
└─ OTHERWISE
   └─ Use Basic Prompt Engineering
```

### Step 2: Choose Context Processing Strategy
```
FOR EACH context source:
│
├─ IF source is structured data (JSON, CSV, tables)
│  └─ Convert to text with clear semantic structure
│
├─ IF source is unstructured text
│  ├─ IF text > 1000 tokens
│  │  └─ Split into semantic chunks
│  └─ ELSE
│     └─ Use as-is with formatting
│
├─ IF source is conversation history
│  ├─ IF history > 10 turns
│  │  └─ Summarize older turns, keep recent verbatim
│  └─ ELSE
│     └─ Keep full history
│
└─ IF source is system instructions
   └─ Place at beginning with high priority
```

### Step 3: Context Optimization Checklist
```
VALIDATION CHECKLIST:
│
├─ Relevance: Is all included context relevant to the current query?
│
├─ Structure: Is the context organized from most to least important?
│
├─ Format: Is information formatted clearly with headers and sections?
│
├─ Attribution: Are knowledge sources clearly attributed?
│
├─ Completeness: Is all necessary information included?
│
└─ Token efficiency: Have redundancies been eliminated?
```

### Key Questions to Consider

- What is the primary task or goal of the LLM interaction?
- What is the expected length and complexity of the interaction?
- What types of knowledge or context will the LLM need access to?
- Are there domain-specific requirements for context structuring?
- How will context change or evolve during the interaction?
- What are the token limitations of the chosen model?
- How can context be optimized for the specific model being used?
- What level of evidence or attribution is needed in responses?
</context>

<context name="context_management_anti_patterns" priority="medium">
## Anti-Patterns and Common Mistakes

### 1. Overloading the Context Window [AP-CONTEXT-001]

**Problem:**
Cramming excessive information into the context window without prioritization or filtering, which dilutes focus and wastes tokens on irrelevant content.

**Example:**
```python
# ❌ Bad approach: Dumping everything into context
def generate_response(query, documents, conversation_history):
    # Dump all documents into context regardless of relevance
    context = "\n\n".join(documents)
    
    # Add entire conversation history without summarization
    context += "\n\n" + "\n".join(conversation_history)
    
    # Add user query
    prompt = f"""
Here's all the information I have:

{context}

Now answer this: {query}
"""
    
    return llm.generate(prompt)
```

**Why It Fails:**
- Exceeds token limits for most models, causing truncation of potentially important information
- Includes irrelevant information that distracts the model from the core query
- Wastes computational resources on processing irrelevant content
- Dilutes the importance of truly relevant context
- Often leads to poor response quality as the model struggles to identify key information

**Better Approach:**
```python
def generate_response(query, documents, conversation_history):
    # Step 1: Embed query for semantic search
    query_embedding = embedding_model.embed(query)
    
    # Step 2: Find most relevant documents
    scored_docs = []
    for doc in documents:
        doc_embedding = embedding_model.embed(doc)
        relevance = cosine_similarity(query_embedding, doc_embedding)
        scored_docs.append((doc, relevance))
    
    # Select top-k most relevant documents
    top_docs = sorted(scored_docs, key=lambda x: x[1], reverse=True)[:3]
    relevant_context = "\n\n".join([doc for doc, _ in top_docs])
    
    # Step 3: Summarize older conversation history
    if len(conversation_history) > 5:
        recent_history = conversation_history[-5:]
        older_history = conversation_history[:-5]
        summary = summarize_text("\n".join(older_history))
        processed_history = f"Previous conversation summary: {summary}\n\n" + "\n".join(recent_history)
    else:
        processed_history = "\n".join(conversation_history)
    
    # Step 4: Structure context with priorities
    prompt = f"""
<context name="user_query" priority="high">
{query}
</context>

<context name="relevant_knowledge" priority="medium">
{relevant_context}
</context>

<context name="conversation_history" priority="low">
{processed_history}
</context>
"""
    
    return llm.generate(prompt)
```

**Severity:** High
**AI-Specific:** Yes

### 2. Neglecting Context Structure [AP-CONTEXT-002]

**Problem:**
Providing unstructured context without clear delineation between different types of information, making it difficult for the model to identify and prioritize relevant content.

**Example:**
```python
# ❌
    mag2 = Math.sqrt(mag2);
    
    return dotProduct / (mag1 * mag2);
  }

  /**
   * Format the conversation history
   * @returns {string} - Formatted conversation history
   */
  formatConversationHistory() {
    // If conversation is short, include everything
    if (this.conversation.length <= 5) {
      return this.conversation.map(turn => 
        `User: ${turn.user}\n${turn.assistant ? `Assistant: ${turn.assistant}\n` : ''}`
      ).join('\n');
    }
    
    // For longer conversations, summarize older turns
    const olderTurns = this.conversation.slice(0, -5);
    const recentTurns = this.conversation.slice(-5);
    
    // Format older turns for summarization
    const olderHistory = olderTurns.map(turn => 
      `User: ${turn.user}\n${turn.assistant ? `Assistant: ${turn.assistant}\n` : ''}`
    ).join('\n');
    
    // Summarize older history
    return this.summarizeConversation(olderHistory)
      .then(summary => {
        const recentHistory = recentTurns.map(turn => 
          `User: ${turn.user}\n${turn.assistant ? `Assistant: ${turn.assistant}\n` : ''}`
        ).join('\n');
        
        return `Previous conversation summary:\n${summary}\n\n${recentHistory}`;
      });
  }

  /**
   * Summarize conversation history using the LLM
   * @param {string} conversation - Conversation to summarize
   * @returns {Promise<string>} - Summary of the conversation
   */
  async summarizeConversation(conversation) {
    const response = await this.llmClient.complete({
      messages: [
        { role: "system", content: "Please provide a concise summary of the following conversation." },
        { role: "user", content: conversation }
      ]
    });
    
    return response.content;
  }

  /**
   * Create structured context using MCP format
   * @param {string} query - Current user query
   * @returns {Promise<string>} - Structured context
   */
  async createStructuredContext(query) {
    // Get conversation history
    const conversationContext = await this.formatConversationHistory();
    
    // Retrieve relevant knowledge
    const knowledgeContext = await this.retrieveKnowledge(query);
    
    // Build structured context
    let structuredContext = "";
    
    // Add system instructions with high priority
    if (this.systemInstructions) {
      structuredContext += `
<context name="system_instructions" priority="high">
${this.systemInstructions}
</context>

`;
    }
    
    // Add current query with high priority
    structuredContext += `
<context name="current_query" priority="high">
${query}
</context>

`;
    
    // Add relevant knowledge with medium priority
    if (knowledgeContext) {
      structuredContext += `
<context name="relevant_knowledge" priority="medium">
${knowledgeContext}
</context>

`;
    }
    
    // Add conversation history with low priority
    if (conversationContext) {
      structuredContext += `
<context name="conversation_history" priority="low">
${conversationContext}
</context>
`;
    }
    
    return structuredContext;
  }

  /**
   * Generate a response to the user query
   * @param {string} query - User query
   * @returns {Promise<string>} - LLM response
   */
  async generateResponse(query) {
    // Create structured context
    const context = await this.createStructuredContext(query);
    
    // Generate response
    const response = await this.llmClient.complete({
      messages: [
        { role: "system", content: context },
        { role: "user", content: "Please respond to my query using the provided context." }
      ]
    });
    
    // Add this turn to conversation history
    this.addConversationTurn(query, response.content);
    
    return response.content;
  }
}

// Simple demonstration clients
class SimpleTokenizer {
  tokenize(text) {
    // Simple approximation - split on spaces and punctuation
    return text.split(/[\s,.!?;:()[\]{}'"]+/).filter(token => token.length > 0);
  }
  
  countTokens(text) {
    return this.tokenize(text).length;
  }
}

class DefaultLLMClient {
  async complete({ messages }) {
    // This is a placeholder - in a real implementation, this would call an actual LLM API
    console.log("LLM called with:", messages);
    return { content: "This is a placeholder response. In a real implementation, this would be the LLM's response." };
  }
}

class DefaultEmbeddingClient {
  async createEmbedding(text) {
    // This is a placeholder - in a real implementation, this would call an embedding API
    // For demonstration, return a random vector of dimension 384
    return Array(384).fill(0).map(() => Math.random());
  }
}

// Example usage
async function demonstrateContextManager() {
  const contextManager = new ContextManager({
    maxTokens: 8000,
    systemInstructions: "You are a helpful AI assistant. Provide accurate and concise information."
  });
  
  // Create knowledge base
  await contextManager.createKnowledgeBase([
    "JavaScript is a programming language commonly used for web development. It allows you to implement complex features on web pages.",
    "React is a JavaScript library for building user interfaces. It is maintained by Meta and a community of individual developers and companies.",
    "Node.js is a JavaScript runtime environment that executes JavaScript code outside a web browser."
  ]);
  
  // Simulate conversation
  const queries = [
    "What is JavaScript?",
    "How does it relate to React?",
    "Can I use it outside the browser?"
  ];
  
  for (const query of queries) {
    const response = await contextManager.generateResponse(query);
    console.log(`User: ${query}`);
    console.log(`Assistant: ${response}\n`);
  }
}
```

### Reusable Component Example

```python
import os
from dataclasses import dataclass
from typing import List, Dict, Optional, Any

import numpy as np
from pydantic import BaseModel

class ContextWindow(BaseModel):
    """Configuration for context window management."""
    max_tokens: int = 8000
    high_priority_percent: float = 0.5
    medium_priority_percent: float = 0.3
    low_priority_percent: float = 0.2
    
    def token_allocation(self) -> Dict[str, int]:
        """Calculate token allocation for each priority level."""
        return {
            "high": int(self.max_tokens * self.high_priority_percent),
            "medium": int(self.max_tokens * self.medium_priority_percent),
            "low": int(self.max_tokens * self.low_priority_percent)
        }

@dataclass
class ContextChunk:
    """A chunk of context with metadata."""
    text: str
    name: str
    priority: str
    source: Optional[str] = None
    tokens: Optional[int] = None
    embedding: Optional[np.ndarray] = None

class MCPContextBuilder:
    """Builder for Model Context Protocol formatted context."""
    
    def __init__(self, config: ContextWindow = None):
        """Initialize the context builder with configuration."""
        self.config = config or ContextWindow()
        self.chunks: List[ContextChunk] = []
        self.tokenizer = None  # Would use a real tokenizer in practice
    
    def add_chunk(self, 
                 text: str, 
                 name: str, 
                 priority: str = "medium", 
                 source: Optional[str] = None) -> None:
        """
        Add a context chunk to the builder.
        
        Args:
            text: The text content of the chunk
            name: A descriptive name for the chunk
            priority: Priority level (high, medium, low)
            source: Source of the information (for attribution)
        """
        # Calculate token count (simplified)
        tokens = len(text.split()) if not self.tokenizer else self.tokenizer.count_tokens(text)
        
        chunk = ContextChunk(
            text=text,
            name=name,
            priority=priority,
            source=source,
            tokens=tokens
        )
        
        self.chunks.append(chunk)
    
    def optimize_chunks(self) -> List[ContextChunk]:
        """
        Optimize chunks to fit within context window constraints.
        Returns a list of chunks that fit within the token limits.
        """
        # Group chunks by priority
        high_priority = [c for c in self.chunks if c.priority == "high"]
        medium_priority = [c for c in self.chunks if c.priority == "medium"]
        low_priority = [c for c in self.chunks if c.priority == "low"]
        
        # Get token allocations
        allocations = self.config.token_allocation()
        
        # Helper to select chunks up to token limit
        def select_chunks(chunks, token_limit):
            selected = []
            tokens_used = 0
            for chunk in chunks:
                if tokens_used + chunk.tokens <= token_limit:
                    selected.append(chunk)
                    tokens_used += chunk.tokens
                else:
                    break
            return selected, tokens_used
        
        # Select high priority chunks (must include)
        selected_high, high_tokens = select_chunks(high_priority, allocations["high"])
        
        # If high priority doesn't use all its allocation, give remainder to medium
        medium_allocation = allocations["medium"] + (allocations["high"] - high_tokens)
        selected_medium, medium_tokens = select_chunks(medium_priority, medium_allocation)
        
        # If medium priority doesn't use all its allocation, give remainder to low
        low_allocation = allocations["low"] + (medium_allocation - medium_tokens)
        selected_low, _ = select_chunks(low_priority, low_allocation)
        
        # Combine all selected chunks
        return selected_high + selected_medium + selected_low
    
    def build(self) -> str:
        """Build the MCP-formatted context string."""
        # Optimize chunks to fit within context window
        optimized_chunks = self.optimize_chunks()
        
        # Build the context string
        context_str = ""
        for chunk in optimized_chunks:
            context_str += f"""
<context name="{chunk.name}" priority="{chunk.priority}">
{chunk.text}
</context>

"""
        
        return context_str.strip()

# Usage Example
builder = MCPContextBuilder(ContextWindow(max_tokens=4000))

# Add system instructions
builder.add_chunk(
    text="You are a helpful AI assistant specialized in programming topics.",
    name="system_instructions",
    priority="high"
)

# Add user query
builder.add_chunk(
    text="How do I implement a binary tree in Python?",
    name="user_query",
    priority="high"
)

# Add relevant knowledge
builder.add_chunk(
    text="A binary tree is a tree data structure where each node has at most two children...",
    name="binary_tree_definition",
    priority="medium", 
    source="Data Structures Handbook"
)

# Add code example
builder.add_chunk(
    text="""
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None
        
    def insert(self, value):
        if not self.root:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)
            
    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)
""",
    name="binary_tree_implementation",
    priority="medium",
    source="Python Examples"
)

# Add conversation history
builder.add_chunk(
    text="User: Can you help me with data structures in Python?\nAssistant: Sure! I'd be happy to help with Python data structures. What specifically would you like to know?",
    name="conversation_history",
    priority="low"
)

# Build the context
context = builder.build()
print(context)
```

**Usage Example:**

```python
# Initialize components
context_builder = MCPContextBuilder(ContextWindow(max_tokens=8000))
knowledge_retriever = DocumentRetriever(vector_db_url="localhost:8080")
conversation_manager = ConversationManager(max_history=10)

# Configure system
context_builder.add_chunk(
    text="You are a programming assistant specializing in Python. Provide clear, concise answers with code examples when relevant.",
    name="system_instructions",
    priority="high"
)

# Process user query
def process_query(query):
    # Add user query to context
    context_builder.add_chunk(
        text=query,
        name="user_query",
        priority="high"
    )
    
    # Retrieve relevant knowledge
    relevant_docs = knowledge_retriever.search(query, k=3)
    for i, doc in enumerate(relevant_docs):
        context_builder.add_chunk(
            text=doc.text,
            name=f"relevant_document_{i}",
            priority="medium",
            source=doc.source
        )
    
    # Add conversation history
    history = conversation_manager.get_formatted_history()
    if history:
        context_builder.add_chunk(
            text=history,
            name="conversation_history",
            priority="low"
        )
    
    # Build context and generate response
    context = context_builder.build()
    response = llm_client.generate(context, query)
    
    # Update conversation history
    conversation_manager.add_turn(query, response)
    
    return response
```
