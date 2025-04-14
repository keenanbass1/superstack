
3. Logs response status code when complete
4. Anonymizes any sensitive data in the logs (auth tokens, passwords)
5. Includes a configurable log level
</context>

<context name="existing_code" priority="medium">
Here's our current logger setup:
```typescript
// src/utils/logger.ts
import winston from 'winston';

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'app.log' })
  ]
});

export default logger;
```
</context>

Please implement the middleware following our project standards.
```

### For Smaller/Local Models

Open-source and locally deployable models (e.g., LLaMA, Mistral, CodeLLaMA) often have different characteristics.

**Strengths:**
- No data sharing/privacy concerns for sensitive code
- Often optimized specifically for code generation
- Can be fine-tuned for specific domains or codebases
- Lower latency for locally deployed models
- Full control over model parameters

**Limitations:**
- Generally lower capabilities than leading commercial models
- Smaller context windows in most cases
- Less up-to-date knowledge on recent libraries and frameworks
- May require more explicit guidance and context

**Best Practices:**
- Break problems into smaller, more manageable chunks
- Provide more detailed context and examples
- Lower expectations for complex architectural guidance
- Focus on standard patterns and libraries
- Be more explicit about desired coding patterns and styles

**Example Effective Patterns:**
```
"I'll show you an example of how we handle API errors in our codebase, then
ask you to implement a similar pattern for a new endpoint.

Here's our standard error handling:
```javascript
try {
  const result = await dataService.performOperation(data);
  return res.status(200).json({ success: true, data: result });
} catch (error) {
  if (error instanceof ValidationError) {
    return res.status(400).json({ 
      success: false, 
      error: error.message,
      details: error.details 
    });
  }
  
  if (error instanceof NotFoundError) {
    return res.status(404).json({ 
      success: false, 
      error: error.message 
    });
  }
  
  logger.error('Operation failed', { error });
  return res.status(500).json({ 
    success: false, 
    error: 'Internal server error' 
  });
}
```

Now, please implement the DELETE /api/products/:id endpoint following this
same error handling pattern. The endpoint should call productService.deleteProduct(id)
which might throw ValidationError, NotFoundError, or AuthorizationError (status 403)."
```

### Cross-Model Recommendations

Regardless of which AI coding assistant you're using, these general recommendations apply:

1. **Start with high-quality prompts**
   - Be specific about requirements and constraints
   - Include necessary context (language, framework, versions)
   - Specify coding standards and patterns to follow

2. **Always review and test generated code**
   - Don't assume correctness, even from confident-sounding responses
   - Check for security issues, edge cases, and performance concerns
   - Run automated tests and linters on generated code

3. **Use iterative development**
   - Start with a basic implementation and refine gradually
   - Break complex tasks into smaller, manageable chunks
   - Build feedback loops to improve the model's understanding

4. **Combine strengths of different tools**
   - Use chat-based models for exploration and explanation
   - Use IDE-integrated tools for implementation and refactoring
   - Leverage specialized tools for their particular strengths

5. **Document AI-assisted processes**
   - Keep records of significant AI contributions to codebase
   - Document any assumptions or limitations in AI-generated code
   - Create organizational guidelines for AI coding assistance

By understanding the specific characteristics of different AI coding assistants, developers can choose the right tool for each task and optimize their interaction patterns accordingly.
</context>

<context name="practical_examples" priority="medium">
## Practical Examples

The following examples demonstrate effective AI collaboration strategies with before/after comparisons.

### Example 1: Converting Pseudocode to Implementation

**Before: Vague Request**
```
"Write code to implement a cache for API responses."
```

**Generated Code (Problematic)**
```javascript
// Simple cache implementation without clear design decisions
const cache = {};

function cacheResponse(url, data) {
  cache[url] = {
    data: data,
    timestamp: Date.now()
  };
}

function getCachedResponse(url) {
  if (cache[url]) {
    return cache[url].data;
  }
  return null;
}

// No expiration, no size limits, no error handling, race conditions...
```

**After: Structured Pseudocode-to-Implementation Approach**
```
"I need to implement an API response cache with the following pseudocode:

```
class ApiCache:
  Initialize with maximum size and default TTL
  
  function set(key, value):
    If cache at max size:
      Remove oldest entry
    Store value with timestamp and TTL
    
  function get(key):
    If key exists in cache:
      If entry has expired:
        Remove entry
        Return null
      Else:
        Update access time
        Return value
    Else:
      Return null
      
  function invalidate(key):
    Remove key from cache if exists
    
  function clear():
    Empty the entire cache
```

Please implement this in TypeScript with:
- Generics for type-safe values
- LRU eviction instead of simple 'oldest entry' removal
- Proper error handling
- Unit tests for the core functionality
"
```

**Generated Code (Improved)**
```typescript
/**
 * Type-safe API response cache with LRU eviction policy
 */
export class ApiCache<T = any> {
  private cache: Map<string, CacheEntry<T>> = new Map();
  private accessOrder: string[] = [];
  
  /**
   * Create a new cache instance
   * @param maxSize Maximum number of entries to store (default: 100)
   * @param defaultTtl Default time-to-live in milliseconds (default: 5 minutes)
   */
  constructor(
    private readonly maxSize: number = 100,
    private readonly defaultTtl: number = 5 * 60 * 1000
  ) {}
  
  /**
   * Store a value in the cache
   * @param key Cache key
   * @param value Value to store
   * @param ttl Optional custom TTL for this entry
   * @throws Error if key or value is invalid
   */
  public set(key: string, value: T, ttl?: number): void {
    if (!key) {
      throw new Error('Cache key cannot be empty');
    }
    
    // If we're at max capacity and this is a new key, remove oldest entry
    if (this.cache.size >= this.maxSize && !this.cache.has(key)) {
      this.evictOldest();
    }
    
    // Update access order (remove + add to end = most recently used)
    this.updateAccessOrder(key);
    
    // Store the entry
    this.cache.set(key, {
      value,
      timestamp: Date.now(),
      ttl: ttl ?? this.defaultTtl,
    });
  }
  
  /**
   * Retrieve a value from the cache
   * @param key Cache key
   * @returns The cached value or null if not found or expired
   */
  public get(key: string): T | null {
    const entry = this.cache.get(key);
    
    if (!entry) {
      return null;
    }
    
    // Check if entry has expired
    if (this.isExpired(entry)) {
      this.invalidate(key);
      return null;
    }
    
    // Update access order since entry was accessed
    this.updateAccessOrder(key);
    
    return entry.value;
  }
  
  /**
   * Remove an item from the cache
   * @param key Cache key to invalidate
   * @returns True if entry was found and removed, false otherwise
   */
  public invalidate(key: string): boolean {
    // Remove from access order
    const index = this.accessOrder.indexOf(key);
    if (index !== -1) {
      this.accessOrder.splice(index, 1);
    }
    
    // Remove from cache
    return this.cache.delete(key);
  }
  
  /**
   * Clear all cache entries
   */
  public clear(): void {
    this.cache.clear();
    this.accessOrder = [];
  }
  
  /**
   * Get the number of entries in the cache
   */
  public get size(): number {
    return this.cache.size;
  }
  
  /**
   * Check if a cache entry has expired
   */
  private isExpired(entry: CacheEntry<T>): boolean {
    return Date.now() - entry.timestamp > entry.ttl;
  }
  
  /**
   * Update the access order for LRU tracking
   */
  private updateAccessOrder(key: string): void {
    // Remove from current position if it exists
    const index = this.accessOrder.indexOf(key);
    if (index !== -1) {
      this.accessOrder.splice(index, 1);
    }
    
    // Add to end (most recently used)
    this.accessOrder.push(key);
  }
  
  /**
   * Evict the least recently used item
   */
  private evictOldest(): void {
    if (this.accessOrder.length === 0) {
      return;
    }
    
    // Get the least recently used key (first in the array)
    const oldestKey = this.accessOrder.shift()!;
    this.cache.delete(oldestKey);
  }
}

/**
 * Cache entry structure
 */
interface CacheEntry<T> {
  value: T;
  timestamp: number;
  ttl: number;
}

// Unit tests
describe('ApiCache', () => {
  test('should store and retrieve values', () => {
    const cache = new ApiCache<string>();
    cache.set('key1', 'value1');
    expect(cache.get('key1')).toBe('value1');
    expect(cache.get('nonexistent')).toBeNull();
  });
  
  test('should respect TTL settings', async () => {
    const cache = new ApiCache<string>(10, 50); // 50ms TTL
    cache.set('key1', 'value1');
    expect(cache.get('key1')).toBe('value1');
    
    // Wait for TTL to expire
    await new Promise(resolve => setTimeout(resolve, 60));
    expect(cache.get('key1')).toBeNull();
  });
  
  test('should evict least recently used items when at capacity', () => {
    const cache = new ApiCache<string>(2); // Only 2 items
    
    cache.set('key1', 'value1');
    cache.set('key2', 'value2');
    expect(cache.size).toBe(2);
    
    // Access key1 to make it most recently used
    cache.get('key1');
    
    // Add a third item, should evict key2 (least recently used)
    cache.set('key3', 'value3');
    expect(cache.size).toBe(2);
    expect(cache.get('key1')).toBe('value1'); // Still there
    expect(cache.get('key2')).toBeNull(); // Evicted
    expect(cache.get('key3')).toBe('value3'); // Added
  });
});
```

**Key Improvements:**
- Detailed pseudocode provided clear intent and structure
- Requested specific improvements over the basic algorithm
- Specific type system and error handling requirements
- Requested unit tests to verify behavior
- Resulting code is more robust, type-safe, and well-tested

### Example 2: Iterative Refinement for Security

**Before: Security-Naive Request**
```
"Create a user authentication API with login and registration in Node.js and Express."
```

**Generated Code (Vulnerable)**
```javascript
const express = require('express');
const router = express.Router();
const User = require('../models/User');

