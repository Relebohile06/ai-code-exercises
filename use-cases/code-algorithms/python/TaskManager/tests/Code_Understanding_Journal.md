Code Understanding Journal

Part 1 — Understanding a Specific Feature

---

Files Related To Task Creation And Status Updates

The main files involved in task creation and status updates are:

- "cli.py"
- "task_manager.py"
- "models.py"
- "storage.py"
- "task_parser.py"
- "task_priority.py"
- "task_list_merge.py"

---

What Each File Does

"cli.py"

This file acts as the front door of the application.

It:

- reads commands typed by the user in the terminal
- parses arguments
- sends instructions to the correct functions

Example:

python cli.py create "Buy milk"

The user interacts with the system through this file.

---

"task_manager.py"

This is the coordinator or brain of the application.

It handles:

- task creation
- task updates
- status changes
- validation
- business logic

This file connects the user commands to storage and task models.

---

"models.py"

This file defines the structure of a Task.

It acts like a blueprint/template that describes:

- task fields
- priority levels
- statuses
- timestamps

This file is a core dependency because most other files rely on it.

---

"storage.py"

This file handles persistence.

It:

- saves tasks into "tasks.json"
- loads tasks from "tasks.json"
- converts Task objects into JSON
- reconstructs JSON back into Task objects

This file works like a translator between Python objects and disk storage.

---

"task_parser.py"

This file handles natural language task parsing.

It converts free-form text into structured task data.

Example:

"Buy milk @shopping !high #tomorrow"

gets transformed into a properly structured Task object.

This file is only used when natural language parsing is needed.

---

"task_priority.py"

This file handles task scoring and sorting.

It:

- calculates task importance scores
- ranks tasks by importance
- returns top-priority tasks

The score depends on:

- priority level
- due dates
- tags
- task status
- update recency

This file affects how tasks are displayed and prioritized.

---

"task_list_merge.py"

This file combines separate task lists together while avoiding duplicates or data loss.

It is only used when task lists need to be merged.

---

Main Components Involved In Task Creation/Updates

The main components involved are:

Component| Responsibility
"cli.py"| User interaction
"task_manager.py"| Coordination and business logic
"models.py"| Task blueprint/data structure
"storage.py"| Saving/loading data
"task_parser.py"| Natural language parsing
"task_priority.py"| Task scoring/sorting

The application follows a layered architecture where each file has one main responsibility.

This is an example of:

- separation of concerns
- modular design
- layered architecture

---

Execution Flow When A Task Is Created

Direct Task Creation Flow

Step 1 — User enters a command

Example:

python cli.py create "Buy milk" -p 2 -d "2026-06-01"

---

Step 2 — "cli.py" parses arguments

"cli.py":

- reads the command
- extracts the values
- calls "TaskManager.create_task()"

---

Step 3 — "task_manager.py" validates and coordinates

"task_manager.py":

- validates the date format
- processes priority values
- prepares task creation

---

Step 4 — "models.py" creates the Task object

A new Task object is created with:

- auto-generated UUID
- title
- priority
- due date
- default status ("TODO")
- created_at timestamp
- updated_at timestamp
- completed_at = None

---

Step 5 — "storage.py" saves the task

"TaskStorage.add_task()":

- stores the task in memory
- calls "save()"

---

Step 6 — "TaskEncoder" converts Task → JSON

The custom JSON encoder converts:

- Enums → values
- datetime objects → ISO strings

Examples:

TaskPriority.HIGH → 3

datetime → "2026-05-27T10:30:00"

---

Step 7 — Data written into "tasks.json"

The task data is written permanently into "tasks.json".

The application rewrites the full file whenever changes occur.

---

Step 8 — Confirmation returned to user

"cli.py" prints:

Created task successfully

---

Optional Parser Path

The application can also use a natural language parsing path.

Flow:

User Input
    ↓
cli.py
    ↓
task_parser.py
    ↓
task_manager.py
    ↓
storage.py

This allows plain text commands to become structured tasks automatically.

---

Execution Flow When Updating Task Status

Status Update Flow

Step 1 — User enters command

Example:

python cli.py status abc123 done

---

Step 2 — "cli.py" calls TaskManager

"cli.py" calls:

TaskManager.update_task_status()

---

Step 3 — Status converted into Enum

Example:

"done" → TaskStatus.DONE

---

Step 4 — Special DONE case handled

If the status is "DONE":

"mark_as_done()" is called.

This:

- changes status to DONE
- sets completed_at timestamp
- updates updated_at timestamp

This is different from normal status updates because completion time must be recorded.

---

Step 5 — Storage saves the updated task

The updated task:

- gets converted into JSON
- gets written back into "tasks.json"

---

Step 6 — Non-DONE updates behave differently

For statuses like:

- TODO
- REVIEW
- IN_PROGRESS

only:

- status changes
- updated_at changes

"completed_at" remains unchanged.

---

How Data Is Stored And Retrieved

The application uses a dual-layer storage system.

---

Layer 1 — Memory Storage

Tasks are stored temporarily in:

self.tasks

This allows:

- fast access
- quick updates
- easier manipulation

---

Layer 2 — Disk Storage

Permanent storage exists inside:

tasks.json

This keeps tasks available even after the application closes.

---

Saving Process

When saving:

1. Task objects converted into JSON
2. Enums converted into values
3. datetime objects converted into strings
4. JSON written into "tasks.json"

This process is called:

serialization

---

Loading Process

When loading:

