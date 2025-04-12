# Retrospective Formats and Templates

Different retrospective formats serve different purposes and contexts. This guide covers various formats, when to use them, and how to implement them effectively.

## Selecting the Right Format

Consider these factors when choosing a retrospective format:

- **Team maturity**: How experienced is the team with retrospectives?
- **Current challenges**: What specific issues need addressing?
- **Time available**: How much time can be allocated?
- **Emotional context**: What's the current team mood and dynamic?
- **Previous formats**: What formats have you used recently?

## Standard Formats

### 1. Start, Stop, Continue

A simple, effective format for teams at any stage.

**Best for:**
- New teams getting started with retrospectives
- Quick retrospectives (30 minutes or less)
- Teams needing clear, actionable outcomes

**Format:**
- **Start**: What should we begin doing that we don't do currently?
- **Stop**: What should we stop doing that isn't working?
- **Continue**: What is working well that we should keep doing?

**Implementation:**
1. Create three columns labeled "Start," "Stop," and "Continue"
2. Have everyone silently write items for each category (5-7 minutes)
3. Share and group similar items (5-10 minutes)
4. Discuss top items in each category (10-15 minutes) 
5. Select 1-2 items from each category to act on (5 minutes)

**Example Template:**
```markdown
# Sprint 24 Retrospective: Start, Stop, Continue

## Start
- Implement pair programming for complex features
- Add static code analysis to build pipeline
- Have daily sync-ups with the product team

## Stop
- Working on multiple tasks simultaneously
- Having unplanned mid-sprint scope changes
- Adding TODOs without tickets

## Continue
- Daily stand-ups at 9:30am
- PR reviews within 4 hours
- Technical documentation for new components

## Action Items
1. **Start**: Schedule pair programming for complex features
   - Owner: Alex
   - Due: Next sprint planning
   
2. **Stop**: Create "WIP limit" policy
   - Owner: Sarah
   - Due: Tomorrow's team meeting
   
3. **Continue**: Maintain current PR review schedule
   - Owner: Entire team
   - Due: Ongoing
```

### 2. The 4 Ls

A balanced reflection on the cognitive and emotional aspects of the work.

**Best for:**
- Teams with good psychological safety
- Mid-level retrospective maturity
- Capturing both emotional and factual aspects

**Format:**
- **Liked**: What did you enjoy or appreciate?
- **Learned**: What new insights or knowledge did you gain?
- **Lacked**: What was missing that would have helped?
- **Longed For**: What do you wish you had (skills, resources, etc.)?

**Implementation:**
1. Create four quadrants for each L
2. Silent brainstorming (5-8 minutes)
3. Round-robin sharing, placing notes in quadrants (10-12 minutes)
4. Identify patterns and vote on priorities (8-10 minutes)
5. Create action items addressing top concerns (5-10 minutes)

**Example Template:**
```markdown
# Release 3.5 Retrospective: The 4 Ls

## Liked
- Collaborative problem-solving sessions
- Clear feature specifications
- Support from the DevOps team
- Flexible work hours during crunch time

## Learned
- New techniques for state management
- How to optimize database queries
- Better ways to handle error states
- The importance of early API integration testing

## Lacked
- Clear prioritization for bug fixes
- Sufficient testing environments
- Consistent code reviewing standards
- Adequate documentation for legacy systems

## Longed For
- More cross-team knowledge sharing
- Earlier involvement in feature planning
- Better tooling for performance testing
- More time for technical debt reduction

## Action Items
1. Create knowledge sharing sessions (from Longed For)
   - Owner: Jamie
   - Due: End of month

2. Develop code review checklist (from Lacked)
   - Owner: Michael
   - Due: Next sprint

3. Document legacy systems incrementally (from Lacked)
   - Owner: Team rotation
   - Due: Ongoing (1 component per sprint)
```

### 3. Mad, Sad, Glad

An emotionally centered format that helps surface team feelings.

**Best for:**
- Teams experiencing emotional challenges
- Situations with interpersonal friction
- Building empathy and understanding