// User registration
router.post('/register', async (req, res) => {
  const { username, password, email } = req.body;
  
  // Create new user
  const newUser = new User({
    username,
    password, // Storing plaintext password!
    email
  });
  
  try {
    const savedUser = await newUser.save();
    res.status(201).json(savedUser);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// User login
router.post('/login', async (req, res) => {
  const { username, password } = req.body;
  
  try {
    const user = await User.findOne({ username });
    if (!user) return res.status(400).json({ error: 'User not found' });
    
    // Insecure direct password comparison
    if (user.password !== password) {
      return res.status(400).json({ error: 'Invalid password' });
    }
    
    // No token creation, session management, or security headers
    res.json({ message: 'Login successful', user });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
```

**After: Iterative Security-Focused Refinement**
```
"I need to create a user authentication API with Node.js, Express, and MongoDB.

First, let's focus on the user model with proper password security."
```

**Response with Initial Model**
```javascript
// models/User.js
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const userSchema = new mongoose.Schema({
  username: {
    type: String,
    required: [true, 'Username is required'],
    unique: true,
    trim: true,
    minlength: 3,
    maxlength: 30
  },
  email: {
    type: String,
    required: [true, 'Email is required'],
    unique: true,
    trim: true,
    lowercase: true,
    match: [/^\S+@\S+\.\S+$/, 'Please enter a valid email']
  },
  password: {
    type: String,
    required: [true, 'Password is required'],
    minlength: 8
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

// Pre-save hook to hash password
userSchema.pre('save', async function(next) {
  // Only hash the password if it's modified (or new)
  if (!this.isModified('password')) return next();
  
  try {
    // Generate a salt
    const salt = await bcrypt.genSalt(10);
    // Hash the password along with the new salt
    this.password = await bcrypt.hash(this.password, salt);
    next();
  } catch (error) {
    next(error);
  }
});

// Method to compare passwords
userSchema.methods.comparePassword = async function(candidatePassword) {
  return bcrypt.compare(candidatePassword, this.password);
};

const User = mongoose.model('User', userSchema);
module.exports = User;
```

**Following Up on Authentication Logic**
```
"Great start with the User model. Now, let's implement the authentication 
controller with proper security measures including:
1. JWT token generation and validation
2. Rate limiting for login attempts
3. Secure HTTP headers
4. Input validation
5. CSRF protection"
```

**Generated Secure Authentication Controller**
```javascript
// controllers/authController.js
const User = require('../models/User');
const jwt = require('jsonwebtoken');
const { body, validationResult } = require('express-validator');
const rateLimit = require('express-rate-limit');

// Environment variables should be set in .env file
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key'; // Change in production
const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN || '1h';

// Create rate limiter for login attempts
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 login attempts per window per IP
  message: { error: 'Too many login attempts, please try again later' },
  standardHeaders: true,
  legacyHeaders: false,
});

// Input validation rules
exports.validateRegistration = [
  body('username')
    .trim()
    .isLength({ min: 3, max: 30 })
    .withMessage('Username must be between 3 and 30 characters')
    .isAlphanumeric()
    .withMessage('Username must contain only letters and numbers'),
  
  body('email')
    .trim()
    .isEmail()
    .withMessage('Please provide a valid email')
    .normalizeEmail(),
  
  body('password')
    .isLength({ min: 8 })
    .withMessage('Password must be at least 8 characters long')
    .matches(/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*])/)
    .withMessage('Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character')
];

exports.validateLogin = [
  body('username').trim().notEmpty().withMessage('Username is required'),
  body('password').notEmpty().withMessage('Password is required')
];

// Register new user
exports.register = async (req, res) => {
  try {
    // Check for validation errors
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    
    const { username, email, password } = req.body;
    
    // Check if user already exists
    const existingUser = await User.findOne({ 
      $or: [{ email }, { username }] 
    });
    
    if (existingUser) {
      return res.status(409).json({ 
        error: 'User with that email or username already exists' 
      });
    }
    
    // Create new user
    const newUser = new User({
      username,
      email,
      password, // Will be hashed via the pre-save hook
    });
    
    await newUser.save();
    
    // Send response without exposing password
    const user = newUser.toObject();
    delete user.password;
    
    res.status(201).json({
      message: 'User registered successfully',
      user
    });
  } catch (error) {
    console.error('Registration error:', error);
    res.status(500).json({ error: 'Server error during registration' });
  }
};

// Login user
exports.login = [
  loginLimiter, // Apply rate limiting to login
  async (req, res) => {
    try {
      // Check for validation errors
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }
      
      const { username, password } = req.body;
      
      // Find user
      const user = await User.findOne({ username });
      if (!user) {
        // Use a consistent error message to prevent username enumeration
        return res.status(401).json({ error: 'Invalid credentials' });
      }
      
      // Check password
      const isMatch = await user.comparePassword(password);
      if (!isMatch) {
        return res.status(401).json({ error: 'Invalid credentials' });
      }
      
      // Create JWT payload
      const payload = {
        user: {
          id: user.id,
          username: user.username
        }
      };
      
      // Sign token
      jwt.sign(
        payload,
        JWT_SECRET,
        { expiresIn: JWT_EXPIRES_IN },
        (err, token) => {
          if (err) throw err;
          res.json({
            message: 'Login successful',
            token
          });
        }
      );
    } catch (error) {
      console.error('Login error:', error);
      res.status(500).json({ error: 'Server error during login' });
    }
  }
];

// Get current user
exports.getCurrentUser = async (req, res) => {
  try {
    // User is loaded by the auth middleware
    const user = await User.findById(req.user.id).select('-password');
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json(user);
  } catch (error) {
    console.error('Get current user error:', error);
    res.status(500).json({ error: 'Server error' });
  }
};
```

**Final Step: Middleware and Routes Setup**
```
"Now let's implement the authentication middleware for protected routes 
and set up the route configuration with CSRF protection and security headers."
```

**Generated Authentication Middleware and Routes**
```javascript
// middleware/auth.js
const jwt = require('jsonwebtoken');

const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key'; // Change in production

module.exports = (req, res, next) => {
  // Get token from header
  const token = req.header('Authorization');
  
  // Check if no token
  if (!token || !token.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Authorization denied. Token required.' });
  }
  
  // Verify token
  try {
    const decoded = jwt.verify(token.split(' ')[1], JWT_SECRET);
    req.user = decoded.user;
    next();
  } catch (err) {
    if (err.name === 'TokenExpiredError') {
      return res.status(401).json({ error: 'Token expired' });
    }
    res.status(401).json({ error: 'Invalid token' });
  }
};

// routes/auth.js
const express = require('express');
const router = express.Router();
const authController = require('../controllers/authController');
const auth = require('../middleware/auth');
const csrf = require('csurf');
const helmet = require('helmet');

// Apply security middlewares
router.use(helmet()); // Sets various HTTP security headers
const csrfProtection = csrf({ cookie: { httpOnly: true, sameSite: 'strict' } });

// Public routes
router.post(
  '/register', 
  authController.validateRegistration, 
  authController.register
);

router.post(
  '/login', 
  authController.validateLogin, 
  authController.login
);

// Protected routes with CSRF protection
router.get(
  '/me', 
  auth, 
  csrfProtection, 
  authController.getCurrentUser
);

// CSRF token generation endpoint
router.get('/csrf-token', csrfProtection, (req, res) => {
  res.json({ csrfToken: req.csrfToken() });
});

module.exports = router;

// app.js
const express = require('express');
const mongoose = require('mongoose');
const cookieParser = require('cookie-parser');
const cors = require('cors');
const rateLimit = require('express-rate-limit');

const app = express();

// Connect to MongoDB
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost/auth-demo')
  .then(() => console.log('MongoDB connected'))
  .catch(err => console.error('MongoDB connection error:', err));

// Apply global middleware
app.use(express.json());
app.use(cookieParser());
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true
}));

// Global rate limiter
const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per IP per window
  standardHeaders: true
});
app.use(globalLimiter);

// Routes
app.use('/api/auth', require('./routes/auth'));

// Error handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something broke!' });
});

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
```

**Key Improvements:**
- Iterative approach focusing on one aspect at a time
- Explicit security requirements specified in follow-up prompts
- Proper password hashing implementation
- Comprehensive input validation and error handling
- Security features such as rate limiting and secure headers
- Clear separation of concerns between model, controller, and routes

### Example 3: Code Optimization and Refactoring

**Before: Request for General Optimization**
```
"Can you optimize this slow function?"

function findDuplicateProducts(products) {
  let duplicates = [];
  for (let i = 0; i < products.length; i++) {
    for (let j = i + 1; j < products.length; j++) {
      if (products[i].id === products[j].id || 
          products[i].sku === products[j].sku) {
        duplicates.push({
          product1: products[i],
          product2: products[j],
          reason: products[i].id === products[j].id ? 'id' : 'sku'
        });
      }
    }
  }
  // Remove duplicates that have been found multiple times
  let uniqueDuplicates = [];
  for (let i = 0; i < duplicates.length; i++) {
    let isDuplicate = false;
    for (let j = 0; j < uniqueDuplicates.length; j++) {
      if ((duplicates[i].product1.id === uniqueDuplicates[j].product1.id && 
           duplicates[i].product2.id === uniqueDuplicates[j].product2.id) ||
          (duplicates[i].product1.id === uniqueDuplicates[j].product2.id && 
           duplicates[i].product2.id === uniqueDuplicates[j].product1.id)) {
        isDuplicate = true;
        break;
      }
    }
    if (!isDuplicate) {
      uniqueDuplicates.push(duplicates[i]);
    }
  }
  return uniqueDuplicates;
}
```

**Generated Code (Minimal Optimization)**
```javascript
function findDuplicateProducts(products) {
  // Use a Set to track duplicates
  const seen = new Set();
  const duplicates = [];
  
  for (let i = 0; i < products.length; i++) {
    for (let j = i + 1; j < products.length; j++) {
      const isDuplicateId = products[i].id === products[j].id;
      const isDuplicateSku = products[i].sku === products[j].sku;
      
      if (isDuplicateId || isDuplicateSku) {
        // Create unique identifier for each pair
        const pair = [products[i].id, products[j].id].sort().join('-');
        
        if (!seen.has(pair)) {
          seen.add(pair);
          duplicates.push({
            product1: products[i],
            product2: products[j],
            reason: isDuplicateId ? 'id' : 'sku'
          });
        }
      }
    }
  }
  
  return duplicates;
}
```

**After: Structured Optimization Request**
```
"I need to optimize this product duplicate detection function that's causing 
performance issues with large datasets (>10,000 products). Here's the current code:

