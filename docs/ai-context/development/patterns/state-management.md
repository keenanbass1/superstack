## Using This Module

This state management context module can be referenced when:
- Designing the architecture for a new application
- Refactoring an existing application with state management issues
- Selecting appropriate libraries and patterns for specific state needs
- Troubleshooting performance problems related to state updates
- Implementing complex state interactions across components
- Evaluating tradeoffs between different state management approaches
- Training developers on best practices for state management

The core concepts to focus on when implementing state management are:
1. Categorizing your state appropriately (local, global, server, URL)
2. Following the principle of single source of truth
3. Using immutability for predictable state updates
4. Keeping state minimal and deriving values when possible
5. Organizing state by concern rather than mixing unrelated state
6. Implementing clear, unidirectional data flow

Remember that no single state management approach is ideal for all situations. Modern applications typically combine multiple approaches, such as component state for local UI, context for theme preferences, React Query for server state, and perhaps Redux for complex global state. Choose the right tool for each specific state management need.

Last Updated: April 13, 2025# State Management

> A comprehensive guide to patterns, principles, and implementations for managing application state in modern development.

## Metadata
- **Priority:** high
- **Domain:** development
- **Target Models:** claude, gpt, cursor-ai
- **Related Modules:** application-architecture, frontend-frameworks, performance-optimization, react-components

## Module Overview
This module explores state management approaches across different application types, providing patterns, decision frameworks, and implementation guidance to help choose and implement the right state management solution for various scenarios.

<context name="state_management_definition" priority="high">
## Conceptual Foundation

State management refers to the approach of storing, tracking, and maintaining the data that represents the condition of an application at a given time. This "state" can include:

- User interface state (form inputs, menu open/closed status, etc.)
- Application data (user information, content items, etc.)
- Navigation state (current route, previous pages, etc.)
- Server communication state (loading status, error messages, etc.)
- Authentication state (login status, user permissions, etc.)

Effective state management is crucial for:

1. **Predictability**: Creating applications that behave consistently
2. **Maintainability**: Making code easier to understand and debug
3. **Performance**: Optimizing rendering and updates
4. **Developer Experience**: Streamlining the development workflow
5. **Scalability**: Supporting application growth without increasing complexity

As applications grow in complexity, managing state becomes increasingly challenging. Different parts of an application need to access and modify shared data, leading to potential issues with data synchronization, component communication, and application flow. State management patterns and libraries provide structured approaches to address these challenges.
</context>

<context name="state_categories" priority="high">
## State Categories

Understanding the different categories of state is essential for choosing the right management approach:

### 1. Local (Component) State

**Definition**: State confined to a single component that doesn't need to be shared.

