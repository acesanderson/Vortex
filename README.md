# Vortex Architecture & Separation of Concerns Design Document

## System Overview: Siphon ↔ Vortex Separation

### Core Architectural Principle
**Siphon**: Passive intelligence and content discovery
**Vortex**: Active task management and productivity environment

This separation follows classic software architecture patterns:
- **Data Layer** (Siphon): Ingestion, processing, analysis, pattern recognition
- **Application Layer** (Vortex): User interaction, task lifecycle, productivity workflows

## Vortex: The Active Productivity Cockpit

### Primary Responsibilities

#### 🎯 **Active Task Management**
- **Manual todo creation** via CLI with rich syntax parsing
- **Task lifecycle management** (TODO → IN PROGRESS → BLOCKED → DONE)
- **Real-time interaction** with your current work context
- **Immediate feedback loops** for productivity decisions

#### 🔄 **Productivity Environment**
- **CLI while-loop interface** for sustained focus sessions
- **Context switching** between different work modes
- **Interactive task triage** from Siphon discoveries
- **Real-time status updates** and progress tracking

#### 📊 **Query & Categorization Engine**
- **Advanced filtering** by status, priority, tags, projects
- **Smart search** across tasks and context
- **Custom views** for different work contexts (coding, meetings, admin)
- **Reporting** on active work patterns

### Software Architecture Analysis

#### ✅ **Why This Separation Makes Sense**

**1. Single Responsibility Principle**
- **Siphon**: "I find and understand todos across your knowledge base"
- **Vortex**: "I help you actively manage and complete tasks right now"

**2. Temporal Boundaries**
- **Siphon**: Batch processing, periodic scans, historical analysis
- **Vortex**: Real-time interaction, immediate responses, active sessions

**3. User Interface Optimization**
- **Siphon**: Background processing, minimal UI (server/API focused)
- **Vortex**: Rich CLI experience, interactive workflows, human-optimized

**4. Data Flow Clarity**
```
[Knowledge Base] → [Siphon Discovery] → [Vortex Triage] → [Active Work] → [Completion] → [Siphon Analytics]
```

**5. Scaling Characteristics**
- **Siphon**: Heavy computational load, can run on dedicated server
- **Vortex**: Lightweight, responsive, local interaction

## Vortex Technical Architecture

### Core Components

#### 1. **CLI Interface Layer**
```python
class VortexCLI:
    """Primary user interface - optimized for speed and natural interaction"""
    
    def quick_add(self, task_input: str):
        """Natural language task creation with instant feedback"""
        
    def interactive_session(self):
        """While-loop productivity environment"""
        
    def query_tasks(self, filters: dict):
        """Advanced search and filtering"""
        
    def triage_siphon_discoveries(self):
        """Review and import Siphon-discovered todos"""
```

#### 2. **Task Lifecycle Engine**
```python
class TaskManager:
    """Handles active task state management"""
    
    def create_task(self, parsed_input: Task) -> UUID:
        """Create new task with rich metadata"""
        
    def update_status(self, task_id: UUID, status: Status):
        """Real-time status transitions"""
        
    def start_focus_session(self, task_id: UUID):
        """Begin active work tracking"""
        
    def batch_operations(self, task_ids: list[UUID], operation: str):
        """Bulk task management"""
```

#### 3. **Productivity Session Manager**
```python
class ProductivitySession:
    """Manages focused work periods and context switching"""
    
    def start_session(self, duration: int, focus_area: str):
        """Begin timed focus session with context"""
        
    def suggest_next_task(self, context: WorkContext):
        """AI-powered task suggestion for current session"""
        
    def handle_interruptions(self, interruption_type: str):
        """Graceful handling of context switches"""
```

#### 4. **Siphon Integration Layer**
```python
class SiphonConnector:
    """Handles bidirectional sync with Siphon discovery engine"""
    
    def fetch_discovered_todos(self) -> list[ToDoMetadata]:
        """Pull new todos discovered by Siphon"""
        
    def sync_completion_status(self, completions: list[UUID]):
        """Report completed tasks back to Siphon"""
        
    def request_contextual_analysis(self, task: Task) -> AnalysisResult:
        """Leverage Siphon's AI for task insights"""
```