[paste original function]

Performance concerns:
1. O(n²) nested loop complexity doesn't scale
2. Unnecessary second pass to filter duplicates
3. No early termination for found matches

Constraints:
1. Must find all products with same ID or SKU
2. Must indicate whether match is by ID, SKU, or both
3. Must handle large product sets efficiently

Can you provide an optimized implementation with time complexity analysis?"
```

**Generated Optimized Code**
```javascript
/**
 * Find duplicate products by ID or SKU
 * Time Complexity: O(n) where n is the number of products
 * Space Complexity: O(n) for the hash maps
 * 
 * @param {Array<Object>} products - List of product objects with id and sku
 * @returns {Array<Object>} List of duplicate product pairs with reason
 */
function findDuplicateProducts(products) {
  // Validate input
  if (!Array.isArray(products)) {
    throw new TypeError('Products must be an array');
  }
  
  // Use maps for O(1) lookups
  const idMap = new Map();
  const skuMap = new Map();
  const duplicates = [];
  const seenPairs = new Set(); // Track pairs to avoid duplicates
  
  // Single pass through all products - O(n)
  for (const product of products) {
    // Skip invalid products
    if (!product || typeof product !== 'object') {
      continue;
    }
    
    const { id, sku } = product;
    
    // Check for ID duplicates
    if (id !== undefined) {
      if (idMap.has(id)) {
        const existingProduct = idMap.get(id);
        const pairKey = [existingProduct.id, product.id]
          .sort()
          .join('|');
        
        if (!seenPairs.has(pairKey)) {
          seenPairs.add(pairKey);
          duplicates.push({
            product1: existingProduct,
            product2: product,
            reason: 'id'
          });
        }
      } else {
        idMap.set(id, product);
      }
    }
    
    // Check for SKU duplicates (only if not already matched by ID)
    if (sku !== undefined) {
      if (skuMap.has(sku)) {
        const existingProduct = skuMap.get(sku);
        
        // Skip if already matched on ID
        if (id === existingProduct.id) {
          continue;
        }
        
        const pairKey = [existingProduct.id, product.id]
          .sort()
          .join('|');
        
        if (!seenPairs.has(pairKey)) {
          seenPairs.add(pairKey);
          duplicates.push({
            product1: existingProduct,
            product2: product,
            reason: 'sku'
          });
        }
      } else {
        skuMap.set(sku, product);
      }
    }
  }
  
  return duplicates;
}

// Performance test function
function testPerformance(size) {
  // Generate test data
  const products = [];
  for (let i = 0; i < size; i++) {
    products.push({
      id: `id-${i}`,
      sku: `sku-${i}`,
      name: `Product ${i}`
    });
  }
  
  // Add a few duplicates
  const duplicateCount = Math.max(10, Math.floor(size * 0.01));
  for (let i = 0; i < duplicateCount; i++) {
    // Duplicate by ID
    products.push({
      id: `id-${i}`,
      sku: `sku-${size + i}`,
      name: `Duplicate ID Product ${i}`
    });
    
    // Duplicate by SKU
    products.push({
      id: `id-${size + i}`,
      sku: `sku-${i}`,
      name: `Duplicate SKU Product ${i}`
    });
  }
  
  // Shuffle array to avoid sequential duplicates
  for (let i = products.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [products[i], products[j]] = [products[j], products[i]];
  }
  
  console.time('findDuplicateProducts');
  const duplicates = findDuplicateProducts(products);
  console.timeEnd('findDuplicateProducts');
  
  console.log(`Found ${duplicates.length} duplicate pairs in ${size} products`);
  return duplicates;
}

// Test with increasing dataset sizes
// testPerformance(100);    // Small dataset
// testPerformance(1000);   // Medium dataset
// testPerformance(10000);  // Large dataset
```

**Key Improvements:**
- Specific performance concerns articulated in the prompt
- Clear constraints and requirements provided
- Request for complexity analysis with the solution
- Improved algorithm with O(n) time complexity instead of O(n²)
- Additional input validation and error handling
- Performance testing function included
- Detailed comments explaining the approach

These examples demonstrate how structured, specific prompts with clear requirements and constraints lead to significantly better output from AI coding agents compared to vague, general requests.
</context>

<context name="using_this_module" priority="high">
## Using This Module

This module can be referenced when:

1. **Integrating AI Coding Assistants into Development Workflows**
   - Setting up AI-assisted coding practices in teams
   - Creating organizational guidelines for AI code usage
   - Designing evaluation criteria for AI-generated code

2. **Improving Personal AI Collaboration Effectiveness**
   - Developing more effective prompting strategies
   - Building verification workflows for generated code
   - Creating personal templates for common coding tasks

3. **Designing AI Coding Tools and Extensions**
   - Identifying features needed for safer AI coding tools
   - Creating guardrails for IDE integrations
   - Developing plugins that enhance code verification

4. **Training and Onboarding Developers**
   - Teaching best practices for AI-assisted coding
   - Creating educational materials about AI code generation
   - Demonstrating effective human-AI collaboration patterns

5. **Refining AI Models for Code Generation**
   - Understanding how to improve code generation capabilities
   - Identifying common failure patterns to address
   - Creating better evaluation metrics for code generation models

### Implementation Guidelines

To implement the strategies in this module:

1. **Start with Clear Evaluation Criteria**
   - Define what "good" AI-generated code looks like for your context
   - Establish security, quality, and style requirements
   - Create checklists for code review of AI-generated content

2. **Build Standard Prompt Templates**
   - Create reusable templates for common coding tasks
   - Include explicit requirements, constraints, and context
   - Standardize patterns for iterative refinement

3. **Implement Verification Layers**
   - Integrate automated testing for all AI-generated code
   - Establish additional security review for sensitive functions
   - Create explicit validation processes for generated APIs

4. **Create Feedback Mechanisms**
   - Track effectiveness of different prompting strategies
   - Document common failure modes and workarounds
   - Share successful patterns within development teams

5. **Balance Automation and Oversight**
   - Identify tasks most suitable for AI delegation
   - Establish clear guidelines for human review requirements
   - Create escalation paths for complex or critical components

By applying these principles systematically, development teams can effectively harness the productivity benefits of AI coding agents while maintaining code quality, security, and alignment with project requirements and standards.
</context>

## Using This Module

This module can be referenced when:
- Integrating AI coding assistants into development workflows
- Training developers on effective AI collaboration strategies
- Designing AI-assisted development tools and environments
- Establishing code review processes for AI-generated code
- Creating organizational guidelines for responsible AI usage in development
- Troubleshooting common issues with AI code generation
- Optimizing prompting techniques for coding tasks

Apply these principles systematically to create more effective, secure, and maintainable code through human-AI collaboration while establishing appropriate guardrails and verification processes.

Last Updated: April 14, 2025

    
  // Extract the token without the 'Bearer ' prefix
  const token = authHeader.split(' ')[1];
  
  try {
    // Use verify instead of decode to check signature
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    
    // Check token expiration explicitly
    const currentTime = Math.floor(Date.now() / 1000);
    if (decoded.exp && decoded.exp < currentTime) {
      return res.status(401).json({ message: 'Token expired' });
    }
    
    // Check for required claims
    if (!decoded.userId) {
      return res.status(401).json({ message: 'Invalid token payload' });
    }
    
    // Set user information on request object
    req.user = decoded;
    next();
  } catch (error) {
    // Provide specific error messages for different JWT errors
    if (error.name === 'JsonWebTokenError') {
      return res.status(401).json({ message: 'Invalid token' });
    }
    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({ message: 'Token expired' });
    }
    
    // Log unexpected errors but don't expose details to client
    console.error('Authentication error:', error);
    return res.status(500).json({ message: 'Authentication failed' });
  }
};
```

**Severity:** High
**AI-Specific:** Yes

### 2. Prompt Vagueness [AP-AICODE-002]

**Problem:**
Using vague, ambiguous, or under-specified prompts that leave too much room for interpretation, resulting in code that doesn't meet requirements or makes incorrect assumptions.

**Example:**
```
// ❌ Vague prompt
"Create a function to process user data"

// ❌ Resulting code with assumptions and ambiguity
function processUserData(data) {
  // What processing? What data structure? What validation?
  const result = {};
  
  // Assuming data is an object with user properties
  if (data.name) {
    result.name = data.name.trim();
  }
  
  // Assuming email needs validation
  if (data.email && isValidEmail(data.email)) {
    result.email = data.email.toLowerCase();
  }
  
  return result;
}

function isValidEmail(email) {
  // Overly simplistic validation
  return email.includes('@');
}
```

**Why It Fails:**
- AI makes assumptions to fill in missing details, often incorrectly
- Vague prompts lead to generic solutions that don't fit specific needs
- Lack of constraints results in omitted error handling or validation
- The developer may assume functionalities that weren't explicitly requested
- The resulting code requires significant rework to meet actual requirements