**Characteristics**:
- Only affects a single component's behavior or rendering
- Not needed by other parts of the application
- Often short-lived and transient
- Can be managed with simple mechanisms (e.g., React's useState)

**Examples**:
- Form input values during typing
- Toggle states (expanded/collapsed)
- Local UI interactions (hover states, focus)
- Component-specific loading indicators

### 2. Global (Application) State

**Definition**: State shared across multiple components or the entire application.

**Characteristics**:
- Needed by many different components
- Persists across component lifecycles
- Often represents core application data
- Requires more sophisticated management approaches

**Examples**:
- User authentication information
- Theme and appearance preferences
- Application-wide settings
- Shared data models

### 3. Server State

**Definition**: Data fetched from an external API or server that is cached locally.

**Characteristics**:
- Originates from external sources
- Requires synchronization with backend
- Has additional concerns like caching, revalidation, and optimistic updates
- Includes loading, error, and staleness states

**Examples**:
- API responses
- User data from database
- Content fetched from CMS
- Real-time data from websockets

### 4. URL State

**Definition**: State stored in the URL (route parameters, query strings).

**Characteristics**:
- Persists across page reloads
- Shareable via links
- Affects routing and navigation
- Makes state bookmarkable

**Examples**:
- Current page/view
- Search queries and filters
- Selected items or tabs
- Pagination parameters

### 5. Form State

**Definition**: State related to forms, including values, validation, and submission status.

**Characteristics**:
- Often complex with interdependent fields
- Requires validation logic
- Includes submission and error states
- May need persistence during navigation

**Examples**:
- Input values
- Validation errors
- Submission status
- Touched/dirty state

### 6. UI State

**Definition**: State specific to user interface elements and interactions.

**Characteristics**:
- Controls visual aspects of the interface
- Often transient
- Typically doesn't affect business logic
- Can be localized or global

**Examples**:
- Modal open/closed states
- Sidebar expanded/collapsed
- Animation states
- Tooltip visibility

Understanding these categories helps determine the appropriate state management approach for each situation. Many applications will use different strategies for different categories of state rather than a one-size-fits-all approach.
</context>

<context name="state_management_core_principles" priority="high">
## Core Principles

### 1. Single Source of Truth

**Principle:** Maintain a definitive source for each piece of state to avoid inconsistencies and synchronization issues.

**Implementation Guidelines:**
- Store each piece of state in exactly one location
- Derive dependent state rather than duplicating it
- Establish clear ownership for each piece of state
- Use references to shared state rather than copies

**Example:**
```javascript
// ❌ Multiple sources of truth
function UserProfile() {
  const [username, setUsername] = useState('');
  // Duplicated state derived from username
  const [displayName, setDisplayName] = useState('');
  
  // Now we have to manually sync these values
  const updateUsername = (newUsername) => {
    setUsername(newUsername);
    setDisplayName(newUsername);
  };
}

// ✅ Single source of truth
function UserProfile() {
  const [username, setUsername] = useState('');
  // Derived value, not state
  const displayName = username;
}
```

### 2. Immutability

**Principle:** Update state by creating new state objects rather than modifying existing ones, preserving history and enabling predictable updates.

**Implementation Guidelines:**
- Never directly modify state objects
- Create new copies of state when making changes
- Use functions like map, filter, and spread operators for updates
- Consider immutability libraries for complex state

**Example:**
```javascript
// ❌ Mutating state directly
function addTodo(todos, newTodo) {
  todos.push(newTodo); // Mutates the original array
  return todos;
}

// ✅ Maintaining immutability
function addTodo(todos, newTodo) {
  return [...todos, newTodo]; // Creates a new array
}
```

### 3. Unidirectional Data Flow

**Principle:** State changes follow a predictable, one-way path through the application, making it easier to track and debug.

**Implementation Guidelines:**
- Create a clear flow from state source to consuming components
- Pass state down through props or contexts, not up
- Implement actions or events to request state changes
- Avoid circular data flows

**Example:**
```javascript
// ❌ Bidirectional flow (harder to track)
function Parent() {
  const [count, setCount] = useState(0);
  return <Child count={count} updateCount={setCount} />;
}

// ✅ Unidirectional flow (more predictable)
function Parent() {
  const [count, setCount] = useState(0);
  
  const increment = () => setCount(count + 1);
  const decrement = () => setCount(count - 1);
  
  return <Child 
    count={count}
    onIncrement={increment}
    onDecrement={decrement}
  />;
}
```

### 4. Minimal State

**Principle:** Store only the essential state and derive everything else, reducing complexity and potential for inconsistencies.

**Implementation Guidelines:**
- Identify the minimal representation of application state
- Calculate derived values on-the-fly rather than storing them
- Avoid redundant state that can be computed from existing state
- Remove state that can be replaced with props

**Example:**
```javascript
// ❌ Redundant state
function ProductList() {
  const [products, setProducts] = useState([]);
  const [totalProducts, setTotalProducts] = useState(0);
  const [hasProducts, setHasProducts] = useState(false);
  
  useEffect(() => {
    setTotalProducts(products.length);
    setHasProducts(products.length > 0);
  }, [products]);
}

// ✅ Minimal state with derived values
function ProductList() {
  const [products, setProducts] = useState([]);
  
  // These are derived values, not state
  const totalProducts = products.length;
  const hasProducts = products.length > 0;
}
```

### 5. Isolation by Concern

**Principle:** Organize state by domain concerns, keeping related state together and separating unrelated state.

**Implementation Guidelines:**
- Group state logically by feature or domain
- Avoid giant state objects that mix unrelated concerns
- Create boundaries between different areas of state
- Consider local state for component-specific concerns

**Example:**
```javascript
// ❌ Mixed concerns
const appState = {
  currentUser: { id: 1, name: 'Alice' },
  isMenuOpen: true,
  products: [...],
  cartItems: [...],
  formData: { name: '', email: '' },
};

// ✅ Isolated concerns
const authState = {
  currentUser: { id: 1, name: 'Alice' },
};

const uiState = {
  isMenuOpen: true,
};

const productState = {
  products: [...],
};

const cartState = {
  items: [...],
};

const checkoutState = {
  formData: { name: '', email: '' },
};
```

### 6. Predictable Updates

**Principle:** State changes should be explicit, traceable, and consistent, making the application behavior more predictable.

**Implementation Guidelines:**
- Use pure functions for state updates
- Make state transitions explicit and trackable
- Implement explicit actions or events to trigger state changes
- Avoid side effects in state update logic

**Example:**
```javascript
// ❌ Unpredictable updates with implicit side effects
function incrementCounter() {
  counter += 1;
  if (counter % 10 === 0) {
    saveToDatabase(); // Side effect
    showNotification(); // Another side effect
  }
}

// ✅ Predictable updates with explicit actions
function counterReducer(state, action) {
  switch (action.type) {
    case 'INCREMENT':
      return { ...state, count: state.count + 1 };
    default:
      return state;
  }
}

// Side effects handled separately
function counterEffects(state, prevState) {
  if (state.count !== prevState.count && state.count % 10 === 0) {
    saveToDatabase();
    showNotification();
  }
}
```
</context>

<context name="state_management_patterns" priority="medium">
## Implementation Patterns

### Centralized Store Pattern

A single, centralized store containing all application state, used by libraries like Redux, Vuex, and NgRx.

```javascript
// Redux implementation example
import { createStore } from 'redux';

// Define initial state
const initialState = {
  counter: 0,
  user: null
};

// Reducer function
function appReducer(state = initialState, action) {
  switch (action.type) {
    case 'INCREMENT':
      return {
        ...state,
        counter: state.counter + 1
      };
    case 'SET_USER':
      return {
        ...state,
        user: action.payload
      };
    default:
      return state;
  }
}

// Create store
const store = createStore(appReducer);

// Dispatch actions
store.dispatch({ type: 'INCREMENT' });
store.dispatch({ 
  type: 'SET_USER', 
  payload: { id: 1, name: 'Alice' } 
});

// Access state
const currentState = store.getState();
```

**When to use:**
- Large applications with complex state
- When multiple components need the same state
- When you need to track all state changes
- When state needs to persist across route changes

### Context-Based State Pattern

Using React Context API or similar mechanisms to provide state to a component tree without prop drilling.

```jsx
// React Context implementation
import React, { createContext, useContext, useReducer } from 'react';

// Create context
const CounterContext = createContext();

// Reducer function
function counterReducer(state, action) {
  switch (action.type) {
    case 'INCREMENT':
      return { count: state.count + 1 };
    case 'DECREMENT':
      return { count: state.count - 1 };
    default:
      return state;
  }
}

// Provider component
function CounterProvider({ children }) {
  const [state, dispatch] = useReducer(counterReducer, { count: 0 });
  
  return (
    <CounterContext.Provider value={{ state, dispatch }}>
      {children}
    </CounterContext.Provider>
  );
}

// Custom hook to use the context
function useCounter() {
  const context = useContext(CounterContext);
  if (!context) {
    throw new Error('useCounter must be used within a CounterProvider');
  }
  return context;
}

// Usage in a component
function Counter() {
  const { state, dispatch } = useCounter();
  
  return (
    <div>
      Count: {state.count}
      <button onClick={() => dispatch({ type: 'INCREMENT' })}>
        Increment
      </button>
    </div>
  );
}

// App setup
function App() {
  return (
    <CounterProvider>
      <Counter />
    </CounterProvider>
  );
}
```

**When to use:**
- Medium-sized applications
- When you need to avoid prop drilling
- When state is shared by a specific subtree of components
- When you want a lighter solution than Redux

### Atomic State Pattern

Breaking state into small, independent "atoms" that components can subscribe to individually (used by libraries like Recoil and Jotai).

```javascript
// Using Recoil as an example
import { atom, useRecoilState, selector, useRecoilValue } from 'recoil';

// Define atoms (individual state pieces)
const counterAtom = atom({
  key: 'counterState',
  default: 0,
});

const userAtom = atom({
  key: 'userState',
  default: null,
});

// Define a selector (derived state)
const userNameSelector = selector({
  key: 'userNameSelector',
  get: ({ get }) => {
    const user = get(userAtom);
    return user ? user.name : 'Guest';
  },
});

// Component using the counter atom
function Counter() {
  const [count, setCount] = useRecoilState(counterAtom);
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}

// Component using the user name selector
function UserGreeting() {
  const userName = useRecoilValue(userNameSelector);
  
  return <p>Hello, {userName}!</p>;
}
```

**When to use:**
- When you need fine-grained updates
- When different parts of your app use different subsets of state
- When you want to optimize performance by minimizing re-renders
- When you need to combine local and global state management

### Server State Pattern

Managing server data with dedicated tools that handle caching, revalidation, and optimistic updates (used by libraries like React Query, SWR, and Apollo Client).

```javascript
// Using React Query as an example
import { useQuery, useMutation, useQueryClient } from 'react-query';

// Fetch function
const fetchTodos = async () => {
  const response = await fetch('/api/todos');
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
};

// Add todo function
const addTodo = async (newTodo) => {
  const response = await fetch('/api/todos', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(newTodo),
  });
  return response.json();
};

// Component using React Query
function TodoList() {
  const queryClient = useQueryClient();
  
  // Query for fetching todos
  const { data: todos, isLoading, error } = useQuery(
    'todos', 
    fetchTodos,
    {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 15 * 60 * 1000, // 15 minutes
    }
  );
  
  // Mutation for adding a todo
  const mutation = useMutation(addTodo, {
    onSuccess: () => {
      // Invalidate and refetch the todos query
      queryClient.invalidateQueries('todos');
    },
  });
  
  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;
  
  return (
    <div>
      <ul>
        {todos.map(todo => (
          <li key={todo.id}>{todo.title}</li>
        ))}
      </ul>
      <button
        onClick={() => mutation.mutate({ title: 'New Todo', completed: false })}
      >
        Add Todo
      </button>
    </div>
  );
}
```

**When to use:**
- When working with API data
- When you need caching and revalidation
- When implementing optimistic updates
- When handling loading and error states for server interactions

### URL State Pattern

Using the URL as a source of truth for certain state elements, making state shareable and bookmarkable.

```javascript
// Using React Router and its hooks
import { useNavigate, useLocation, useParams } from 'react-router-dom';

function ProductFilters() {
  const navigate = useNavigate();
  const location = useLocation();
  
  // Parse current filters from URL query parameters
  const queryParams = new URLSearchParams(location.search);
  const category = queryParams.get('category') || 'all';
  const sort = queryParams.get('sort') || 'newest';
  const page = parseInt(queryParams.get('page') || '1', 10);
  
  // Update filters by changing the URL
  const updateFilters = (newFilters) => {
    const newParams = new URLSearchParams(location.search);
    
    Object.entries(newFilters).forEach(([key, value]) => {
      if (value) {
        newParams.set(key, value);
      } else {
        newParams.delete(key);
      }
    });
    
    navigate(`${location.pathname}?${newParams.toString()}`);
  };
  
  return (
    <div>
      <div>
        <label>Category:</label>
        <select 
          value={category} 
          onChange={(e) => updateFilters({ category: e.target.value })}
        >
          <option value="all">All</option>
          <option value="electronics">Electronics</option>
          <option value="clothing">Clothing</option>
        </select>
      </div>
      
      <div>
        <label>Sort by:</label>
        <select 
          value={sort} 
          onChange={(e) => updateFilters({ sort: e.target.value })}
        >
          <option value="newest">Newest</option>
          <option value="price-low">Price: Low to High</option>
          <option value="price-high">Price: High to Low</option>
        </select>
      </div>
      
      <div>
        <button 
          onClick={() => updateFilters({ page: Math.max(1, page - 1) })}
          disabled={page === 1}
        >
          Previous Page
        </button>
        <span>Page {page}</span>
        <button 
          onClick={() => updateFilters({ page: page + 1 })}
        >
          Next Page
        </button>
      </div>
    </div>
  );
}
```

**When to use:**
- For shareable state (filters, search terms, etc.)
- To make state bookmarkable
- To persist state across page reloads
- For SEO-relevant state

### Proxy State Pattern

Using JavaScript Proxies to create a mutable API with immutability under the hood (used by libraries like Immer).

```javascript
// Using Immer with React
import { useImmer } from 'use-immer';

function TodoList() {
  const [todos, updateTodos] = useImmer([
    { id: 1, text: 'Learn React', completed: true },
    { id: 2, text: 'Learn Immer', completed: false }
  ]);
  
  const toggleTodo = (id) => {
    updateTodos(draft => {
      const todo = draft.find(todo => todo.id === id);
      if (todo) {
        // With Immer, we can "mutate" the draft directly
        // and it will produce a new immutable state
        todo.completed = !todo.completed;
      }
    });
  };
  
  const addTodo = (text) => {
    updateTodos(draft => {
      draft.push({
        id: Date.now(),
        text,
        completed: false
      });
    });
  };
  
  return (
    <div>
      <ul>
        {todos.map(todo => (
          <li key={todo.id} 
            style={{ textDecoration: todo.completed ? 'line-through' : 'none' }}
            onClick={() => toggleTodo(todo.id)}
          >
            {todo.text}
          </li>
        ))}
      </ul>
      <button onClick={() => addTodo('New Todo')}>Add Todo</button>
    </div>
  );
}
```

**When to use:**
- When working with deeply nested state
- To simplify immutable updates
- When migrating from mutable to immutable patterns
- To reduce boilerplate in state updates

### Publisher-Subscriber Pattern

Using an event system where components can subscribe to state changes without direct coupling.

```javascript
// Simple custom implementation
class StateManager {
  constructor(initialState = {}) {
    this.state = initialState;
    this.subscribers = new Map();
    this.nextSubscriberId = 1;
  }
  
  getState() {
    return this.state;
  }
  
  setState(newState) {
    this.state = { ...this.state, ...newState };
    this.notifySubscribers();
  }
  
  subscribe(callback) {
    const id = this.nextSubscriberId++;
    this.subscribers.set(id, callback);
    
    // Return unsubscribe function
    return () => {
      this.subscribers.delete(id);
    };
  }
  
  notifySubscribers() {
    for (const callback of this.subscribers.values()) {
      callback(this.state);
    }
  }
}

// Usage in a React component
function useStateManager(stateManager, selector) {
  const [selectedState, setSelectedState] = useState(
    selector(stateManager.getState())
  );
  
  useEffect(() => {
    const unsubscribe = stateManager.subscribe((state) => {
      setSelectedState(selector(state));
    });
    
    return unsubscribe;
  }, [stateManager, selector]);
  
  return selectedState;
}

// Create instance
const userStateManager = new StateManager({
  user: null,
  isLoading: false,
  error: null
});

// Component using the state manager
function UserProfile() {
  const user = useStateManager(
    userStateManager, 
    state => state.user
  );
  
  const login = (username, password) => {
    userStateManager.setState({ isLoading: true });
    
    // Simulated API call
    fetchUser(username, password)
      .then(user => {
        userStateManager.setState({ 
          user, 
          isLoading: false,
          error: null
        });
      })
      .catch(error => {
        userStateManager.setState({ 
          isLoading: false,
          error: error.message
        });
      });
  };
  
  // Rest of component
}
```

**When to use:**
- For loose coupling between components
- When state consumers are in different parts of the component tree
- For cross-cutting concerns like authentication or notifications
- When implementing custom state management solutions
</context>

<context name="state_management_decision_logic" priority="medium">
## Decision Logic

### Choosing a State Management Approach

```
What type of state are you managing?
├── Local UI State (temporary, component-specific)
│   ├── React/Vue/Angular component state
│   └── useState, ref, etc.
│
├── Form State (complex forms with validation)
│   ├── Simple Forms → useState or component state
│   ├── Complex Forms with validation → Form libraries (Formik, React Hook Form)
│   └── Complex Forms with many interdependencies → State management library
│
├── Global Application State (shared across components)
│   ├── Small Application with simple state → Context API
│   ├── Medium Application → Zustand, Jotai, simple Redux
│   ├── Large Application → Redux Toolkit, MobX, NgRx
│   └── Very complex state with many relationships → Consider normalized state patterns
│
├── Server State (data from APIs)
│   ├── Simple data fetching → useState + useEffect
│   ├── Moderate complexity → React Query, SWR, Apollo Client
│   ├── Complex queries and mutations → GraphQL with Apollo or Relay
│   └── Real-time data → WebSockets with specialized libraries
│
└── URL State (state in the URL)
    ├── Routing libraries (React Router, Vue Router)
    ├── Query parameter utilities
    └── History API wrappers
```

### Selecting a State Management Library

```
What are your requirements?
├── Bundle Size Concerns
│   ├── High Priority → Zustand, Jotai, Valtio
│   └── Low Priority → Redux, MobX
│
├── Learning Curve Tolerance
│   ├── Prefer Simplicity → Context API, Zustand
│   ├── Moderate Complexity → Redux Toolkit
│   └── Comfortable with Complexity → MobX, NgRx
│
├── Debugging Needs
│   ├── Excellent Devtools → Redux, NgRx
│   ├── Good Enough → MobX, Zustand
│   └── Not Important → Simple Context API
│
├── Team Experience
│   ├── Mostly React Developers → React-specific solutions
│   ├── Angular Developers → NgRx, RxJS
│   └── Vue Developers → Pinia, Vuex
│
├── Application Size
│   ├── Small → Context API, Zustand
│   ├── Medium → Redux Toolkit, Zustand
│   ├── Large → Redux Toolkit, NgRx, MobX
│   └── Microfront-ends → Consider isolated state per micro-frontend
│
└── Performance Concerns
    ├── Frequent Updates to Large State → MobX, Zustand
    ├── Many Small Independent States → Jotai, Recoil
    ├── Deeply Nested State → Immer-based solution
    └── Seldom-changing State → Almost any solution
```

### Deciding on State Location

```
Where should this piece of state live?
├── Is it used by only one component?
│   ├── YES → Use local component state
│   └── NO → Continue
│
├── Is it used by a few related components in the same subtree?
│   ├── YES → Use a common parent component or local Context
│   └── NO → Continue
│
├── Is it server data that needs caching and revalidation?
│   ├── YES → Use a server state manager (React Query, SWR, Apollo)
│   └── NO → Continue
│
├── Is it shareable via URL and should persist across page reloads?
│   ├── YES → Store in URL state
│   └── NO → Continue
│
├── Is it specific to a feature or module?
│   ├── YES → Use module-specific state management
│   └── NO → Continue
│
└── Is it truly global application state?
    ├── YES → Use global state management
    └── NO → Reconsider your state structure
```

### Structuring Global State

```
How should I structure my global state?
├── By Domain/Feature
│   ├── Pros: Modularity, team ownership, code splitting
│   ├── Cons: Potential duplication, cross-feature dependencies
│   └── Example: auth/, products/, cart/, checkout/
│
├── By State Category
│   ├── Pros: Clear separation of concerns
│   ├── Cons: Domain logic spread across files
│   └── Example: entities/, ui/, session/, errors/
│
├── By Data Type
│   ├── Pros: Consistent patterns for each data type
│   ├── Cons: Business domains split across files
│   └── Example: queries/, mutations/, subscriptions/
│
└── Normalized State
    ├── Pros: Eliminates duplication, reference integrity
    ├── Cons: More complex, requires normalization/denormalization
    └── Example: entities/{users, products, orders}, relationship tables
```

### Determining Update Patterns

```
How should state updates be handled?
├── Immutable Updates
│   ├── Use when tracking history or implementing undo/redo
│   ├── Libraries: Redux, Immer, Immutable.js
│   └── Techniques: Spread operators, map/filter/reduce
│
├── Reactive Updates
│   ├── Use when complex derived state is needed
│   ├── Libraries: MobX, Vue reactivity, RxJS
│   └── Techniques: Computed properties, observers, subscriptions
│
├── Action-Based Updates
│   ├── Use when traceability and predictability are priorities
│   ├── Libraries: Redux, NgRx, Vuex
│   └── Techniques: Action creators, reducers, middleware
│
├── Direct Mutation with Proxies
│   ├── Use when you want code simplicity but immutable benefits
│   ├── Libraries: Immer, Valtio
│   └── Techniques: Proxy objects that track changes
│
└── Hook-Based Updates
    ├── Use when component-centric state management is preferred
    ├── Libraries: Zustand, Jotai
    └── Techniques: Custom hooks with updater functions
```
</context>

<context name="state_management_anti_patterns" priority="medium">
## Anti-Patterns and Common Mistakes

### 1. Prop Drilling [AP-STATE-001]

**Problem:**
Passing state through multiple layers of components that don't need it, just to reach a deeply nested component that does.

**Example:**
```jsx
// Prop drilling through multiple components
function App() {
  const [user, setUser] = useState({ name: 'Alice' });
  
  return (
    <div>
      <Header user={user} />
    </div>
  );
}

function Header({ user }) {
  // Header doesn't use user but passes it down
  return (
    <nav>
      <NavigationMenu user={user} />
    </nav>
  );
}

function NavigationMenu({ user }) {
  // NavigationMenu doesn't use user either
  return (
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/about">About</a></li>
      <UserProfileLink user={user} />
    </ul>
  );
}

function UserProfileLink({ user }) {
  // Finally, this component uses the user prop
  return <li><a href="/profile">{user.name}'s Profile</a></li>;
}
```

**Why It Fails:**
- Creates tight coupling between unrelated components
- Makes code harder to maintain and refactor
- Increases complexity with each added layer
- Causes unnecessary re-renders when props change
- Makes component reusability difficult

**Better Approach:**
```jsx
// Using Context API instead of prop drilling
const UserContext = createContext();

function App() {
  const [user, setUser] = useState({ name: 'Alice' });
  
  return (
    <UserContext.Provider value={user}>
      <div>
        <Header />
      </div>
    </UserContext.Provider>
  );
}

function Header() {
  // No user prop needed
  return (
    <nav>
      <NavigationMenu />
    </nav>
  );
}

function NavigationMenu() {
  // No user prop needed
  return (
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/about">About</a></li>
      <UserProfileLink />
    </ul>
  );
}

function UserProfileLink() {
  // Get user directly from context
  const user = useContext(UserContext);
  return <li><a href="/profile">{user.name}'s Profile</a></li>;
}
```

**Severity:** Medium
**AI-Specific:** No

### 2. Monolithic State [AP-STATE-002]

**Problem:**
Using a single large state object that combines unrelated concerns, making updates complex and causing unnecessary re-renders.

**Example:**
```jsx
// One giant state object with mixed concerns
function App() {
  const [state, setState] = useState({
    user: { id: 1, name: 'Alice' },
    products: [],
    cart: [],
    ui: {
      isMenuOpen: false,
      activeTab: 'home',
      theme: 'light',
      notifications: []
    },
    form: {
      name: '',
      email: '',
      message: '',
      errors: {}
    },
    isLoading: false,
    error: null
  });
  
  // Update function becomes complex and error-prone
  const updateState = (path, value) => {
    const newState = {...state};
    const parts = path.split('.');
    let current = newState;
    
    for (let i = 0; i < parts.length - 1; i++) {
      current = current[parts[i]];
    }
    
    current[parts[parts.length - 1]] = value;
    setState(newState);
  };
  
  // All components re-render when any part of state changes
  return (
    <div>
      <UserProfile user={state.user} />
      <ProductList products={state.products} />
      <ShoppingCart cart={state.cart} />
      {/* More components... */}
    </div>
  );
}
```

**Why It Fails:**
- Performance issues from unnecessary re-renders
- Complex, error-prone state updates
- Tight coupling between unrelated state
- Difficult to understand and debug
- Harder to split code or implement code-splitting

**Better Approach:**
```jsx
// Split state by concern
function App() {
  // Separate state for different concerns
  const [user, setUser] = useState({ id: 1, name: 'Alice' });
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]);
  const [uiState, setUiState] = useState({
    isMenuOpen: false,
    activeTab: 'home',
    theme: 'light'
  });
  
  // Update functions are now simpler and focused
  const updateUiState = (key, value) => {
    setUiState({
      ...uiState,
      [key]: value
    });
  };
  
  return (
    <div>
      <UserProfile user={user} />
      <ProductList products={products} />
      <ShoppingCart cart={cart} />
      {/* More components... */}
    </div>
  );
}
```

**Severity:** High
**AI-Specific:** No

### 3. Direct State Mutation [AP-STATE-003]

**Problem:**
Modifying state objects directly instead of creating new copies, leading to unpredictable behavior and rendering issues.

**Example:**
```jsx
// Directly mutating state objects
function TodoList() {
  const [todos, setTodos] = useState([
    { id: 1, text: 'Learn React', completed: false }
  ]);
  
  const toggleTodo = (id) => {
    // ❌ Direct mutation
    const todo = todos.find(todo => todo.id === id);
    todo.completed = !todo.completed;
    setTodos(todos); // This won't trigger a re-render
  };
  
  const addTodo = (text) => {
    // ❌ Direct mutation
    todos.push({ id: Date.now(), text, completed: false });
    setTodos(todos); // This won't trigger a re-render correctly
  };
  
  return (
    /* Component rendering */
  );
}
```

**Why It Fails:**
- React may not detect state changes, resulting in missed renders
- Makes debugging difficult as original state is lost
- Breaks time-travel debugging
- Can lead to race conditions and unpredictable behavior
- Violates React's immutability principle

**Better Approach:**
```jsx
// Immutable state updates
function TodoList() {
  const [todos, setTodos] = useState([
    { id: 1, text: 'Learn React', completed: false }
  ]);
  
  const toggleTodo = (id) => {
    // ✅ Creating new array with updated item
    setTodos(todos.map(todo => 
      todo.id === id 
        ? { ...todo, completed: !todo.completed } 
        : todo
    ));
  };
  
  const addTodo = (text) => {
    // ✅ Creating new array
    setTodos([
      ...todos, 
      { id: Date.now(), text, completed: false }
    ]);
  };
  
  return (
    /* Component rendering */
  );
}
```

**Severity:** High
**AI-Specific:** Yes

### 4. Derived State as State [AP-STATE-004]

**Problem:**
Storing derived values as state rather than computing them on-the-fly, leading to synchronization issues and redundancy.

**Example:**
```jsx
// Storing derived state as state
function UserProfile() {
  const [user, setUser] = useState({
    firstName: 'John',
    lastName: 'Doe',
    birthYear: 1990
  });
  
  // ❌ Derived state stored as state
  const [fullName, setFullName] = useState(`${user.firstName} ${user.lastName}`);
  const [age, setAge] = useState(new Date().getFullYear() - user.birthYear);
  
  // This effect tries to keep derived state in sync
  useEffect(() => {
    setFullName(`${user.firstName} ${user.lastName}`);
    setAge(new Date().getFullYear() - user.birthYear);
  }, [user.firstName, user.lastName, user.birthYear]);
  
  const updateUser = (updates) => {
    setUser({ ...user, ...updates });
    // Forgetting to update derived state here would cause inconsistencies
  };
  
  return (
    <div>
      <h2>{fullName}</h2>
      <p>Age: {age}</p>
      {/* Form to update user */}
    </div>
  );
}
```

**Why It Fails:**
- Creates multiple sources of truth
- Requires synchronization code that can easily break
- Increases complexity unnecessarily
- Can lead to stale or inconsistent UI state
- Adds unnecessary re-renders

**Better Approach:**
```jsx
// Computing derived values on-the-fly
function UserProfile() {
  const [user, setUser] = useState({
    firstName: 'John',
    lastName: 'Doe',
    birthYear: 1990
  });
  
  // ✅ Derive values when needed
  const fullName = `${user.firstName} ${user.lastName}`;
  const age = new Date().getFullYear() - user.birthYear;
  
  const updateUser = (updates) => {
    setUser({ ...user, ...updates });
    // No need to worry about updating derived values
  };
  
  return (
    <div>
      <h2>{fullName}</h2>
      <p>Age: {age}</p>
      {/* Form to update user */}
    </div>
  );
}
```

**Severity:** Medium
**AI-Specific:** Yes

### 5. Over-Centralization [AP-STATE-005]

**Problem:**
Putting everything in global state even when it's only needed by a small part of the application, creating unnecessary complexity and dependencies.

**Example:**
```jsx
// Over-centralized state in Redux
// store/actions.js
export const TOGGLE_MENU = 'TOGGLE_MENU';
export const SET_FORM_FIELD = 'SET_FORM_FIELD';
export const FOCUS_INPUT = 'FOCUS_INPUT';
export const SET_SCROLL_POSITION = 'SET_SCROLL_POSITION';
// ...many more UI-specific actions

// store/reducer.js
function rootReducer(state = initialState, action) {
  switch (action.type) {
    case TOGGLE_MENU:
      return { ...state, isMenuOpen: !state.isMenuOpen };
    case SET_FORM_FIELD:
      return {
        ...state,
        forms: {
          ...state.forms,
          [action.formId]: {
            ...state.forms[action.formId],
            fields: {
              ...state.forms[action.formId].fields,
              [action.fieldId]: action.value
            }
          }
        }
      };
    case FOCUS_INPUT:
      return { ...state, focusedInput: action.inputId };
    case SET_SCROLL_POSITION:
      return { ...state, scrollPosition: action.position };
    // ...cases for many more UI-specific actions
    default:
      return state;
  }
}
```

**Why It Fails:**
- Bloats global state with component-specific concerns
- Creates tight coupling between unrelated components
- Makes the codebase harder to maintain
- Increases boilerplate for simple operations
- Leads to performance issues with unnecessary renders

**Better Approach:**
```jsx
// Hybrid approach with local and global state
// Global store only for truly shared state
// store/actions.js
export const LOGIN_USER = 'LOGIN_USER';
export const LOGOUT_USER = 'LOGOUT_USER';
export const ADD_TO_CART = 'ADD_TO_CART';
// ...only truly global actions

// Component with local state for UI concerns
function Menu() {
  // ✅ Local state for UI-specific concerns
  const [isOpen, setIsOpen] = useState(false);
  
  return (
    <div>
      <button onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? 'Close' : 'Open'} Menu
      </button>
      {isOpen && <MenuItems />}
    </div>
  );
}

// Component with form state
function ContactForm() {
  // ✅ Form library for form-specific state
  const { register, handleSubmit, formState } = useForm();
  
  const onSubmit = (data) => {
    // Use global actions only when needed
    dispatch(submitContactForm(data));
  };
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* Form fields */}
    </form>
  );
}
```

**Severity:** Medium
**AI-Specific:** No

### 6. Inconsistent Immutability [AP-STATE-006]

**Problem:**
Mixing immutable and mutable state update patterns, creating confusion and potential bugs when state doesn't update as expected.

**Example:**
```jsx
// Mixing mutable and immutable approaches
function ProductManager() {
  const [products, setProducts] = useState([
    { id: 1, name: 'Laptop', price: 999, tags: ['electronics', 'computers'] }
  ]);
  
  const updatePrice = (productId, newPrice) => {
    // Immutable approach
    setProducts(products.map(product => 
      product.id === productId 
        ? { ...product, price: newPrice } 
        : product
    ));
  };
  
  const addTag = (productId, tag) => {
    // Find the product to update
    const product = products.find(p => p.id === productId);
    
    // ❌ Mutable approach mixed with immutable
    product.tags.push(tag); // Direct mutation
    
    // This creates a new array of products but with the same
    // mutated product object inside
    setProducts([...products]);
  };
  
  // Rest of component
}
```

**Why It Fails:**
- Creates confusing code with inconsistent patterns
- Can lead to subtle bugs when updates don't work as expected
- Makes code harder to reason about
- May break optimizations based on reference equality
- Complicates debugging

**Better Approach:**
```jsx
// Consistent immutable pattern
function ProductManager() {
  const [products, setProducts] = useState([
    { id: 1, name: 'Laptop', price: 999, tags: ['electronics', 'computers'] }
  ]);
  
  const updatePrice = (productId, newPrice) => {
    // Immutable approach
    setProducts(products.map(product => 
      product.id === productId 
        ? { ...product, price: newPrice } 
        : product
    ));
  };
  
  const addTag = (productId, tag) => {
    // ✅ Consistent immutable approach for nested updates
    setProducts(products.map(product => 
      product.id === productId 
        ? { 
            ...product, 
            tags: [...product.tags, tag] // New array for tags
          } 
        : product
    ));
  };
  
  // Or using Immer for a more consistent approach to nested updates
  const addTagWithImmer = (productId, tag) => {
    updateProducts(draft => {
      const product = draft.find(p => p.id === productId);
      if (product) {
        product.tags.push(tag); // Looks mutable but Immer handles immutability
      }
    });
  };
  
  // Rest of component
}
```

**Severity:** Medium
**AI-Specific:** Yes
</context>

<context name="state_management_reasoning_principles" priority="low">
## Reasoning Principles

### Complexity vs. Simplicity Tradeoffs

When choosing a state management approach, there's always a tradeoff between simplicity and power:

1. **Simple Solutions (Local State, Context)**
   - Benefits: Lower learning curve, less boilerplate, faster development
   - Costs: Limited scalability, potential performance issues, fewer built-in features
   - Reasoning: Use when the application is small or medium-sized with simple state requirements

2. **Complex Solutions (Redux, MobX, NgRx)**
   - Benefits: Better scalability, powerful features, strong conventions
   - Costs: Steeper learning curve, more boilerplate, slower initial development
   - Reasoning: Use when the application is large or has complex state requirements

The key principle is to match the complexity of your solution to the complexity of your problem. Adding unnecessary complexity is as problematic as using an overly simplistic approach for complex needs.

### Performance Considerations

State management choices significantly impact application performance:

1. **Granularity Principle**
   - Fine-grained state: Better for frequent updates to small pieces of state
   - Coarse-grained state: Better for infrequent updates to large pieces of state
   - Reasoning: The granularity of your state should match the update patterns of your application

2. **Rendering Optimization**
   - State changes trigger re-renders in affected components
   - Localized state minimizes unnecessary re-renders
   - Global state can cause cascading re-renders
   - Reasoning: Structure state to minimize the scope of re-renders

3. **Computation Timing**
   - Eager computation: Calculate derived values immediately when state changes
   - Lazy computation: Calculate derived values only when needed
   - Reasoning: Choose based on usage frequency and computation cost

### Consistency vs. Convenience

Different state management approaches offer different balances of consistency and convenience:

1. **Strict Immutability (Redux)**
   - Benefits: Predictable updates, time-travel debugging, clear data flow
   - Costs: More boilerplate, steeper learning curve
   - Reasoning: Prefer when correctness and predictability are critical

2. **Managed Mutability (MobX, Vue)**
   - Benefits: More intuitive API, less boilerplate, feels like "normal" JavaScript
   - Costs: Potentially less predictable, magic under the hood
   - Reasoning: Prefer when developer experience and productivity are priorities

3. **Proxied Immutability (Immer)**
   - Benefits: Immutable guarantees with mutable syntax
   - Costs: Additional abstraction layer
   - Reasoning: Good compromise when you want both convenience and immutability

### Coupling and Cohesion

State management significantly affects application architecture through coupling and cohesion:

1. **Tight Coupling**
   - Global state often increases coupling between components
   - Makes components less reusable and harder to test
   - Reasoning: Use more isolated state for better component reusability

2. **Loose Coupling**
   - Context boundaries and module-specific state create natural isolation
   - Enables better code splitting and parallel development
   - Reasoning: Design state boundaries that match your application's domain boundaries

3. **Cohesion Principle**
   - Related state should be managed together
   - Unrelated state should be managed separately
   - Reasoning: Group state by domain concerns rather than technical concerns

### State Categorization

Effective state management requires understanding the nature of your state:

1. **Persistence Categories**
   - Transient: Exists only during the current session or interaction
   - Persistent: Survives page reloads or app restarts
   - Reasoning: Persistent state needs storage strategies (localStorage, cookies, server)

2. **Scope Categories**
   - Component-local: Affects only one component
   - Feature-scoped: Affects a group of related components
   - Application-global: Affects the entire application
   - Reasoning: Match the state's scope to its management method

3. **Ownership Categories**
   - Client-owned: Originates and is controlled by the frontend
   - Server-owned: Originates and is controlled by the backend
   - Shared: Controlled by both client and server
   - Reasoning: Server-owned state requires different synchronization patterns
</context>

<context name="state_management_model_specific_notes" priority="low">
## Model-Specific Implementation Notes

### For Claude (Anthropic)

When working with state management through Claude, consider these approaches:

- Claude excels at explaining conceptual models and principles, so focus on understanding the fundamental patterns rather than specific library implementations
- When asking Claude to generate state management code, be explicit about which pattern or library you want to use
- Provide context about your application's size, complexity, and specific requirements to get tailored recommendations
- Ask Claude to explain tradeoffs between different approaches rather than just implementing a solution

Example prompt:
```
I'm building a React application with around 20 components that needs to manage user authentication, product data from an API, and UI state like filters and sorting. Could you help me decide between Context API, Redux, and React Query for my state management needs? Please explain the tradeoffs and recommend a combined approach.
```

### For GPT (OpenAI)

When working with state management through GPT models, consider:

- GPT models often provide more code-heavy responses with specific implementations
- Specify the exact version of libraries you're using to get compatible code
- Ask for complete working examples rather than snippets
- Request explanations of the generated code to ensure understanding
- Have GPT evaluate potential performance implications of different approaches

Example prompt:
```
I need to implement a global state management solution for my React application using Redux Toolkit 1.9. Please show me a complete example of setting up a store with multiple slices for users, products, and cart features. Include examples of async thunks for API calls and explain how to connect the store to components.
```

### For Cursor AI

When working with state management through Cursor AI, consider:

- Cursor AI is optimized for code completion and editing
- Provide partial implementations and ask for improvements or extensions
- Use comments to indicate specific parts you want help with
- Focus on specific functions or features rather than entire implementations
- Use Cursor AI to refactor existing state management code

Example prompt:
```
// I have this Redux reducer for my products state, but I need to add support
// for filtering and sorting products. Please extend this implementation.

const initialState = {
  items: [],
  isLoading: false,
  error: null
};

export const productsReducer = (state = initialState, action) => {
  switch (action.type) {
    case 'FETCH_PRODUCTS_REQUEST':
      return { ...state, isLoading: true };
    case 'FETCH_PRODUCTS_SUCCESS':
      return { ...state, items: action.payload, isLoading: false };
    case 'FETCH_PRODUCTS_FAILURE':
      return { ...state, error: action.payload, isLoading: false };
    default:
      return state;
  }
};
```

### For Local Models

When working with state management through local code models:

- Local models may have limitations in understanding complex state management patterns
- Break down complex state management requests into smaller, more focused tasks
- Provide more context about the specific libraries and patterns you're using
- Focus on basic patterns rather than advanced optimizations
- Verify generated code more carefully, especially for performance implications

Example prompt:
```
I'm using React with useState and useContext hooks for state management. Please show me a simple implementation of a theme context that allows switching between light and dark modes. Include both the context creation and a custom hook for consuming the theme.
```
</context>

<context name="state_management_related_concepts" priority="low">
## Related Concepts

- **Immutability** - The principle of not modifying data once created, but instead creating new copies with changes, which is fundamental to many state management approaches.

- **Pure Functions** - Functions that always produce the same output for the same input and have no side effects, used heavily in reducer patterns and functional state updates.

- **Unidirectional Data Flow** - The architectural pattern where data changes flow in a single direction, providing predictability and easier debugging.

- **Memoization** - Optimization technique for caching results of expensive function calls, commonly used with selectors in state management.

- **Normalization** - Technique for structuring complex state to avoid duplication and maintain relationships, similar to database normalization.

- **Side Effects** - Operations that affect something outside the scope of the current function, like API calls or localStorage updates, which need special handling in state management.

- **Time-Travel Debugging** - Ability to move back and forth between previous states, enabled by immutable state management approaches like Redux.

- **Reactive Programming** - Programming paradigm oriented around data streams and the propagation of changes, used in libraries like RxJS and MobX.

- **Event Sourcing** - Pattern where state changes are stored as a sequence of events, which can be replayed to reconstruct the state.

- **CQRS (Command Query Responsibility Segregation)** - Pattern that separates read and write operations for data, often used in complex state management systems.

- **Actor Model** - Concurrency model where "actors" are the universal primitives of computation that respond to messages, influencing some state management approaches.

- **Finite State Machines** - Mathematical model of computation that can be in exactly one of a finite number of states at any given time, useful for managing complex UI states.

- **Observable Pattern** - Design pattern where an object maintains a list of dependents and notifies them of state changes, foundational for reactive state management.

- **Proxy Pattern** - Design pattern that provides a surrogate or placeholder for another object to control access to it, used in state management libraries like Immer and Vue.

- **Flux Architecture** - Application architecture pattern for building user interfaces, which influenced libraries like Redux.
</context>

<context name="state_management_practical_examples" priority="medium">
## Practical Examples

### Example 1: Form State Management

**Before**: Unstructured form state with synchronization issues.

```jsx
function RegistrationForm() {
  // Multiple state variables for form fields
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  
  // Separate state for validation
  const [usernameError, setUsernameError] = useState('');
  const [emailError, setEmailError] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [confirmPasswordError, setConfirmPasswordError] = useState('');
  
  // Validation functions that need to be called separately
  const validateUsername = () => {
    if (username.length < 3) {
      setUsernameError('Username must be at least 3 characters');
      return false;
    } else {
      setUsernameError('');
      return true;
    }
  };
  
  const validateEmail = () => {
    if (!email.includes('@')) {
      setEmailError('Invalid email address');
      return false;
    } else {
      setEmailError('');
      return true;
    }
  };
  
  // More validation functions...
  
  // Submit handler has to call all validation functions
  const handleSubmit = (e) => {
    e.preventDefault();
    
    const isUsernameValid = validateUsername();
    const isEmailValid = validateEmail();
    // More validation calls...
    
    if (isUsernameValid && isEmailValid && /* other validations */) {
      // Submit form
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Username:</label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          onBlur={validateUsername}
        />
        {usernameError && <p className="error">{usernameError}</p>}
      </div>
      
      <div>
        <label>Email:</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          onBlur={validateEmail}
        />
        {emailError && <p className="error">{emailError}</p>}
      </div>
      
      {/* More form fields... */}
      
      <button type="submit">Register</button>
    </form>
  );
}
```

**After**: Structured form state using a form library (React Hook Form).

```jsx
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';

// Define validation schema
const schema = yup.object().shape({
  username: yup
    .string()
    .min(3, 'Username must be at least 3 characters')
    .required('Username is required'),
  email: yup
    .string()
    .email('Invalid email address')
    .required('Email is required'),
  password: yup
    .string()
    .min(8, 'Password must be at least 8 characters')
    .matches(
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, 
      'Password must contain at least one uppercase letter, one lowercase letter, and one number'
    )
    .required('Password is required'),
  confirmPassword: yup
    .string()
    .oneOf([yup.ref('password'), null], 'Passwords must match')
    .required('Please confirm your password')
});

function RegistrationForm() {
  // Form state managed by React Hook Form
  const { 
    register, 
    handleSubmit, 
    formState: { errors, isSubmitting },
    watch
  } = useForm({
    resolver: yupResolver(schema),
    mode: 'onBlur'
  });
  
  // Form submission handler
  const onSubmit = async (data) => {
    try {
      // Submit form data
      await submitRegistration(data);
      // Handle successful registration
    } catch (error) {
      // Handle submission error
    }
  };
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label>Username:</label>
        <input {...register('username')} />
        {errors.username && (
          <p className="error">{errors.username.message}</p>
        )}
      </div>
      
      <div>
        <label>Email:</label>
        <input {...register('email')} />
        {errors.email && (
          <p className="error">{errors.email.message}</p>
        )}
      </div>
      
      <div>
        <label>Password:</label>
        <input type="password" {...register('password')} />
        {errors.password && (
          <p className="error">{errors.password.message}</p>
        )}
      </div>
      
      <div>
        <label>Confirm Password:</label>
        <input type="password" {...register('confirmPassword')} />
        {errors.confirmPassword && (
          <p className="error">{errors.confirmPassword.message}</p>
        )}
      </div>
      
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Registering...' : 'Register'}
      </button>
    </form>
  );
}
```

Key improvements:
- Centralized form state management
- Declarative validation with schema
- Automatic error handling and display
- Less code with better organization
- Built-in form submission state
- Better performance with optimized re-renders

### Example 2: Global Application State

**Before**: Mixed component state and context with poor organization.

```jsx
// Multiple contexts with overlapping concerns
const ThemeContext = createContext();
const AuthContext = createContext();
const CartContext = createContext();
const NotificationContext = createContext();

function App() {
  // Duplicated state management logic in App component
  const [theme, setTheme] = useState('light');
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [cart, setCart] = useState([]);
  const [notifications, setNotifications] = useState([]);

  // Authentication functions defined directly in component
  const login = async (credentials) => {
    try {
      const user = await loginApi(credentials);
      setUser(user);
      setIsAuthenticated(true);
      addNotification('Login successful');
    } catch (error) {
      addNotification(`Login failed: ${error.message}`, 'error');
    }
  };

  const logout = () => {
    setUser(null);
    setIsAuthenticated(false);
    addNotification('Logged out successfully');
  };

  // Cart functions
  const addToCart = (product) => {
    const existingItem = cart.find(item => item.id === product.id);
    
    if (existingItem) {
      setCart(cart.map(item => 
        item.id === product.id 
          ? { ...item, quantity: item.quantity + 1 } 
          : item
      ));
    } else {
      setCart([...cart, { ...product, quantity: 1 }]);
    }
    
    addNotification(`Added ${product.name} to cart`);
  };

  // Notification functions
  const addNotification = (message, type = 'info') => {
    const id = Date.now();
    setNotifications([
      ...notifications, 
      { id, message, type }
    ]);
    
    // Auto-remove notification after 3 seconds
    setTimeout(() => {
      removeNotification(id);
    }, 3000);
  };

  const removeNotification = (id) => {
    setNotifications(notifications.filter(
      notification => notification.id !== id
    ));
  };

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      <AuthContext.Provider value={{ user, isAuthenticated, login, logout }}>
        <CartContext.Provider value={{ cart, addToCart, setCart }}>
          <NotificationContext.Provider 
            value={{ notifications, addNotification, removeNotification }}
          >
            {/* App components */}
          </NotificationContext.Provider>
        </CartContext.Provider>
      </AuthContext.Provider>
    </ThemeContext.Provider>
  );
}
```

**After**: Structured global state with Redux Toolkit.

```jsx
// store/index.js
import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice';
import cartReducer from './cartSlice';
import uiReducer from './uiSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    cart: cartReducer,
    ui: uiReducer
  }
});

// store/authSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { loginApi } from '../api/auth';
import { addNotification } from './uiSlice';

export const loginUser = createAsyncThunk(
  'auth/login',
  async (credentials, { dispatch, rejectWithValue }) => {
    try {
      const user = await loginApi(credentials);
      dispatch(addNotification({ 
        message: 'Login successful', 
        type: 'success' 
      }));
      return user;
    } catch (error) {
      dispatch(addNotification({ 
        message: `Login failed: ${error.message}`, 
        type: 'error' 
      }));
      return rejectWithValue(error.message);
    }
  }
);

const authSlice = createSlice({
  name: 'auth',
  initialState: {
    user: null,
    isAuthenticated: false,
    status: 'idle', // 'idle' | 'loading' | 'succeeded' | 'failed'
    error: null
  },
  reducers: {
    logoutUser: (state) => {
      state.user = null;
      state.isAuthenticated = false;
      state.status = 'idle';
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(loginUser.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.user = action.payload;
        state.isAuthenticated = true;
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.payload;
      });
  }
});

export const { logoutUser } = authSlice.actions;
export default authSlice.reducer;

// store/cartSlice.js
import { createSlice } from '@reduxjs/toolkit';
import { addNotification } from './uiSlice';

const cartSlice = createSlice({
  name: 'cart',
  initialState: {
    items: []
  },
  reducers: {
    addItem: (state, action) => {
      const product = action.payload;
      const existingItemIndex = state.items.findIndex(
        item => item.id === product.id
      );
      
      if (existingItemIndex >= 0) {
        state.items[existingItemIndex].quantity += 1;
      } else {
        state.items.push({ ...product, quantity: 1 });
      }
    },
    removeItem: (state, action) => {
      state.items = state.items.filter(
        item => item.id !== action.payload
      );
    },
    clearCart: (state) => {
      state.items = [];
    }
  }
});

// Thunk to add to cart with notification
export const addToCartWithNotification = (product) => (dispatch) => {
  dispatch(addItem(product));
  dispatch(addNotification({
    message: `Added ${product.name} to cart`,
    type: 'info'
  }));
};

export const { addItem, removeItem, clearCart } = cartSlice.actions;
export default cartSlice.reducer;

// store/uiSlice.js
import { createSlice } from '@reduxjs/toolkit';

const uiSlice = createSlice({
  name: 'ui',
  initialState: {
    theme: 'light',
    notifications: []
  },
  reducers: {
    setTheme: (state, action) => {
      state.theme = action.payload;
    },
    addNotification: (state, action) => {
      const notification = {
        id: Date.now(),
        message: action.payload.message,
        type: action.payload.type || 'info'
      };
      state.notifications.push(notification);
    },
    removeNotification: (state, action) => {
      state.notifications = state.notifications.filter(
        notification => notification.id !== action.payload
      );
    }
  }
});

// Thunk to add auto-dismissing notification
export const addTimedNotification = (notification) => (dispatch) => {
  dispatch(addNotification(notification));
  
  setTimeout(() => {
    dispatch(removeNotification(notification.id));
  }, 3000);
};

export const { setTheme, addNotification, removeNotification } = uiSlice.actions;
export default uiSlice.reducer;

// App.js
import { Provider } from 'react-redux';
import { store } from './store';

function App() {
  return (
    <Provider store={store}>
      {/* App components */}
    </Provider>
  );
}

// Using in components
import { useDispatch, useSelector } from 'react-redux';
import { loginUser, logoutUser } from './store/authSlice';
import { addToCartWithNotification } from './store/cartSlice';
import { setTheme } from './store/uiSlice';

function LoginComponent() {
  const dispatch = useDispatch();
  const { status, error } = useSelector(state => state.auth);
  
  const handleLogin = (credentials) => {
    dispatch(loginUser(credentials));
  };
  
  // Component JSX
}

function ThemeToggle() {
  const dispatch = useDispatch();
  const theme = useSelector(state => state.ui.theme);
  
  const toggleTheme = () => {
    dispatch(setTheme(theme === 'light' ? 'dark' : 'light'));
  };
  
  // Component JSX
}
```

Key improvements:
- Properly organized state by domain
- Clear separation of concerns
- Centralized business logic
- Predictable state updates with reducers
- Middleware for side effects (thunks)
- Easier debugging with Redux DevTools
- Better code organization and maintainability
- Strong conventions for state updates

### Example 3: Server State Management

**Before**: Manual server state management with loading, error, and cache handling.

```jsx
function ProductList() {
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lastFetched, setLastFetched] = useState(null);
  
  const fetchProducts = async () => {
    // Don't fetch if data is fresh (less than 5 minutes old)
    if (lastFetched && Date.now() - lastFetched < 5 * 60 * 1000) {
      return;
    }
    
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/products');
      
      if (!response.ok) {
        throw new Error('Failed to fetch products');
      }
      
      const data = await response.json();
      setProducts(data);
      setLastFetched(Date.now());
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Fetch on mount
  useEffect(() => {
    fetchProducts();
  }, []);
  
  // Manual refresh function
  const handleRefresh = () => {
    // Force refresh by ignoring cache
    setLastFetched(null);
    fetchProducts();
  };
  
  if (isLoading && products.length === 0) {
    return <div>Loading...</div>;
  }
  
  if (error && products.length === 0) {
    return (
      <div>
        <p>Error: {error}</p>
        <button onClick={handleRefresh}>Retry</button>
      </div>
    );
  }
  
  return (
    <div>
      <button onClick={handleRefresh}>
        {isLoading ? 'Refreshing...' : 'Refresh'}
      </button>
      
      {isLoading && <p>Updating...</p>}
      
      <ul>
        {products.map(product => (
          <li key={product.id}>{product.name} - ${product.price}</li>
        ))}
      </ul>
    </div>
  );
}
```

**After**: Using React Query for efficient server state management.

```jsx
import { useQuery, useMutation, useQueryClient } from 'react-query';

// API functions
const fetchProducts = async () => {
  const response = await fetch('/api/products');
  if (!response.ok) {
    throw new Error('Failed to fetch products');
  }
  return response.json();
};

const addProduct = async (newProduct) => {
  const response = await fetch('/api/products', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(newProduct),
  });
  
  if (!response.ok) {
    throw new Error('Failed to add product');
  }
  
  return response.json();
};

function ProductList() {
  const queryClient = useQueryClient();
  
  // Query for fetching products
  const {
    data: products = [],
    isLoading,
    isError,
    error,
    refetch,
    isFetching,
  } = useQuery('products', fetchProducts, {
    staleTime: 5 * 60 * 1000, // 5 minutes
    refetchOnWindowFocus: true,
    refetchOnMount: true,
    refetchOnReconnect: true,
  });
  
  // Mutation for adding a new product
  const addProductMutation = useMutation(addProduct, {
    onSuccess: () => {
      // Invalidate and refetch the products query
      queryClient.invalidateQueries('products');
    },
  });
  
  const handleAddProduct = (productData) => {
    addProductMutation.mutate(productData);
  };
  
  if (isLoading) {
    return <div>Loading...</div>;
  }
  
  if (isError) {
    return (
      <div>
        <p>Error: {error.message}</p>
        <button onClick={refetch}>Retry</button>
      </div>
    );
  }
  
  return (
    <div>
      <button 
        onClick={refetch} 
        disabled={isFetching}
      >
        {isFetching ? 'Refreshing...' : 'Refresh'}
      </button>
      
      {isFetching && <p>Updating...</p>}
      
      <ul>
        {products.map(product => (
          <li key={product.id}>{product.name} - ${product.price}</li>
        ))}
      </ul>
      
      <button
        onClick={() => handleAddProduct({ name: 'New Product', price: 9.99 })}
        disabled={addProductMutation.isLoading}
      >
        {addProductMutation.isLoading ? 'Adding...' : 'Add Product'}
      </button>
      
      {addProductMutation.isError && (
        <p>Error adding product: {addProductMutation.error.message}</p>
      )}
    </div>
  );
}
```

Key improvements:
- Automatic caching and stale data handling
- Background refetching with loading states
- Automatic retry on failure
- Optimistic updates for mutations
- Deduplication of requests
- Query invalidation
- Loading and error states for both queries and mutations
- Cache normalization and relationship handling
- Simpler component code with more sophisticated data handling