**Format:**
- **Mad**: What frustrated or angered team members?
- **Sad**: What disappointed team members?
- **Glad**: What made team members happy or proud?

**Implementation:**
1. Create three sections labeled "Mad," "Sad," and "Glad"
2. Silent writing (5 minutes)
3. Each person shares their notes, starting with "Glad" to set positive tone
4. Group similar items and discuss patterns (15 minutes)
5. Identify actions to address negative emotions and reinforce positive ones (10 minutes)

**Example Template:**
```markdown
# Q1 Project Retrospective: Mad, Sad, Glad

## Mad
- Last-minute requirement changes disrupted planned work
- External dependencies delayed key features
- Technical debt slowed development significantly
- Unclear decision-making processes caused rework

## Sad
- We missed our original release target
- User feedback wasn't incorporated early enough
- Team communication broke down during high-pressure periods
- Some quality issues made it to production

## Glad
- Team pulled together to meet adjusted deadline
- New automated testing saved significant time
- Customer feedback on completed features was positive
- We improved our estimation accuracy

## Root Causes
- Communication gaps between stakeholders
- Insufficient risk management for dependencies
- Technical debt accumulation over previous quarters

## Action Items
1. Implement change request process with impact assessment
   - Owner: Product Manager
   - Due: Two weeks

2. Schedule regular technical debt reduction time
   - Owner: Team Lead
   - Due: Next planning session

3. Create dependency risk assessment template
   - Owner: Project Manager
   - Due: End of month
```

### 4. Sailboat Retrospective

A visual metaphor that helps teams think about their journey.

**Best for:**
- Visual thinkers
- Mixed technical and non-technical teams
- Building shared understanding of goals and challenges

**Format:**
- **Wind (pushing)**: What's helping the team move forward?
- **Anchors (holding back)**: What's preventing progress?
- **Rocks (risks)**: What hazards might cause problems?
- **Island (goal)**: Where is the team trying to go?

**Implementation:**
1. Draw a sailboat on water with an island, wind, anchors, and rocks
2. Label each element and explain the metaphor
3. Have team add sticky notes to each area (10 minutes)
4. Discuss items in each area (15-20 minutes)
5. Prioritize: strengthening winds, lifting anchors, avoiding rocks (10 minutes)

**Example Template:**
```markdown
# H1 2025 Project Sailboat Retrospective

## Island (Our Goals)
- Successful launch of v2.0 platform
- 95% test coverage for core modules
- Reduced load time by 50%
- Improved user satisfaction scores

## Wind (Helping Us)
- Clear product roadmap
- New team members with specialized expertise
- Improved CI/CD pipeline
- Strong executive support

## Anchors (Holding Us Back)
- Legacy code that's difficult to modify
- Multiple competing priorities
- Unclear requirements for some features
- Incomplete documentation

## Rocks (Risks Ahead)
- Third-party API changes scheduled mid-project
- Team members' planned vacations during critical period
- Potential security vulnerabilities in dependencies
- Scaling challenges with increased user load

## Action Items
1. Create legacy code modernization plan
   - Owner: Senior Developer
   - Due: End of month
   
2. Develop priority framework with stakeholders
   - Owner: Product Owner
   - Due: Next week
   
3. Perform security audit of dependencies
   - Owner: Security Team
   - Due: Two weeks
```

### 5. What Went Well, What Didn't, What Questions, What Ideas

A comprehensive format that balances reflection with forward-thinking.

**Best for:**
- Experienced teams
- Complex projects
- Balancing problem identification with innovation

**Format:**
- **What Went Well**: Successes and positive aspects
- **What Didn't Go Well**: Challenges and issues
- **Questions**: Open questions and uncertainties
- **Ideas**: Suggestions and innovations for the future

**Implementation:**
1. Create four sections for each category
2. Silent writing in all categories (8-10 minutes)
3. Share items round-robin (10-15 minutes)
4. Dot voting to prioritize (5 minutes)
5. Deep-dive discussion on top items (15-20 minutes)
6. Create action items addressing each category (10 minutes)