**Better Approach:**
```
// ✅ Specific prompt with clear requirements
"Create a user data processing function that:
1. Accepts a user object with name, email, and age properties
2. Validates that name is a non-empty string
3. Validates that email is in a valid format using a regular expression
4. Validates that age is a number between 18 and 120
5. Returns a new object with sanitized data if valid
6. Throws a ValidationError with specific messages if validation fails"

// ✅ Resulting well-specified implementation
class ValidationError extends Error {
  constructor(message, field) {
    super(message);
    this.name = 'ValidationError';
    this.field = field;
  }
}

/**
 * Process and validate user data
 * @param {Object} userData - The user data to process
 * @param {string} userData.name - User's full name
 * @param {string} userData.email - User's email address
 * @param {number} userData.age - User's age
 * @returns {Object} Processed and validated user data
 * @throws {ValidationError} If validation fails
 */
function processUserData(userData) {
  const result = {};
  
  // Validate name
  if (!userData.name || typeof userData.name !== 'string' || userData.name.trim() === '') {
    throw new ValidationError('Name must be a non-empty string', 'name');
  }
  result.name = userData.name.trim();
  
  // Validate email
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!userData.email || !emailRegex.test(userData.email)) {
    throw new ValidationError('Email must be in a valid format', 'email');
  }
  result.email = userData.email.toLowerCase();
  
  // Validate age
  if (!userData.age || typeof userData.age !== 'number' || userData.age < 18 || userData.age > 120) {
    throw new ValidationError('Age must be a number between 18 and 120', 'age');
  }
  result.age = userData.age;
  
  return result;
}
```

**Severity:** Medium
**AI-Specific:** Yes

### 3. Scope Creep and Over-Engineering [AP-AICODE-003]

**Problem:**
Asking AI to generate overly complex solutions or allowing it to expand scope beyond what's needed, resulting in bloated, difficult-to-maintain code.

**Example:**
```python
# ❌ Over-engineered solution for a simple task
# Prompt: "Write code to check if a string is a palindrome"

class StringAnalyzer:
    """A class for analyzing string properties and patterns."""
    
    def __init__(self, text_processor=None, case_sensitive=False):
        """
        Initialize the StringAnalyzer with optional text processor.
        
        Args:
            text_processor: A callable that pre-processes strings
            case_sensitive: Whether comparisons should be case sensitive
        """
        self.text_processor = text_processor
        self.case_sensitive = case_sensitive
        self.analysis_history = []
    
    def preprocess_text(self, text):
        """Apply preprocessing to the input text."""
        if not self.case_sensitive:
            text = text.lower()
        
        if self.text_processor:
            text = self.text_processor(text)
            
        return text
    
    def is_palindrome(self, text, ignore_spaces=True, ignore_punctuation=True):
        """
        Check if the input text is a palindrome.
        
        Args:
            text: The string to check
            ignore_spaces: Whether to ignore spaces in comparison
            ignore_punctuation: Whether to ignore punctuation
            
        Returns:
            bool: True if palindrome, False otherwise
        """
        if not text:
            return False
            
        processed_text = self.preprocess_text(text)
        
        if ignore_spaces:
            processed_text = processed_text.replace(' ', '')
            
        if ignore_punctuation:
            import string
            for char in string.punctuation:
                processed_text = processed_text.replace(char, '')
        
        # Store in analysis history
        result = processed_text == processed_text[::-1]
        self.analysis_history.append({
            'original': text,
            'processed': processed_text,
            'analysis': 'palindrome',
            'result': result
        })
        
        return result
    
    def get_analysis_history(self):
        """Return the history of string analyses."""
        return self.analysis_history
```

**Why It Fails:**
- Introduces unnecessary complexity for a simple problem
- Creates maintenance burden with additional features nobody asked for
- Obscures the core functionality with elaborate abstractions
- Uses resources (memory, CPU) inefficiently
- Makes code harder to test and debug

**Better Approach:**
```python
# ✅ Simple, focused solution
def is_palindrome(s):
    """
    Check if a string is a palindrome.
    
    Args:
        s: String to check
        
    Returns:
        bool: True if the string is a palindrome, False otherwise
    """
    # Handle empty input
    if not s:
        return False
    
    # Remove spaces and punctuation, convert to lowercase
    import re
    s = re.sub(r'[^\w]', '', s.lower())
    
    # Check if the string equals its reverse
    return s == s[::-1]
```

**Severity:** Medium
**AI-Specific:** Yes

### 4. Hallucinated APIs and Features [AP-AICODE-004]

**Problem:**
AI models sometimes generate code that references non-existent functions, methods, or libraries, creating code that appears valid but won't actually work.

**Example:**
```javascript
// ❌ Code with hallucinated APIs
// Prompt: "Show me how to use React's useLocalStorage hook"

import React, { useState, useEffect, useLocalStorage } from 'react';

function UserPreferences() {
  // useLocalStorage is not a built-in React hook!
  const [theme, setTheme] = useLocalStorage('theme', 'light');
  const [fontSize, setFontSize] = useLocalStorage('fontSize', 'medium');
  
  const toggleTheme = () => {
    setTheme(theme === 'light' ? 'dark' : 'light');
  };
  
  return (
    <div>
      <h2>User Preferences</h2>
      <button onClick={toggleTheme}>
        Switch to {theme === 'light' ? 'Dark' : 'Light'} Theme
      </button>
      <select 
        value={fontSize} 
        onChange={(e) => setFontSize(e.target.value)}
      >
        <option value="small">Small</option>
        <option value="medium">Medium</option>
        <option value="large">Large</option>
      </select>
    </div>
  );
}
```

**Why It Fails:**
- `useLocalStorage` is not a built-in React hook
- Code will result in runtime errors when executed
- Developers might waste time looking for documentation of non-existent features
- May lead to incorrect implementations based on hallucinated functionality
- Makes code review challenging for less experienced team members

**Better Approach:**
```javascript
// ✅ Implementation with actual APIs
import React, { useState, useEffect } from 'react';

// Custom hook implementation for localStorage
function useLocalStorage(key, initialValue) {
  // State to store our value
  const [storedValue, setStoredValue] = useState(() => {
    try {
      // Get from local storage by key
      const item = window.localStorage.getItem(key);
      // Parse stored json or if none return initialValue
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      // If error also return initialValue
      console.error(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  });

  // Return a wrapped version of useState's setter function that
  // persists the new value to localStorage
  const setValue = value => {
    try {
      // Allow value to be a function so we have same API as useState
      const valueToStore =
        value instanceof Function ? value(storedValue) : value;
      // Save state
      setStoredValue(valueToStore);
      // Save to local storage
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      // A more advanced implementation would handle the error case
      console.error(`Error setting localStorage key "${key}":`, error);
    }
  };

  return [storedValue, setValue];
}

function UserPreferences() {
  const [theme, setTheme] = useLocalStorage('theme', 'light');
  const [fontSize, setFontSize] = useLocalStorage('fontSize', 'medium');
  
  const toggleTheme = () => {
    setTheme(theme === 'light' ? 'dark' : 'light');
  };
  
  return (
    <div>
      <h2>User Preferences</h2>
      <button onClick={toggleTheme}>
        Switch to {theme === 'light' ? 'Dark' : 'Light'} Theme
      </button>
      <select 
        value={fontSize} 
        onChange={(e) => setFontSize(e.target.value)}
      >
        <option value="small">Small</option>
        <option value="medium">Medium</option>
        <option value="large">Large</option>
      </select>
    </div>
  );
}
```

**Severity:** High
**AI-Specific:** Yes

### 5. Ignoring Edge Cases and Error Handling [AP-AICODE-005]

**Problem:**
AI-generated code often handles the happy path well but neglects proper error handling, input validation, and edge cases, leading to brittle code that fails in production.

**Example:**
```python
# ❌ Code lacking proper error handling and edge cases
def divide_and_process_data(data, divisor):
    result = []
    for item in data:
        # Missing input validation
        # No error handling for division by zero
        # No type checking
        value = item / divisor
        result.append(process_value(value))
    return result

def process_value(value):
    # Undefined function with no implementation
    # No documentation of what processing occurs
    return value * 2
```

**Why It Fails:**
- No validation of input parameters
- No handling of division by zero
- No type checking for inputs
- Undefined dependencies (process_value implementation)
- No documentation or specifications for expected behavior
- Will fail unexpectedly with various inputs

**Better Approach:**
```python
# ✅ Robust implementation with proper error handling
from typing import List, Union, Any, Optional

def divide_and_process_data(
    data: List[Union[int, float]], 
    divisor: Union[int, float]
) -> List[Union[int, float]]:
    """
    Divide each item in the data list by the divisor and process the result.
    
    Args:
        data: List of numeric values to process
        divisor: Number to divide each data item by
        
    Returns:
        List of processed values
        
    Raises:
        TypeError: If inputs are not of expected types
        ValueError: If divisor is zero or data contains invalid values
    """
    if not isinstance(data, list):
        raise TypeError("Data must be a list")
        
    if not all(isinstance(item, (int, float)) for item in data):
        raise TypeError("All items in data must be numeric")
        
    if not isinstance(divisor, (int, float)):
        raise TypeError("Divisor must be a number")
        
    if divisor == 0:
        raise ValueError("Divisor cannot be zero")
    
    result = []
    for item in data:
        try:
            value = item / divisor
            result.append(process_value(value))
        except Exception as e:
            # Log the error and continue with other items
            import logging
            logging.error(f"Error processing item {item}: {str(e)}")
            continue
            
    return result

def process_value(value: Union[int, float]) -> Union[int, float]:
    """
    Process a numeric value by multiplying it by 2.
    
    Args:
        value: The numeric value to process
        
    Returns:
        The processed value
    """
    return value * 2
```

**Severity:** High
**AI-Specific:** No

### 6. Context-Ignorant Integration [AP-AICODE-006]

**Problem:**
Integrating AI-generated code without considering the broader system context, architectural patterns, or project standards, creating inconsistencies and integration issues.

**Example:**
```java
// ❌ Generated code that doesn't match project patterns
// Prompt: "Generate code to fetch user data from an API"

// Generated code ignores existing project architecture and patterns
public class UserApiClient {
    private static final String API_URL = "https://api.example.com/users";
    
    public static User fetchUser(int userId) throws IOException {
        URL url = new URL(API_URL + "/" + userId);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");
        
        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(conn.getInputStream()))) {
            StringBuilder response = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                response.append(line);
            }
            
            // Direct JSON parsing with no error handling
            JSONObject json = new JSONObject(response.toString());
            User user = new User();
            user.setId(json.getInt("id"));
            user.setName(json.getString("name"));
            user.setEmail(json.getString("email"));
            return user;
        }
    }
}
```