### User Experience Design

#### CLI While-Loop Productivity Environment
```bash
# Enter Vortex productivity mode
$ vortex session

Welcome to Vortex Productivity Session
Current context: coding | energy: high | time: 09:30

[3 active tasks, 7 pending from Siphon]

> suggest next
AI: Based on your context, try "Refactor auth module" (Est: 45min, High priority)
Start this task? [y/N/list/context]: y

> focus 45
Starting 45-minute focus session on "Refactor auth module"
Timer: 44:32 remaining | Status: IN_PROGRESS
Break for interruption? [q/pause/status]: 

> status
Active: Refactor auth module (IN_PROGRESS, 12min elapsed)
Queue: 2 tasks | Siphon discoveries: 7 pending review
Context: deep work | No interruptions requested

> pause
Session paused. Resume with 'continue' or switch context with 'context'

> context admin
Switching to admin context...
Available admin tasks: [Review expense reports, Schedule 1:1s, Update project docs]

> quick add "Email team about holiday schedule" -p high #admin
Added: Email team about holiday schedule (HIGH, #admin)

> list #admin
Admin Tasks:
1. [ ] Email team about holiday schedule (HIGH) - just added
2. [ ] Review expense reports (MED) - due Friday
3. [ ] Schedule 1:1s (LOW) - this week

> complete 1
✓ Completed: Email team about holiday schedule
Syncing with Siphon... ✓

> exit
Session summary: 47min focused work, 1 task completed, 1 task added
```

#### Natural Language Task Creation
```bash
# Vortex's strength: instant, natural task capture
$ todo "follow up with sarah about the api changes, high priority, blocked on her response"

Parsed: 
- Task: "Follow up with Sarah about API changes"
- Priority: HIGH  
- Status: BLOCKED
- Context: "waiting on her response"
- Tags: [api, communication]

Add task? [Y/n]: y
✓ Added task #47 | Set reminder for 2 days? [y/N]: y
```

#### Siphon Discovery Triage
```bash
$ vortex review

Siphon discovered 12 new todos. Review for import:

1. "TODO: Add error handling to payment flow" 
   Source: /code/payments.py | Context: code | Est: 1h
   Import? [y/N/skip]: y

2. "Follow up on budget meeting notes"
   Source: /notes/2024-01-15.md | Context: admin | Est: 15min  
   Import? [y/N/skip]: y

3. "Buy groceries - milk, bread, eggs"
   Source: /notes/daily.md | Context: personal | Est: 30min
   Import? [y/N/skip]: n

Imported 2/3 discoveries. Run 'vortex list' to see active tasks.
```

## Data Architecture & Integration

### Shared Data Layer
```python
# PostgreSQL schema shared between Siphon and Vortex
class SharedTask(BaseModel):
    id: UUID
    source: Literal["siphon_discovered", "vortex_created", "vortex_imported"]
    siphon_metadata: Optional[ToDoMetadata]  # Rich discovery context
    vortex_metadata: Optional[VortexTaskData]  # Active management data
    sync_status: SyncStatus
```

### Integration Patterns

#### 1. **Discovery → Triage → Action**
```python
# Siphon discovers → Vortex imports → User acts
discovered_todo = siphon.discover_todo(content)  # Background process
vortex.present_for_triage(discovered_todo)       # User interaction
vortex.create_active_task(discovered_todo)       # Task activation
```

#### 2. **Completion Feedback Loop**
```python
# Vortex completion → Siphon learning
vortex.complete_task(task_id)                    # User action
siphon.record_completion(task_id, completion_context)  # Analytics update
siphon.update_ai_models(completion_pattern)     # Learning feedback
```

#### 3. **Contextual Intelligence**
```python
# Vortex requests → Siphon provides insights
context = vortex.get_current_work_context()     # What user is doing now
suggestions = siphon.analyze_context(context)   # AI-powered insights
vortex.present_suggestions(suggestions)         # User-friendly display
```

## System Benefits of This Architecture