**Example Template:**
```markdown
# Feature X Retrospective: 4W Format

## What Went Well
- Cross-team collaboration was smooth and productive
- Early user testing helped refine the design
- Performance goals were exceeded by 15%
- Documentation was thorough and helpful

## What Didn't Go Well
- Several bugs were found late in testing
- Deployment took longer than expected
- Some edge cases weren't identified during planning
- Team was stretched thin during final week

## Questions
- How can we identify edge cases earlier?
- Should we change our approach to estimation?
- Do we need more specialized testing resources?
- How can we better manage dependencies?

## Ideas
- Create an edge case brainstorming template
- Add buffer days for deployment activities
- Implement staged rollout for complex features
- Cross-train team members on specialized testing

## Action Items
1. Develop edge case identification worksheet
   - Owner: QA Lead
   - Due: Next sprint

2. Revise deployment checklist with timeboxes
   - Owner: DevOps Engineer
   - Due: End of week

3. Schedule cross-training sessions for testing
   - Owner: Team Lead
   - Due: Planning for next quarter
```

## Specialized Formats

### 1. Three Little Pigs

A risk-focused format using the fairy tale metaphor.

**Best for:**
- Projects with significant risk factors
- Teams needing to focus on robustness
- Preparing for challenging work ahead

**Format:**
- **Straw House**: Fragile elements that could easily break
- **Stick House**: Somewhat resilient elements that might fail under pressure
- **Brick House**: Solid elements that will withstand challenges

**Implementation:**
1. Explain the metaphor of the three houses
2. Have team identify elements in each category (10 minutes)
3. For straw and stick houses, brainstorm how to reinforce them (15 minutes)
4. For brick houses, identify how to leverage these strengths (10 minutes)
5. Create action plan for reinforcing vulnerable areas (10 minutes)

### 2. KALM (Keep, Add, Less, More)

A format focused on incremental adjustment rather than binary changes.

**Best for:**
- Mature teams making refinements
- Ongoing processes that need tuning
- Nuanced improvements rather than major changes

**Format:**
- **Keep**: What should stay exactly as it is?
- **Add**: What new elements should we introduce?
- **Less**: What should we reduce (but not eliminate)?
- **More**: What should we increase or emphasize?

**Implementation:**
1. Create four quadrants for the KALM categories
2. Team members add items to each quadrant (8 minutes)
3. Group similar items and identify patterns (10 minutes)
4. Discuss the balance between quadrants (10 minutes)
5. Select one or two items from each quadrant for action (5 minutes)

### 3. Timeline Retrospective

A chronological review of the project or period.

**Best for:**
- Longer projects or periods (multiple sprints)
- Understanding cause-and-effect relationships
- Recognizing patterns over time

**Format:**
- Create a timeline of key events, decisions, and milestones
- Mark high points, low points, and significant changes
- Analyze patterns and turning points

**Implementation:**
1. Draw a horizontal timeline covering the period
2. Team adds significant events to the timeline (15 minutes)
3. Mark emotional highs and lows along the timeline (5 minutes)
4. Identify patterns, cause-effect relationships (15 minutes)
5. Extract lessons learned and create forward-looking actions (15 minutes)

### 4. Lean Coffee

A democratically structured discussion format.

**Best for:**
- Teams that want to focus on their most pressing issues
- Situations where the key topics aren't clear in advance
- Teams that want to maximize engagement

**Format:**
- Team generates topics they want to discuss
- Votes to prioritize topics
- Timeboxed discussion of each topic in priority order

**Implementation:**
1. Each person writes topics they want to discuss (5 minutes)
2. Present all topics briefly (5 minutes)
3. Vote on topics using dot voting (3 minutes)
4. Discuss topics in order of votes, timeboxing each (5-10 minutes per topic)
5. After each topic, decide whether to continue or move on
6. Extract action items from discussions (5 minutes)

### 5. Six Thinking Hats

A comprehensive approach that examines issues from multiple perspectives.

**Best for:**
- Complex problems requiring thorough analysis
- Teams that tend to get stuck in one thinking mode
- Issues with both technical and emotional components