**Why It Fails:**
- Ignores existing architectural patterns in the project
- Uses static methods when project might use dependency injection
- Hardcodes API URL instead of using configuration
- Uses a different HTTP client than the rest of the application
- Performs direct JSON parsing when project might use a serialization library
- Creates tight coupling between components

**Better Approach:**
```java
// ✅ Integration-aware implementation
// First, understand the project context
// Prompt: "Here's how our project handles API calls:"

// Example of existing RestClient in the project
@Service
public class UserService {
    private final RestClient restClient;
    private final String apiBaseUrl;
    
    @Autowired
    public UserService(RestClient restClient, 
                      @Value("${api.baseUrl}") String apiBaseUrl) {
        this.restClient = restClient;
        this.apiBaseUrl = apiBaseUrl;
    }
    
    /**
     * Fetches a user by their ID
     * 
     * @param userId The user's ID
     * @return The user data
     * @throws ApiException If the API request fails
     * @throws ResourceNotFoundException If the user doesn't exist
     */
    public User fetchUser(int userId) throws ApiException, ResourceNotFoundException {
        try {
            return restClient.get(apiBaseUrl + "/users/" + userId, User.class);
        } catch (ApiNotFoundException e) {
            throw new ResourceNotFoundException("User not found with ID: " + userId);
        } catch (ApiException e) {
            logger.error("Error fetching user with ID: {}", userId, e);
            throw e;
        }
    }
}
```

**Severity:** Medium
**AI-Specific:** Yes

### 7. Overlooking Security Considerations [AP-AICODE-007]

**Problem:**
Failing to address security concerns in AI-generated code, leading to vulnerabilities like SQL injection, XSS, CSRF, insecure direct object references, and more.

**Example:**
```javascript
// ❌ Insecure code with SQL injection vulnerability
// Prompt: "Create an Express route to search users by name"

router.get('/search', (req, res) => {
  const userName = req.query.name;
  
  // Direct SQL injection vulnerability!
  const query = `SELECT * FROM users WHERE name LIKE '%${userName}%'`;
  
  db.query(query, (err, results) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    res.json(results);
  });
});
```

**Why It Fails:**
- Direct interpolation of user input into SQL query creates SQL injection vulnerability
- No input validation or sanitization
- Exposes database error messages to clients
- No authentication or authorization checks
- Returns potentially sensitive user data without filtering

**Better Approach:**
```javascript
// ✅ Secure implementation with prepared statements
router.get('/search', authenticate, (req, res) => {
  // Input validation
  const userName = req.query.name;
  if (!userName || typeof userName !== 'string') {
    return res.status(400).json({ error: 'Invalid name parameter' });
  }
  
  // Rate limiting check (implementation depends on middleware)
  if (isRateLimited(req)) {
    return res.status(429).json({ error: 'Too many requests' });
  }
  
  // Use parameterized query to prevent SQL injection
  const query = 'SELECT id, name, email FROM users WHERE name LIKE ?';
  const searchParam = `%${userName}%`;
  
  db.query(query, [searchParam], (err, results) => {
    if (err) {
      // Log the error but don't expose details to client
      console.error('Database error:', err);
      return res.status(500).json({ error: 'An error occurred while searching' });
    }
    
    // Check authorization for returned results
    const authorizedResults = results.filter(user => 
      canViewUser(req.user, user)
    );
    
    res.json(authorizedResults);
  });
});

// Authorization helper
function canViewUser(currentUser, targetUser) {
  // Admin can see all users
  if (currentUser.role === 'admin') return true;
  
  // Users can see themselves
  if (currentUser.id === targetUser.id) return true;
  
  // Users can see other users in their organization
  if (currentUser.organizationId === targetUser.organizationId) return true;
  
  return false;
}
```

**Severity:** Critical
**AI-Specific:** No
</context>

<context name="reasoning_principles" priority="low">
## Reasoning Principles

Understanding how to guide AI coding agents toward better outcomes requires knowledge of their reasoning capabilities and limitations.

### 1. Explicit vs. Implicit Information

AI coding agents work best with explicit, clearly stated information rather than relying on implicit understanding. Humans often communicate with shared context and unstated assumptions, but AI requires explicit articulation of requirements and constraints.

**Implementation Strategy:**
- State all requirements explicitly, even those that seem obvious
- Define interfaces, function signatures, and return types up front
- Specify error handling expectations and edge cases
- Be explicit about non-functional requirements (performance, security, etc.)
- Articulate any assumptions you're making about the system

**Example - Implicit vs. Explicit Prompting:**
```
# ❌ Implicit (Too Many Assumptions)
"Write a function to validate user input."

# ✅ Explicit (Clear Requirements)
"Write a function to validate a user registration form with these fields:
- username: 3-20 alphanumeric characters, no spaces
- email: Standard email format with valid TLD
- password: Minimum 8 characters, must include uppercase, lowercase, 
  number, and special character
- age: Integer between 18-120

The function should return an object with a 'valid' boolean and
an 'errors' object containing field-specific error messages."
```

### 2. Step-by-Step Reasoning

AI models tend to produce better results when encouraged to break down complex problems into smaller steps and reason through each step sequentially.

**Implementation Strategy:**
- Ask the AI to outline its approach before implementation
- Request explanation of design choices and tradeoffs
- Use "chain of thought" prompting techniques
- Break complex tasks into sequential subtasks
- Ask for intermediate results at critical points

**Example - Step-by-Step Implementation:**
```
"Let's implement a JWT authentication system step by step:

1. First, outline the data structure for user credentials and tokens
2. Next, create the function to register users with password hashing
3. Then, implement the login function that validates credentials and issues tokens
4. After that, create the token verification middleware
5. Finally, implement the token refresh functionality

At each step, explain your design decisions and security considerations."
```

### 3. Feedback Integration Mechanisms

AI coding agents improve significantly when given specific feedback on their outputs and clear guidance for corrections.

**Implementation Strategy:**
- Provide specific, actionable feedback on generated code
- Point out exact locations and nature of issues
- Explain why something is problematic, not just what
- Suggest concrete alternatives or improvements
- Acknowledge and reinforce good practices when observed

**Example - Effective Feedback:**
```
"The authentication middleware you generated has a few issues:

1. In line 12, you're using jwt.decode() instead of jwt.verify(), which doesn't
   check if the token signature is valid. This is a security vulnerability.

2. There's no explicit check for token expiration (the exp claim).

3. The error handling at lines 18-20 doesn't distinguish between different
   types of JWT errors (invalid signature, expired token, etc.).

Could you update the code to address these specific issues?"
```

### 4. Anchoring with Examples

AI models respond well to concrete examples that demonstrate the desired implementation patterns, coding style, or approach.

**Implementation Strategy:**
- Provide examples of similar code from your codebase
- Show "before and after" examples to illustrate transformations
- Use examples to demonstrate coding conventions
- Create mini-templates for repeating patterns
- Show both positive examples (do this) and negative examples (avoid this)

**Example - Anchoring with Project Examples:**
```
"In our project, we implement API endpoints following this pattern:

```javascript
router.post('/resource', validateResourceMiddleware, async (req, res, next) => {
  try {
    // 1. Extract validated data from request
    const resourceData = req.validatedData;
    
    // 2. Call service layer function
    const result = await resourceService.createResource(resourceData);
    
    // 3. Return standardized response
    return res.status(201).json({
      success: true,
      data: result,
      message: 'Resource created successfully'
    });
  } catch (error) {
    // 4. Error handling follows this pattern
    return next(createError(error));
  }
});
```

Please implement the PUT /users/:id endpoint following this same pattern
to update user information."
```

### 5. Context Refreshing and Reinforcement

For longer, more complex coding sessions, AI models benefit from occasional context refreshing to maintain focus and coherence.

**Implementation Strategy:**
- Periodically summarize progress and current state
- Restate key requirements or constraints at transition points
- Reference previous decisions when they impact current implementation
- Create "checkpoints" that capture the current understanding
- Explicitly note when requirements or approach changes

**Example - Context Refreshing:**
```
"So far, we've implemented:
1. The user data model with validation
2. The registration endpoint with password hashing
3. The login functionality with JWT issuance

Let's now implement the password reset flow. Remember that we're using:
- nodemailer for sending emails
- crypto for generating secure reset tokens
- a 1-hour expiration for reset tokens

Let's start with the function to generate and store reset tokens..."
```

### 6. Test-Driven Specification

Using tests to define expected behavior helps AI models understand requirements more precisely and produces code that aligns better with actual needs.

**Implementation Strategy:**
- Write test cases before implementation code
- Use tests to define edge cases and expected handling
- Define clear assertions that specify outputs for given inputs
- Use test descriptions to communicate intent
- Ask AI to implement code that passes the tests

**Example - Test-Driven Approach:**
```
"Here are the test cases for the date formatting utility we need:

```javascript
describe('dateFormatter', () => {
  test('formats YYYY-MM-DD correctly', () => {
    expect(dateFormatter('2023-09-15', 'YYYY-MM-DD', 'MM/DD/YYYY'))
      .toBe('09/15/2023');
  });
  
  test('handles time components', () => {
    expect(dateFormatter('2023-09-15T14:30:45', 'YYYY-MM-DDTHH:mm:ss', 'HH:mm'))
      .toBe('14:30');
  });
  
  test('returns null for invalid dates', () => {
    expect(dateFormatter('invalid-date', 'YYYY-MM-DD', 'MM/DD/YYYY'))
      .toBe(null);
  });
  
  test('throws error for invalid format patterns', () => {
    expect(() => dateFormatter('2023-09-15', 'invalid', 'MM/DD/YYYY'))
      .toThrow('Invalid input format pattern');
  });
});
```

Please implement the dateFormatter function that will pass all these tests."
```

By applying these reasoning principles, developers can more effectively guide AI coding assistants toward producing higher-quality code that meets requirements and integrates well with existing systems.
</context>

<context name="model_specific_notes" priority="low">
## Model-Specific Implementation Notes