### 🎯 **Clear Separation of Concerns**
- **Vortex never does content discovery** - focuses purely on active management
- **Siphon never does real-time interaction** - focuses purely on intelligence
- **Clean data contracts** between systems

### ⚡ **Performance Optimization**
- **Vortex optimized for responsiveness** - immediate CLI feedback
- **Siphon optimized for thoroughness** - deep content analysis
- **Independent scaling** - can optimize each system separately

### 🧠 **ADHD-Friendly Design**
- **Vortex provides immediate gratification** - quick task capture, instant feedback
- **Siphon provides background intelligence** - no cognitive overhead for discovery
- **Seamless context switching** - Vortex handles interruption patterns

### 🔄 **Natural Workflow Integration**
```
Daily Flow:
1. Work on code → Vortex suggests code-related tasks
2. Complete tasks → Siphon learns completion patterns  
3. Meeting ends → Siphon discovers action items → Vortex presents for triage
4. Context switch → Vortex adapts interface to new context
5. End of day → Siphon analyzes patterns → Vortex shows tomorrow's suggestions
```

## Implementation Roadmap

### Phase 1: Core Vortex (Independent)
- CLI task creation with natural language parsing
- Basic CRUD operations and task lifecycle
- PostgreSQL storage and simple querying
- Focus session management

### Phase 2: Productivity Environment
- While-loop interactive interface
- Context switching and work mode management
- Advanced filtering and custom views
- Time tracking and session analytics

### Phase 3: Siphon Integration
- Bidirectional data sync protocol
- Discovery triage workflow
- Completion feedback mechanisms
- Shared PostgreSQL schema

### Phase 4: Advanced Intelligence
- AI-powered task suggestions
- Context-aware productivity recommendations
- Pattern-based workflow optimization
- Cross-system analytics dashboard

## Conclusion

This architecture achieves clean separation while maximizing the strengths of each system:

- **Vortex**: Fast, interactive, human-optimized task management
- **Siphon**: Deep, intelligent, automated knowledge discovery
- **Together**: A complete productivity ecosystem that works with ADHD patterns

The key insight is that these are fundamentally different problems requiring different solutions, but with enormous synergy when properly integrated.

# Old README
This is a command line-based todo app inspired by linux pass and my llm scripts (like leviathan, tutorialize, ask, twig, etc.)

Motivation for this project:
- todo apps on the command line have existed for a long time, as well as implementations that store in a text-based format.
- my experience with the Mentor project showed the benefit of building my work environment as I do my daily work.
- I want to scale this idea to how I store, take notes, and complete tasks more broadly. Obsidian can be the GUI counterpart to this, and implementation is trivial given Obsidian being a wrapper around text files.
- This is "building the airplane as we are flying it" and a new approach to work. The idea here is that I spend 20% of my work day editing my work environment, with outsize performance benefits of 50%.

### Metalearning goals
- productivity theory, particulary in relation to what "works" for me -- i.e. NOT GTD, but zettelkasten/obsidian
 - lean into the WHY of certain tasks that get delayed or not completed
- click CLI framework

### Use cases
- command line:
 - create a task: `todo follow up with Zapier -p ! -s blocked`
 - create a task (NLP): `todo follow up with zapier, high priority, blocked, before next Tuesday`
- shell: every command available that you have through `todo ____` on command line
 - advanced commands like building projects, adding / accessing documents
- obsidian: rework todo in main todo (changes in that markdown file get realized in database); work with daily mds as well
- ad hoc scripting: attaching work flows / data flows etc. into the mix; importing todo list into various convenience functions + AI implementations 

### Architecture
- python package (with setup.py entry points)
- postgres backend (for saving tasks, metadata, and everything else)
- markdown file in obsidian vault. A main todo file mirrors tasks saved in postgres; allows for manual editing of the todo list. Can contain hidden uuids. Other markdown files keyed to particular days can be pre-populated.
- vector document store in the backend (postgres or chroma)

### Task creation syntax
task: natural language
tag: #work
project: +project
status: -s
- todo (default if not specified)
- doing or in-progress
- blocked / waiting for
- done or completed
priority: -p l/m/h OR ! !! !!!
date: -d YYYY-MM-DD