**Format:**
- **White Hat**: Focus on facts and data
- **Red Hat**: Express feelings and intuitions
- **Black Hat**: Identify risks and problems
- **Yellow Hat**: Explore benefits and opportunities
- **Green Hat**: Generate creative solutions
- **Blue Hat**: Process management and big picture

**Implementation:**
1. Select 1-3 key topics to analyze
2. For each topic, cycle through all six hats in sequence
3. Spend 3-5 minutes in each thinking mode
4. Capture insights from each perspective
5. Synthesize findings into comprehensive action items

## Remote/Distributed Retrospective Adaptations

Adaptations for teams working remotely:

### 1. Digital Tooling

Effective tools for remote retrospectives:

- **Digital whiteboards**: Miro, Mural, Jamboard
- **Retrospective platforms**: RetroTool, TeamRetro, Parabol
- **Collaboration tools**: Trello, Notion, Confluence
- **Voting tools**: Mentimeter, Poll Everywhere, Slido

**Implementation tips:**
- Pre-create boards with clear sections and instructions
- Use templates to speed up setup
- Test tools before the retrospective
- Have a backup plan if technology fails

### 2. Engagement Techniques

Methods to maintain engagement in remote settings:

- **Timers**: Use visible timers for activities to maintain focus
- **Round-robin**: Explicitly invite each person to speak in turn
- **Chat waterfall**: Everyone types responses but only presses Enter on cue
- **Breakout sessions**: Use smaller groups for deeper discussions
- **Check-in signals**: Use reaction buttons to gauge understanding

### 3. Asynchronous Components

Elements that can be done asynchronously to maximize synchronous time:

- **Pre-work**: Data gathering and individual reflection before the meeting
- **Silent writing**: Simultaneous input creation in shared documents
- **Voting**: Prioritizing items outside the main meeting
- **Follow-up**: Detailed action item definition after key decisions

**Example asynchronous sequence:**
1. Send reflection prompts 24 hours before meeting
2. Team members add items to digital board before meeting
3. Synchronous meeting focuses on discussion, not data gathering
4. Post-meeting voting on priority items
5. Action item details refined asynchronously

## Customizing Retrospective Formats

Guidelines for creating hybrid or custom formats:

### 1. Mixing Elements

Combine components from different formats to address specific needs:

- Start with basic Start/Stop/Continue but add a "Puzzles" section for open questions
- Use Timeline for data gathering but KALM for action creation
- Begin with Mad/Sad/Glad for emotional processing, then transition to Six Thinking Hats for solutions

### 2. Creating Themed Retrospectives

Design retrospectives around specific themes or metaphors:

- **Weather Report**: Sunny (positive), Cloudy (uncertain), Stormy (problematic), Rainbow (hopeful)
- **Health Check**: Vital signs, symptoms, diagnosis, treatment plan
- **Road Trip**: Route, vehicle, fuel, obstacles, destinations
- **Garden**: Seeds (ideas), soil (foundation), weeds (problems), harvest (outcomes)

### 3. Progressive Formats

Design retrospective series that build on each other:

**Sprint 1**: Focus on process issues using Start/Stop/Continue
**Sprint 2**: Examine technical practices using custom Technical Debt format
**Sprint 3**: Explore team dynamics using Mad/Sad/Glad
**Sprint 4**: Meta-retrospective on the retrospective process itself

## Retrospective Templates

Ready-to-use templates for common scenarios:

### 1. New Team Retrospective

```markdown
# New Team Formation Retrospective

## Setup
- Duration: 60 minutes
- Materials: Whiteboard/digital board, sticky notes, voting dots

## Format
1. **Check-in**: One word to describe your experience so far (3 min)

2. **What's Working**: What aspects of our teamwork are effective? (10 min)
   - Silent writing (3 min)
   - Sharing and grouping (7 min)

3. **Challenges**: What obstacles are we facing as a new team? (10 min)
   - Silent writing (3 min)
   - Sharing and grouping (7 min)

4. **Team Needs**: What do you need to be successful? (10 min)
   - Complete: "I can work most effectively when the team..."
   - Share and identify patterns

5. **Working Agreements**: What agreements would help us work better? (15 min)
   - Brainstorm potential agreements
   - Discuss and clarify
   - Check for consensus

6. **Next Steps**: Who will document and share our agreements? (5 min)

7. **Check-out**: One thing you're looking forward to in our work together (2 min)
```