Different AI coding assistants have distinct strengths, limitations, and behavioral patterns. Understanding these differences can help you optimize your workflow with each tool.

### For Cursor AI

Cursor AI is built on VS Code and specializes in project-aware coding assistance.

**Strengths:**
- Strong at multi-file operations and understanding project structure
- Excellent at refactoring and code transformation tasks
- Good context retention across conversation turns
- Built-in support for running code and debugging
- Effective agent mode for autonomous multi-step tasks

**Limitations:**
- May sometimes generate non-deterministic results for the same prompt
- Can occasionally be overconfident with complex architectural decisions
- Sometimes struggles with very large files (>1000 lines)
- May have difficulty with obscure libraries or frameworks

**Best Practices:**
- Use specific file references when asking for changes (`In src/components/Header.js, modify the navigation...`)
- Leverage its file browser awareness to provide context
- For complex changes, use the "explain first, then implement" approach
- Provide examples from your codebase for stylistic consistency
- Be explicit about which dependencies/versions you're using

**Example Effective Patterns:**
```
"In our utils/formatting.js file, we need to add a new function for currency formatting.
It should follow the pattern of our existing formatDate and formatNumber functions:

[Show existing code from the file]

Please add a formatCurrency function that takes an amount (number) and a
currency code (string, default 'USD'), and returns a properly formatted string
using the Intl.NumberFormat API."
```

### For GitHub Copilot

GitHub Copilot excels at inline completions and is deeply integrated with multiple IDEs.

**Strengths:**
- Excellent at completing code based on partial implementation
- Strong pattern recognition within a repository
- Good at standard programming tasks and common libraries
- Integrates well with various IDEs (VS Code, Visual Studio, JetBrains)
- Effective at generating unit tests for existing code

**Limitations:**
- More limited conversation capabilities compared to chat-first models
- Sometimes continues generating beyond the desired scope
- May occasionally suggest deprecated approaches
- Can be less effective with highly specialized domain logic

**Best Practices:**
- Write clear function signatures and comments before asking for implementations
- Use code comments to guide its completions (`// Now handle the error case where user is not found`)
- Try "stub and fill" approach—write function shells, then let Copilot fill them in
- For complex functions, outline the approach using comments first
- Focus on smaller, discrete tasks rather than large-scale implementations

**Example Effective Patterns:**
```javascript
/**
 * Validates a product submission against business rules
 * @param {Object} product - The product to validate
 * @param {string} product.name - Product name (required, 3-50 chars)
 * @param {number} product.price - Price in cents (required, positive integer)
 * @param {string[]} product.categories - Categories (at least one required)
 * @param {string} product.description - Product description (optional, max 1000 chars)
 * @return {Object} Validation result with isValid flag and errors array
 */
function validateProduct(product) {
  // Implement validation logic here
}
```

### For Claude and ChatGPT

Claude and general-purpose models like ChatGPT often work best with conversational coding assistance.

**Strengths:**
- Excellent at explaining code and concepts
- Strong contextual understanding in long conversations
- Good at high-level design and architectural guidance
- Effective for exploring multiple approaches to a problem
- Can handle a wide variety of programming languages and paradigms

**Limitations:**
- Less aware of project structure compared to dedicated coding tools
- No direct ability to run or test generated code
- Sometimes limited by context window for large codebases
- Cannot directly access or modify files

**Best Practices:**
- Provide more explicit context about your project structure and environment
- Use clear, structured prompting with specific requirements
- Leverage the conversational nature for iterative refinement
- Ask for explanations along with implementations
- Use MCP (Model Context Protocol) for structured context with Claude

**Example Effective Patterns:**
```
<context name="project_info" priority="high">
This is a Node.js 18 project using Express.js 4.17 and MongoDB via Mongoose 6.5.
We use TypeScript with strict type checking and ESLint with Airbnb rules.
</context>

<context name="task" priority="high">
I need to implement a middleware for API request logging that:
1. Logs incoming request method, path, and query parameters
2. Tracks response time# AI-Assisted Coding Agents: Capabilities, Limitations, and Best Practices

> A comprehensive guide to understanding, effectively utilizing, and working around the limitations of AI coding assistants like Cursor AI, GitHub Copilot, and Claude.

## Metadata
- **Priority:** high
- **Domain:** software-development
- **Target Models:** claude, cursor-ai, github-copilot, general-llms
- **Related Modules:** prompt-engineering, software-testing, code-security, human-ai-collaboration

## Module Overview

This module provides a structured framework for understanding and effectively utilizing AI-assisted coding systems. It covers fundamental concepts, key strategies, implementation patterns, and common pitfalls when working with code generation models. The focus is on creating a productive human-AI collaboration workflow that maximizes the strengths of both while implementing appropriate guardrails around the current limitations of AI-generated code.

<context name="ai_coding_agents_definition" priority="high">
## Conceptual Foundation

AI coding agents are software tools powered by large language models (LLMs) that assist developers with code generation, modification, explanation, and optimization. These systems—such as GitHub Copilot, Cursor AI, and Claude—process natural language prompts, code context, and documentation to generate or suggest code that satisfies the developer's intent.

### Core Components of AI Coding Agents

Modern AI coding assistants typically integrate several key capabilities:

1. **Code Generation**: Producing code from natural language descriptions or converting pseudocode to implementation
2. **Context-Aware Completion**: Suggesting code completions based on surrounding code, project structure, and development patterns 
3. **Code Explanation**: Describing what existing code does in human-readable language
4. **Code Transformation**: Refactoring, optimizing, or adapting existing code to new requirements
5. **Bug Detection**: Identifying potential issues or suggesting fixes for problematic code
6. **Project Navigation**: Understanding multi-file projects and making cross-file changes
7. **Interactive Debugging**: Assisting with runtime issues or explaining error messages

### How AI Coding Agents Work

AI coding agents leverage large language models trained on vast corpora of code from sources like GitHub, Stack Overflow, and documentation. The underlying process typically involves:

1. **Context Processing**: The agent analyzes the current codebase, open files, and cursor position to establish context
2. **Query Interpretation**: The model interprets the developer's prompt or question
3. **Pattern Matching**: The model identifies patterns in its training data relevant to the query and context
4. **Code Generation**: The model produces code that attempts to satisfy the developer's intent
5. **Iterative Refinement**: Many agents support follow-up interactions to refine, debug, or expand upon the generated code

### General Limitations of AI Coding Agents

Despite their impressive capabilities, current AI coding agents face several fundamental limitations:

1. **Training Cutoff Limitations**: Models have knowledge only up to their training cutoff date and may not understand recent frameworks, libraries, or language features
2. **Pattern Matching vs. Understanding**: Models generate code based on statistical patterns rather than true understanding of program execution or logic
3. **Hallucinated APIs and Features**: Models may confidently suggest non-existent functions, classes, or methods
4. **Security and Quality Gaps**: Generated code may contain subtle bugs, security vulnerabilities, or inefficient implementations
5. **Context Window Constraints**: Limited ability to reason about large codebases or complex multi-file projects
6. **Lack of Execution Feedback**: Models typically cannot run code to verify correctness or validate outputs
7. **Lack of Domain Understanding**: Limited knowledge of business logic, specialized domains, or company-specific implementations
8. **Overconfidence**: Providing plausible-sounding but incorrect solutions without indicating uncertainty

### The Role of the Human Developer

The human developer plays several critical roles in effective AI-assisted coding:

1. **Intent Provider**: Clearly communicating the desired functionality and constraints
2. **Context Creator**: Ensuring the AI has necessary context and background information
3. **Solution Architect**: Defining the overall structure and approach to problems
4. **Code Reviewer**: Critically evaluating generated code for correctness, security, and quality
5. **Integration Expert**: Adapting generated code to fit within existing systems and standards
6. **Testing Supervisor**: Verifying that generated code performs as expected under different conditions
7. **Learning Guide**: Training the AI through effective prompting and feedback patterns

Understanding these roles is essential for creating an effective human-AI collaboration that produces high-quality, reliable code.
</context>

<context name="core_principles" priority="high">
## Core Principles

### 1. Effective Prompt Engineering for Code Generation

Creating effective prompts is fundamental to getting useful responses from AI coding agents. The most effective prompts for code generation follow specific patterns:

**Clear and Specific Requirements:**
```
# ✅ Effective Prompt:
"Write a Python function that validates email addresses. It should:
- Accept a string input
- Return True for valid emails, False otherwise
- Check for a valid format (name@domain.tld)
- Ensure the domain has at least one dot
- Use regular expressions for the validation"

# ❌ Vague Prompt:
"Write some code to check emails"
```

**Explicit Context Provision:**
```
# ✅ Effective Prompt:
"I'm using Express.js 4.18 with MongoDB via Mongoose 7.5.0. Write a route handler 
for user registration that includes input validation, password hashing with bcrypt, 
and returns appropriate HTTP status codes."

# ❌ Missing Context:
"Write a user registration function"
```

**Guideline Establishment:**
```
# ✅ Effective Prompt:
"Generate a React component using TypeScript and functional component syntax. 
Follow these standards:
- Use React hooks instead of class components
- Include proper TypeScript interfaces for props and state
- Include error handling for API calls
- Include basic unit tests using React Testing Library"

# ❌ No Guidelines:
"Make a React component for displaying user profiles"
```

**Function Signatures and Interfaces:**
```
# ✅ Effective Prompt:
"Implement the following function in JavaScript:
/**
 * Sorts an array of objects by the specified property
 * @param {Array<Object>} items - The array to sort
 * @param {string} property - The property to sort by
 * @param {boolean} ascending - Whether to sort in ascending order
 * @return {Array<Object>} The sorted array
 */
function sortByProperty(items, property, ascending) {
  // Implementation needed
}"

# ❌ No Interface Definition:
"Write a function to sort objects in an array"
```

**Chunking and Scoping:**

Break down complex tasks into smaller, manageable parts:

```
# ✅ Effective Approach:
"Let's build a URL shortener API step by step:
1. First, define the database schema for storing shortened URLs
2. Next, write the function to generate a unique short code
3. Then, create the endpoint for creating new shortened URLs
4. Finally, implement the redirection logic"