1. "tasks.json" is read
2. "TaskDecoder" reconstructs Task objects
3. JSON values converted back into Python types

Examples:

JSON Value| Python Type
""done""| "TaskStatus.DONE"
"3"| "TaskPriority.HIGH"
ISO datetime string| "datetime object"

This process is called:

deserialization

---

Interesting Design Patterns I Discovered

Separation Of Concerns

Each file handles one specific responsibility:

- "cli.py" → user interaction
- "task_manager.py" → coordination/business logic
- "models.py" → structure
- "storage.py" → persistence

This makes the application easier to maintain and debug.

---

Layered Architecture

The application follows a layered flow:

User
 ↓
cli.py
 ↓
task_manager.py
 ↓
models.py + storage.py
 ↓
tasks.json

Components communicate step-by-step instead of everything happening in one file.

---

Optional Helper Components

Some helper files only run when needed:

- "task_parser.py" → natural language parsing
- "task_priority.py" → task ranking/sorting
- "task_list_merge.py" → list synchronization

Core files like "models.py" are always imported because the entire system depends on them.

---

What I Learned

At first I thought all Python files automatically ran together whenever the application started.

Now I understand:

- files only run when imported or called
- imports connect the application together
- each file has a different responsibility

I also learned:

- the difference between built-in and custom imports
- how JSON serialization works
- how Task objects are saved and reconstructed
- how business rules affect application behavior

---

Part 2 — Task Prioritization System

---

My Initial Understanding vs What I Discovered

What I Thought At First

When I first looked at "task_priority.py", I understood the basic idea:

- tasks receive scores
- higher scores mean higher importance
- DONE tasks move lower in the list

But I did not understand:

- why specific numbers were chosen
- how scores change over time
- how the scoring system actually affects behavior

---

What I Discovered

The scoring system works like a point-based priority engine.

Base Priority Scores

LOW     = 1 × 10 = 10 points
MEDIUM  = 2 × 10 = 20 points
HIGH    = 4 × 10 = 40 points
URGENT  = 6 × 10 = 60 points

---

Additional Score Rules

Points Added

overdue               → +35
due today             → +20
due in 2 days         → +15
due this week         → +10
critical/blocker tag  → +8
updated today         → +5

Points Removed

DONE status           → -50
REVIEW status         → -15

---

Key Insights I Discovered

Insight 1 — Scores Tell A Story

Example:

URGENT      = 60
overdue     = +35
blocker tag = +8
updated     = +5

TOTAL = 108

This score represents a task that needs immediate attention.

The scoring system reflects business priorities.

---

Insight 2 — Scores Change Over Time

A task score is not fixed permanently.

For example:

- overdue penalties increase urgency
- recency boosts disappear after one day
- approaching deadlines increase scores

This means tasks naturally move up or down in importance over time.

---

Insight 3 — Calculation And Sorting Are Separate

I learned that:

- "calculate_task_score()" calculates scores
- "sort_tasks_by_importance()" only sorts

The sorting function does not contain business rules.

---

Insight 4 — Business Rules Live Inside The Score Calculator

If developers want new rules like:

TODO for 30 days → +20

that logic belongs inside:

calculate_task_score()

not inside the sorting function.

---

Misconceptions I Had

Misconception 1

I thought sorting logic and scoring logic were the same thing.

Now I understand:

- scoring decides importance
- sorting only orders the results

---

Misconception 2

I thought priority numbers were random.

Now I understand:

- larger gaps between HIGH and URGENT are intentional
- the system exaggerates higher priorities on purpose

---

Misconception 3

I thought scores stayed fixed forever.

Now I understand:

- scores evolve automatically based on time and activity

---

What I Still Don't Understand

- how Python loops through all tasks internally during score calculations
- how developers decide exact business rule values
- whether long-abandoned tasks eventually stop losing priority
- how new scoring rules would be implemented in actual Python syntax

---

Part 3 — Marking A Task Complete

---

Data Flow Diagram

USER TYPES:
python cli.py status abc123 done

        ↓

cli.py reads the command

        ↓

task_manager.py receives request

        ↓

storage.py retrieves task

        ↓

mark_as_done() executes

        ↓

status changes to DONE
completed_at timestamp created
updated_at timestamp updated

        ↓

storage.save() called

        ↓

TaskEncoder converts data to JSON

        ↓

tasks.json updated permanently

        ↓

cli.py confirms success

---

State Changes During Completion

Before

status       = IN_PROGRESS
completed_at = None
updated_at   = 2026-05-20T09:00:00

---

After

status       = DONE
completed_at = 2026-05-27T10:30:00
updated_at   = 2026-05-27T10:30:00

---

Potential Failure Points

Task Not Found

If the task ID does not exist:

- storage returns None
- the update cannot happen

---

Invalid Status

If a user enters:

doneee

instead of:

done

the status conversion may crash.

---

Corrupted JSON File

If "tasks.json" is corrupted:

- loading may fail
- tasks may become inaccessible

---

Save Failure

If saving fails:

- changes remain only in memory
- data may be lost after closing the app

---

How Persistence Works

The application saves permanently by:

1. storing tasks in memory
2. converting them into JSON
3. writing them into "tasks.json"

Saving flow:

Task object
    ↓
TaskEncoder
    ↓
JSON
    ↓
tasks.json

Loading flow:

tasks.json
    ↓
JSON
    ↓
TaskDecoder
    ↓
Task object

"storage.py" works in both directions like a translator.