### 2. Project Milestone Retrospective

```markdown
# Milestone X Retrospective

## Setup
- Duration: 90 minutes
- Materials: Timeline on wall/board, sticky notes, markers

## Format
1. **Project Recap**: Brief summary of milestone achievements and metrics (5 min)

2. **Timeline Creation**: (20 min)
   - Create a timeline from milestone start to completion
   - Mark key events, decisions, successes, and challenges
   - Add emotional indicators (high/low points)

3. **Pattern Analysis**: (15 min)
   - What patterns do we see across the timeline?
   - Which events had the biggest impact?
   - Where were turning points or pivots?

4. **Four Quadrants**: (30 min)
   - What went well? What didn't go well?
   - What was unclear? What surprised us?
   - Silent writing (5 min)
   - Sharing and discussion (25 min)

5. **Learning Extraction**: (15 min)
   - What key lessons should we carry forward?
   - What would we do differently next time?
   - What advice would we give to another team?

6. **Action Items**: (5 min)
   - What specific changes will we make for the next milestone?
   - Who owns each action item?
```

### 3. Production Incident Retrospective

```markdown
# Incident Retrospective: [Incident Name/ID]

## Incident Overview
- **Date/Time**: [When the incident occurred]
- **Duration**: [How long the incident lasted]
- **Impact**: [What services/users were affected]
- **Severity**: [Critical/Major/Minor]

## Timeline
- Create detailed timeline of the incident
- Include detection, response, mitigation, and resolution phases
- Note key decision points

## Five Whys Analysis
- **Problem Statement**: [Clear statement of what happened]
- **Why #1**: [First level cause]
- **Why #2**: [Deeper cause]
- **Why #3**: [Deeper cause]
- **Why #4**: [Deeper cause]
- **Why #5**: [Root cause]

## What Went Well
- [Aspects of detection, response, or resolution that were effective]

## What Needs Improvement
- [Areas where the response could have been better]

## Action Items
- **Prevention**: How to prevent this type of incident
- **Detection**: How to detect it faster next time
- **Response**: How to improve the response process
- **Documentation**: How to better document systems/processes

## Follow-up
- Who is responsible for each action item?
- When will progress be reviewed?
- How will we verify improvements?
```

### 4. Agile Transformation Retrospective

```markdown
# Agile Transformation Retrospective

## Current State Assessment
- What agile practices are working well?
- What practices are challenging to implement?
- What traditional practices are we still using?
- What metrics have changed since starting the transformation?

## Transformation Journey
- Create a timeline of the transformation to date
- Mark key milestones, changes, successes, and setbacks
- Note resistance points and breakthrough moments

## Transformation Impact
- **Team Level**: How has it affected team dynamics and delivery?
- **Organization Level**: How has it affected the broader organization?
- **Individual Level**: How has it affected individual roles and satisfaction?
- **Customer Level**: How has it affected customer outcomes?

## Scaling Questions (1-10)
- How well do we understand agile principles (not just practices)?
- How consistently do we apply agile practices?
- How much has our culture changed to support agility?
- How much customer value have we delivered compared to before?

## Next Steps
- What aspects of the transformation need more attention?
- What support do teams need to continue improving?
- What organizational impediments need to be addressed?
- What metrics should we track moving forward?

## Action Plan
- Short-term actions (next 1-2 sprints)
- Medium-term initiatives (next quarter)
- Long-term organizational changes (6-12 months)
```

By having a diverse toolkit of retrospective formats, facilitators can select the right approach for their team's specific needs, maturity level, and challenges. Regularly varying the format also helps keep retrospectives fresh and engaging, encouraging deeper insights and more effective outcomes.