# ❌ Overwhelming Scope:
"Build a complete URL shortener service with user authentication, analytics, 
custom domains, and link expiration"
```

### 2. Code Verification and Quality Assurance

Generated code should never be used without appropriate verification and quality checks:

**Incremental Testing:**
```python
# Generate a function
def parse_csv(file_path):
    """Parse a CSV file and return a list of dictionaries."""
    import csv
    
    results = []
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            results.append(row)
    
    return results

# Write a unit test to verify behavior
import unittest
from unittest.mock import mock_open, patch

class TestParseCSV(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, 
           read_data='name,age\nAlice,30\nBob,25')
    def test_parse_csv(self, mock_file):
        result = parse_csv('dummy.csv')
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'Alice')
        self.assertEqual(result[0]['age'], '30')
        self.assertEqual(result[1]['name'], 'Bob')
        self.assertEqual(result[1]['age'], '25')

# Run the test
unittest.main(argv=['first-arg-is-ignored'], exit=False)
```

**Code Review Checklist:**
- Correctness: Does the code correctly implement the specified functionality?
- Edge Cases: Does it handle boundary conditions and unexpected inputs?
- Error Handling: Does it gracefully handle exceptions and error conditions?
- Security: Is the code free from common vulnerabilities (e.g., SQL injection, XSS)?
- Performance: Are there any obvious inefficiencies or scalability issues?
- Readability: Is the code clear, well-documented, and maintainable?
- Standards: Does it follow project coding standards and best practices?

**Static Analysis:**
Integrate AI-generated code with static analysis tools to catch issues:
```bash
# Example for Python
pylint generated_code.py
mypy generated_code.py
bandit generated_code.py  # Security-focused

# Example for JavaScript
eslint generated_code.js
```

**Explicit Validation Requests:**
```
"Review the following code for potential issues, focusing on security vulnerabilities, 
edge cases, and performance problems:

[paste generated code here]

Then provide an improved version that addresses any issues you identify."
```

### 3. Feedback Loops and Iterative Refinement

Effective AI coding collaboration typically requires multiple rounds of feedback and refinement:

**Initial Generation → Analysis → Refinement Cycle:**
```
# Step 1: Initial Request
"Create a function to calculate the median value of an array of numbers in JavaScript"

# Step 2: Analyze Generated Solution
"The solution looks correct but has a few issues:
1. It doesn't handle empty arrays
2. It modifies the original array when sorting
3. Missing type checking for non-numeric values
Please address these issues."

# Step 3: Iterative Refinement
"Good improvements. Now let's add proper error handling with specific error 
messages for each validation case. Also, add JSDoc comments to document the function."
```

**Test-Driven Refinement:**
```
# Step 1: Generate code from requirements
"Write a password strength validator in Python that checks for minimum length, 
uppercase, lowercase, numbers, and special characters"

# Step 2: Generate tests to validate requirements
"Now write comprehensive unit tests for this password validator that cover all 
requirements and edge cases"

# Step 3: Identify gaps through tests
"The tests revealed that the validator doesn't properly handle non-ASCII characters. 
Please update the validator to properly validate Unicode strings."
```

**Explanation-Driven Refinement:**
```
# Step 1: Request code explanation
"Explain how the following authentication middleware works, step by step:
[paste code here]"

# Step 2: Identify improvement opportunities
"Based on your explanation, I see that the middleware doesn't check token expiration. 
Please modify the code to include proper expiration validation."

# Step 3: Verify solution understanding
"Explain how your modified solution handles token expiration and what happens 
when an expired token is detected."
```

### 4. Documentation and Knowledge Transfer

Well-documented code generation helps both current and future developers:

**Request Documentation Along with Code:**
```
"Write a recursive directory traversal function in Python and include:
1. Comprehensive docstrings in Google format
2. Type hints for all parameters and return values
3. Example usage showing common scenarios
4. Comments explaining any complex logic
5. Links to relevant Python documentation where appropriate"
```

**Request for Self-Explaining Code:**
```
"Generate a React custom hook for managing form state. The code should be 
self-documenting with:
- Clear, descriptive variable and function names
- Logical structure that follows standard patterns
- Comments explaining 'why' rather than 'what' where appropriate
- Minimal external dependencies"
```

**Knowledge Capture Pattern:**
```
"Explain the following code to me, focusing on:
1. The design pattern being used
2. Potential performance implications
3. Security considerations
4. How to test it effectively

[paste code here]

Then, summarize this explanation in a format suitable for a team documentation wiki."
```

By applying these core principles, developers can dramatically improve the quality, reliability, and maintainability of AI-generated code while building an effective human-AI collaboration workflow.
</context>

<context name="implementation_patterns" priority="medium">
## Implementation Patterns

### Patterns for Structuring Tasks for AI Coders

The following patterns help organize and structure tasks for more effective AI code generation:

#### 1. Write-Explain-Validate Loop

This pattern creates a continuous feedback loop that improves code quality:

```
# Step 1: Write
"Write a function that implements binary search in JavaScript"

# Step 2: Explain
"Explain the time and space complexity of this implementation. 
Are there any edge cases it doesn't handle properly?"

# Step 3: Validate
"Generate unit tests that verify the correctness of this function, 
including edge cases like empty arrays, single-element arrays, 
and duplicates in the array."

# Step 4: Refine (repeat from Step 1 with improvements)
"Update the binary search implementation to handle the edge cases 
identified in the tests and optimize the code based on your complexity analysis."
```

This pattern works because it forces both the AI and the developer to think critically about the solution at each stage, identifying potential issues before they become problems in production.

#### 2. Spec-First Development

This pattern focuses on clear specifications before implementation:

```
# Step 1: Define Interface
"Define a TypeScript interface for a weather service API client that can:
- Fetch current weather by city or coordinates
- Get 5-day forecast
- Search for location by name or postal code
- Convert between units (metric/imperial)"

# Step 2: Approve/Refine Interface
"The interface looks good, but let's add error handling patterns and 
rate limiting consideration."

# Step 3: Implement Core Functionality
"Now implement the core functionality for fetching current weather, 
using the Fetch API and with proper error handling as defined in our interface."

# Step 4: Add Tests
"Create unit tests for the implemented functionality using Jest, 
mocking the external API calls."
```

This approach ensures clarity about what will be built before writing implementation code, reducing rework and misalignment.

#### 3. Pseudocode-to-Code Transformation

This pattern leverages human architectural thinking with AI implementation skills:

```
# Step 1: Write Pseudocode
"Here's my pseudocode for a file upload service with progress tracking:

```
function uploadFile(file, progressCallback):
  1. Validate file size and type
  2. Create form data with file and metadata
  3. Initialize upload with resumable protocol
     a. Get upload URL from server
     b. Set up chunked upload parameters
  4. For each chunk of the file:
     a. Calculate progress percentage
     b. Send chunk to server
     c. Call progressCallback with current progress
     d. Handle any chunk upload failures with retry logic
  5. When all chunks complete, finalize upload on server
  6. Return download URL from server response
```

# Step 2: Generate Implementation
"Implement this pseudocode in JavaScript using the Fetch API and 
the Blob.slice() method for chunking. Include proper error handling 
and progress calculation."

# Step 3: Review and Refine
"The implementation looks good, but I'd like to add support for pause/resume. 
How would you modify this code to support pausing and resuming uploads?"
```

This pattern plays to the strengths of both human and AI: humans excel at high-level problem decomposition, while AI is good at turning structured ideas into implementation details.

#### 4. Component Assembly Pattern

This pattern breaks a complex system into manageable components:

```
# Step 1: System Architecture
"I'm building a task management application with the following components:
- Task list component (displays and manages tasks)
- Task creation form
- Filter and sort controls
- Task detail view
- Statistics dashboard

Let's focus on implementing these one by one."

# Step 2: Component Implementation
"First, let's create the Task list component in React with TypeScript. 
It should:
- Accept an array of Task objects as props
- Support marking tasks as complete
- Support deleting tasks
- Display tasks in a responsive grid/list view"

# Step 3: Component Integration
"Now let's implement the Task creation form that will add new tasks 
to our task list. It should work with our existing Task list component."

# Step 4: System Assembly
"Now, create a parent App component that combines our Task list and 
Task creation form, managing the shared state between them."
```

This approach prevents overwhelming the AI with complexity while ensuring components work together correctly.

### Collaboration Models

Different collaboration models define how developers and AI work together:

#### 1. AI as Implementation Assistant

Human provides high-level design and specifications; AI handles implementation details:

```
# Human provides architectural direction
"I need a caching layer for my Express.js application that:
- Uses Redis as the backing store
- Caches API responses based on URL and query parameters
- Supports TTL configuration per route
- Provides a way to manually invalidate specific cache entries

Design this as middleware that can be applied to specific routes."

# AI generates implementation code
function cacheMiddleware(options) {
  const redis = require('redis');
  const client = redis.createClient(options.redisOptions);
  
  return async (req, res, next) => {
    // Implementation details handled by AI
    // ...
  };
}

# Human reviews, tests, and integrates
```

#### 2. AI as Code Reviewer

Human writes code; AI reviews for issues, improvements, and optimizations:

```
# Human writes code
function calculateTotal(items) {
  let total = 0;
  for (let i = 0; i < items.length; i++) {
    total += items[i].price * items[i].quantity;
  }
  return total;
}

# AI reviews
"Here's my analysis of your code:

1. The function works correctly for calculating totals.
2. Improvement opportunity: Use reduce() for a more functional approach
3. Missing input validation for null/undefined items
4. Consider adding type checking or JSDoc for better IDE support
5. Edge case: The function doesn't handle empty arrays explicitly

Here's an improved version:

```javascript
/**
 * Calculate the total price of all items
 * @param {Array<{price: number, quantity: number}>} items - Array of items with price and quantity
 * @return {number} The total price
 */
function calculateTotal(items) {
  if (!items || !Array.isArray(items)) {
    throw new Error('Items must be a valid array');
  }
  
  return items.reduce((total, item) => {
    if (typeof item.price !== 'number' || typeof item.quantity !== 'number') {
      throw new Error('Each item must have numeric price and quantity');
    }
    return total + (item.price * item.quantity);
  }, 0);
}
```"
```

#### 3. Paired Problem-Solving

Human and AI collaborate on discovering and implementing solutions together:

```
# Human poses problem
"I'm trying to optimize our image processing pipeline. Currently, we're loading 
all images in memory before processing them, which is causing out-of-memory issues 
with large batches. How can we implement a streaming approach?"

# AI suggests approaches
"You could solve this with a streaming approach. Here are a few options:

1. Use a generator function to process images one at a time
2. Implement a worker pool pattern to process images in parallel with controlled concurrency
3. Use Node.js streams for a fully streaming pipeline

Which approach would you like to explore further?"

# Human selects approach
"Let's go with the worker pool pattern as we need some parallelism but with 
controlled memory usage."

# AI elaborates on implementation
"Here's how we could implement a worker pool for image processing..."

# Collaborative refinement continues
```

### Prompting Techniques for Multi-File Projects

Working with complex projects across multiple files requires specialized approaches:

#### 1. Context Building Pattern

Progressively build context about a larger project:

```
# Step 1: Explain project structure
"I'm working on a React e-commerce application with the following structure:
- src/
  - components/
  - contexts/
  - hooks/
  - pages/
  - services/
  - utils/

The application uses React Router for navigation, React Query for data fetching,
and styled-components for styling."

# Step 2: Explain specific component dependencies
"I need to modify the ProductDetail component which depends on:
1. The CartContext for adding items to cart
2. The useProduct hook for fetching product details
3. The ImageGallery component for displaying product images"

# Step 3: Show relevant code snippets
"Here's the current ProductDetail component:
[code snippet]

And here's the CartContext:
[code snippet]

And the useProduct hook:
[code snippet]"

# Step 4: Request specific changes
"Now, I need to add a 'Save for Later' feature that moves items from cart 
to a saved items list. Please modify the ProductDetail component and suggest 
any necessary changes to the CartContext."
```

#### 2. File Map Pattern

Create a mental map for the AI of related files and their purposes:

```
"I'm working on a Node.js backend with the following key files:

1. src/models/User.js - Mongoose schema for users
```js
const mongoose = require('mongoose');
const userSchema = new mongoose.Schema({
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  // ...other fields
});
// ...methods and hooks
```

2. src/controllers/authController.js - Handles authentication logic
```js
// Current login and register functions
// ...
```

3. src/middleware/auth.js - JWT verification middleware
```js
// Current JWT verification code
// ...
```

4. src/routes/auth.js - Authentication routes
```js
// Current route definitions
// ...
```

I need to add password reset functionality. Please suggest changes to each file
to implement this feature, including:
1. Adding necessary fields to the User schema
2. Creating password reset controller functions
3. Adding new middleware if needed
4. Defining new routes for password reset"
```

#### 3. Interface-First Pattern

Define interfaces between components before implementation details:

```
"I'm building a multi-file React application for task management. Let's first 
define the interfaces between components:

1. TaskItem interface:
```typescript
interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  dueDate: Date | null;
  priority: 'low' | 'medium' | 'high';
}
```

2. TaskContext interface:
```typescript
interface TaskContextType {
  tasks: Task[];
  addTask: (task: Omit<Task, 'id'>) => void;
  updateTask: (id: string, updates: Partial<Task>) => void;
  deleteTask: (id: string) => void;
  getTasks: () => Promise<void>;
}
```

Now, please implement:
1. The TaskContext.tsx file that provides this context
2. A useTaskActions.ts custom hook that consumes this context
3. A TaskList.tsx component that displays tasks using the context"
```

These implementation patterns provide structured approaches to effectively utilize AI coding assistants for different scenarios and project complexities.
</context>

<context name="decision_logic" priority="medium">
## Decision Logic for Implementation

Understanding when and how to leverage AI coding assistants requires clear decision frameworks.

### Step 1: Task Suitability Assessment

```
START
│
├─ IS the task well-defined with clear requirements?
│  ├─ YES → Continue evaluation
│  └─ NO → Clarify requirements before proceeding
│
├─ DOES the task involve a standard pattern or widely-used library?
│  ├─ YES → Good candidate for AI assistance
│  └─ NO → Requires more caution and verification
│
├─ IS the task self-contained with minimal external dependencies?
│  ├─ YES → Good candidate for AI assistance
│  └─ NO → Consider breaking down into smaller parts
│
├─ DOES the task require deep domain knowledge?
│  ├─ YES → Human should provide domain context or handle the task
│  └─ NO → Good candidate for AI assistance
│
├─ IS the task security-critical?
│  ├─ YES → Requires thorough human verification
│  └─ NO → Standard verification procedures apply
│
└─ CONCLUSION: Rate task suitability (High/Medium/Low)
```

### Step 2: Approach Selection

```
BASED ON task characteristics:
│
├─ IF task is algorithmic or involves standard patterns
│  └─ Use AI for initial implementation with human review
│
├─ IF task is exploratory or innovative
│  └─ Use AI as brainstorming partner with human leading design
│
├─ IF task involves system integration
│  └─ Human designs integration points, AI implements components
│
├─ IF task is performance-critical
│  └─ Human defines performance criteria, AI implements with benchmarking
│
├─ IF task requires extensive refactoring
│  └─ AI analyzes code and proposes refactorings for human approval
│
└─ IF task is maintenance/bug fixing
   └─ AI diagnoses issues and proposes fixes for human verification
```

### Step 3: Execution Strategy

```
FOR EACH selected task:
│
├─ IF complexity is high
│  ├─ Break into subtasks
│  └─ Address each subtask separately
│
├─ IF multiple files affected
│  ├─ Map file relationships
│  └─ Establish interfaces before implementation
│
├─ IF task requires new library/framework
│  ├─ Verify AI knowledge of latest version
│  └─ Confirm with documentation if needed
│
├─ IF external API integration needed
│  ├─ Human provides API documentation
│  └─ AI implements with mock testing
│
└─ IF task involves data processing
   ├─ Test with small datasets first
   └─ Verify edge cases explicitly
```

### Step 4: Verification and Integration Checklist

```
VERIFICATION CHECKLIST:
│
├─ Code Review
│  ├─ Does the solution match requirements?
│  ├─ Are edge cases handled?
│  ├─ Is error handling appropriate?
│  ├─ Are there security concerns?
│  └─ Does the code follow project standards?
│
├─ Testing
│  ├─ Unit tests for core functionality
│  ├─ Integration tests for component interaction
│  ├─ Edge case testing
│  └─ Performance testing if relevant
│
├─ Security Assessment
│  ├─ Input validation
│  ├─ Authentication/authorization checks
│  ├─ Data sanitization
│  └─ Secure coding practices
│
└─ Documentation
   ├─ Code comments for complex logic
   ├─ Function/method documentation
   ├─ Usage examples
   └─ Update project documentation if needed
```

### Key Questions to Consider

When deciding whether or how to use AI for a coding task, consider these questions:

1. **Criticality**: How crucial is this code to core business functions?
   - Mission-critical code requires higher scrutiny and more human involvement
   - Non-critical code can have more AI autonomy with standard verification

2. **Novelty**: Is this a standard pattern or a novel solution?
   - Standard patterns (e.g., CRUD operations) work well with AI
   - Novel designs benefit from human architectural leadership with AI assistance

3. **Complexity**: What is the complexity level of the task?
   - Simple, well-defined tasks are ideal for AI implementation
   - Complex tasks should be broken down into manageable components

4. **Maintenance**: Who will maintain this code long-term?
   - Code that requires long-term maintenance needs high readability and documentation
   - Consider generating explanations and documentation alongside code

5. **Integration**: How does this code integrate with the broader system?
   - Clearly defined interfaces help manage integration points
   - Explicit contracts between components reduce integration issues

6. **Security**: What are the security implications?
   - Security-sensitive code requires explicit security review
   - Ask AI to explicitly address security considerations in its implementation

7. **Performance**: Are there performance constraints?
   - Specify performance requirements upfront
   - Verify with benchmarking or profiling

8. **Testing Strategy**: How will the code be tested?
   - Consider test-driven approaches where tests are created first
   - Use AI to generate comprehensive test suites

These decision frameworks help developers make informed choices about when and how to leverage AI assistance, ensuring appropriate safeguards while maximizing productivity benefits.
</context>

<context name="anti_patterns" priority="medium">
## Anti-Patterns and Common Pitfalls

Understanding and avoiding common mistakes when working with AI coding assistants is crucial for maintaining code quality and security.

### 1. Uncritical Acceptance of Generated Code [AP-AICODE-001]

**Problem:**
Accepting and using code generated by AI assistants without proper review or verification, assuming the code is correct, secure, and optimal because it looks plausible.

**Example:**
```javascript
// ❌ AI generated this authentication middleware
const authenticate = (req, res, next) => {
  const token = req.headers.authorization;
  
  if (!token) {
    return res.status(401).json({ message: 'Authentication required' });
  }
  
  try {
    // Missing token validation, no expiration check, no signature verification
    const decoded = jwt.decode(token);
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({ message: 'Invalid token' });
  }
};
```

**Why It Fails:**
- Generated code often contains subtle bugs or security vulnerabilities
- AI may use outdated or deprecated approaches learned from training data
- Missing validation for edge cases or error conditions
- AI has no understanding of your specific security requirements
- Code may appear functional in simple tests but fail in production scenarios

**Better Approach:**
```javascript
// ✅ Properly reviewed and secured authentication middleware
const authenticate = (req, res, next) => {
  // Check for authorization header using constants to prevent typos
  const authHeader = req.headers.authorization;
  
  // Validate header format and extract token
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ 
      message: 'Authentication required. Bearer token missing.'
    });
  }
  