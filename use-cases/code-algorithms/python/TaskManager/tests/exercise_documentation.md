## Task Manager — Final Submission

### 1. Initial vs Final Understanding

**where i started:**

honestly when i first opened the project i just saw a bunch of random python files and had no idea how they connected. i thought all the files ran together every single time you run the app like one big thing. i also thought models.py was about selecting or clicking which task is more important — like a UI thing. i called the testing framework "flash" instead of unittest 😭 and i had no idea what the difference was between a built-in import and a custom import. i just thought all imports were files you had to create yourself.

**where i ended up:**

now i understand that each file has ONE specific job and they talk to each other through imports. the whole thing follows a layered pattern:

```
user types command
        ↓
cli.py reads it        ← the front door
        ↓
task_manager.py acts   ← the brain
        ↓
storage.py saves       ← the filing cabinet
        ↓
models.py defines      ← the blueprint

helpers only when needed:
task_parser.py    → translates text into tasks
task_priority.py  → scores and ranks tasks
task_list_merge.py → syncs two task lists
```

i also now understand that not every file runs every time. helper files only get called when a specific command needs them. skipping a file that IS needed breaks everything — but not every file is needed every time.

---

### 2. Most Valuable Insights From Each Prompt

**Exercise 1 — Understanding Project Structure:**

the most valuable thing i learned here was the difference between built-in imports and custom imports. i used to think all imports were files you created yourself. now i know that things like `argparse` and `datetime` come FREE with python — they're already there when you install it. custom imports like `from models import Task` are files YOUR project created.

the second most valuable thing was understanding what models.py actually does. i thought it was about selecting priority — but it's actually a blueprint. it defines what a task IS before anything else happens.

**Exercise 2 — Finding Feature Implementation:**

the most valuable thing here was understanding the difference between a `.py` file and a `.csv` file. i thought task_export.csv was the file i needed to create. now i know:

- `task_export.py` = the tool/machine you build once
- `my_tasks.csv` = the result that gets automatically generated when a user runs the command

i also learned that when adding a new feature you don't always build from scratch. you read existing files like `storage.py` to understand the pattern and then copy that pattern for your new feature.

**Exercise 3 — Domain Model:**

the most valuable thing here was understanding the scoring system and how business rules hide inside code. those `if` statements in `task_priority.py` aren't just random conditions — they're actual business decisions someone made. like:

```
overdue → +35 points  (missing deadlines is serious)
DONE    → -50 points  (finished tasks need no attention)
```

i also finally understood the difference between TaskStatus and TaskPriority properly:

- TaskStatus = where is the task RIGHT NOW in its journey
- TaskPriority = how important is this task compared to others

---

### 3. My Approach To Implementing The New Business Rule

if i had to implement the CSV export feature today here is exactly how i would approach it:

**step 1 — read before touching anything**
open `models.py` and write down every single field a task has. those become my CSV column headers:

```
id, title, description, priority,
status, due_date, tags, created_at,
updated_at, completed_at
```

**step 2 — create `task_export.py`**
this is the new file that handles all CSV writing logic. it's the photocopy machine. build it once and it works every time someone runs the export command.

**step 3 — modify `task_manager.py`**
add a method called `export_to_csv()` that gets all tasks from storage and passes them to task_export.py. i would find where `get_all_tasks()` already lives and add my new method nearby so the code stays organised.

**step 4 — modify `cli.py`**
add the export command following the exact same pattern as existing commands like `stats` or `list`. the user should be able to type:

```
python cli.py export --filename "my_tasks.csv"
```

**step 5 — create `test_task_export.py`**
write tests that follow the same pattern as `test_task_manager.py`. test that the file gets created, that the columns are correct, and that the data matches what's in storage.

---

### 4. Strategies I've Developed For Approaching Unfamiliar Code

these are things i will actually do next time i open a codebase i've never seen before:

**look at file names first before reading any code**
file names tell you a lot. storage.py obviously stores things. task_parser.py obviously parses tasks. don't dive into code immediately — read the map first.

**find the entry point first**
always ask: where does this program START? for this project it's `cli.py` for users and `python -m unittest discover tests` for developers. once you know where it starts you can follow the flow.

**read the imports at the top of each file**
imports show you exactly which files talk to each other. if `task_manager.py` imports from `models.py` and `storage.py` — that tells you those three files are connected.

**search for keywords before writing anything**
before adding a new feature search the codebase for words like `export`, `csv`, `save`, `write`, `open(` — maybe someone already built what you need or something close to it.

**plan on paper before touching code**
i learned this from the CSV exercise. write down which files you'll modify and which new files you'll create BEFORE writing a single line of code. it saves a lot of confusion.

**be honest about what you don't understand**
i started adding "what i still don't understand" to every findings document. this is actually really useful because it shows you exactly what to google or ask about next. knowing what you don't know is a skill on its own.

---

### What I Still Don't Understand Overall

- i understand the flow of the whole system but i still haven't seen what actual CSV writing code looks like inside task_export.py — i know the plan but not the syntax yet
- i know how to READ imports but i don't fully understand yet how python actually FINDS the file when you import it — like what if the file is in a different folder
- i understand the scoring rules but i don't know who in a real company decides what the numbers should be and how developers know what rules to code
- i still want to understand what happens when two tasks have the exact same score — which one comes first and why

Exercise: Algorithm Deconstruction Challenge

Algorithm 1: Task Priority Sorting Algorithm

### What The Algorithm Does In My Own Words

okay so basically this algorithm is like a scoring system for tasks. it looks at each task and gives it a number based on how important and urgent it is. the higher the number the more important the task. tasks with the highest scores appear first in the list so you always see the most important stuff at the top.

it's basically a reminder system that automatically ranks your tasks for you based on multiple factors — not just one thing like priority alone.

---

### The 5 Sections And What Each Does

```
SECTION 1 — Base Priority Score
looks at the priority level of the task
converts it into a base score:
  LOW    = 1 × 10 = 10 points
  MEDIUM = 2 × 10 = 20 points
  HIGH   = 4 × 10 = 40 points
  URGENT = 6 × 10 = 60 points

SECTION 2 — Due Date Factor
checks if the task has a due date
if YES → adds urgency points:
  overdue        → +35 points
  due today      → +20 points
  due in 2 days  → +15 points
  due this week  → +10 points
if NO due date → skips entirely, no crash

SECTION 3 — Status Penalty
removes points if task is finished:
  DONE   → -50 points
  REVIEW → -15 points
this pushes completed tasks to the bottom

SECTION 4 — Tag Boost
checks if task has special tags:
  "blocker", "critical", "urgent" → +8
regular tags like "shopping" → nothing

SECTION 5 — Recency Boost
checks when task was last updated
updated today → +5 points
not updated recently → no boost
rewards tasks being actively worked on
```

---

### My Concrete Example With Numbers

```
Task: "Fix login bug"
priority   = HIGH
due_date   = tomorrow
status     = TODO
tags       = ["critical"]
updated_at = today

SECTION 1: HIGH = 4 × 10  = 40 points
SECTION 2: tomorrow = +15 = 15 points
SECTION 3: TODO = no penalty = 0
SECTION 4: critical tag = +8 = 8 points
SECTION 5: updated today = +5 = 5 points

TOTAL = 40 + 15 + 8 + 5 = 68 points
→ goes near the TOP of the list
```

---

### How The Three Functions Work Together

```
get_top_priority_tasks(tasks, limit=5)
  → calls sort_tasks_by_importance()
        → calls calculate_task_score()
           for EVERY task
        → sorts all scores highest first
  → returns only top 5 tasks

think of it like a competition:
calculate_task_score()     = judges scoring
sort_tasks_by_importance() = ranking everyone
get_top_priority_tasks()   = announcing top 5
```

---

### What Confused Me And What Clicked

what confused me was the calculations — the code just says "calculate" without showing a real example. i didn't understand HOW to actually do the math until i had a proper scenario with real values.

once i had a concrete example with actual numbers like HIGH priority + tomorrow due date + critical tag — the whole thing clicked immediately. i could see exactly where each number came from and how they added up.

the key insight was realising it's just addition and subtraction — each section either adds or removes points and you just total them up at the end.

---

### Edge Cases I Discovered

```
Edge case 1 — No due date:
algorithm skips section 2 entirely
does NOT crash
task just gets no urgency bonus

Edge case 2 — URGENT + DONE:
URGENT = 60 points
DONE   = -50 points
total  = 10 points → goes to BOTTOM
even urgent tasks drop when completed

Edge case 3 — Task not updated recently:
loses the +5 recency boost
slowly drops in the rankings
forgotten tasks naturally lose priority
```

---

### What I Still Don't Understand

- i understand the scoring with a scenario but i still find it hard to read the raw code and calculate without first writing out the scenario myself — is that a normal way to approach code or do experienced developers just read it directly?
- i understand that scores change over time but i don't know how often the scores get recalculated — does it happen automatically or only when someone runs a command?
- i get that the tag boost only works for "blocker", "critical" and "urgent" tags — but who decided those specific words and how would a developer add more special tags in the future?
- i calculated 68 points for my example — but i don't know if 68 is considered high or low compared to other tasks without seeing the full list

## Algorithm 2 — Task Text Parser

### What The Algorithm Does In My Own Words

basically this algorithm reads whatever the user types in plain text and sorts it out into the correct fields of a task. it looks for special symbols like @, ! and # and uses them as markers to know what information goes where. once it finds and extracts everything it creates a proper structured task object that the rest of the system can use.

think of it like a form that fills itself in automatically based on clues the user left in their text.

---

### The Key Symbols And What They Mean

```
@word   → adds a TAG to the task
          example: @shopping → tag = "shopping"

!N or 
!name   → sets the PRIORITY level
          example: !2 or !high → priority = HIGH
          
          valid options:
          !1 or !low    → LOW priority
          !2 or !medium → MEDIUM priority
          !3 or !high   → HIGH priority
          !4 or !urgent → URGENT priority

#word   → sets the DUE DATE
          example: #tomorrow → due tomorrow
          
          valid options:
          #today, #tomorrow, #next_week
          #monday, #tuesday, #wednesday
          #thursday, #friday
          or a specific date like #2026-06-01
```

---

### The 5 Steps The Algorithm Follows

```
STEP 1 — Set default values
before doing anything, set safe fallbacks:
  title    = full text the user typed
  priority = MEDIUM (default)
  due_date = None (default)
  tags     = [] empty list (default)

STEP 2 — Find and extract priority
looks for ! symbols in the text
finds "!high" → converts to TaskPriority.HIGH
removes "!high" from the title
if TWO priorities typed → first one wins

STEP 3 — Find and extract tags
looks for @ symbols in the text
finds "@shopping" → adds "shopping" to tags
removes "@shopping" from the title
can find multiple tags at once

STEP 4 — Find and extract due date
looks for # symbols in the text
finds "#tomorrow" → calculates tomorrow's date
removes "#tomorrow" from the title
converts weekday names to actual dates

STEP 5 — Clean up and create task
removes any leftover double spaces
creates a proper Task object with:
  title    = cleaned up text
  priority = extracted or default
  due_date = extracted or None
  tags     = extracted or empty
```

---

### My Concrete Example With Real Values

```
USER TYPES:
"Buy milk @shopping !high #tomorrow"

STEP 1 — defaults:
title    = "Buy milk @shopping !high #tomorrow"
priority = MEDIUM
due_date = None
tags     = []

STEP 2 — extract priority:
finds "!high"
priority = HIGH
title    = "Buy milk @shopping #tomorrow"

STEP 3 — extract tags:
finds "@shopping"
tags     = ["shopping"]
title    = "Buy milk #tomorrow"

STEP 4 — extract date:
finds "#tomorrow"
due_date = 2026-05-29
title    = "Buy milk"

STEP 5 — clean up:
title    = "Buy milk" ← clean, no extra spaces

FINAL TASK OBJECT:
  title    = "Buy milk"
  priority = HIGH
  due_date = 2026-05-29
  tags     = ["shopping"]
```

---

### Edge Cases I Discovered

```
Edge case 1 — No symbols typed:
"Buy milk"
→ title    = "Buy milk"
→ priority = MEDIUM (default kicks in)
→ due_date = None (default kicks in)
→ tags     = [] (default kicks in)
does NOT crash — defaults handle it

Edge case 2 — Two priorities typed:
"Buy milk !high !low"
→ FIRST one wins → priority = HIGH
→ !low gets completely ignored

Edge case 3 — Leftover spaces after extraction:
"Buy milk  @shopping  !high"
after removing symbols → "Buy milk  "
re.sub cleans it up → "Buy milk"
no messy double spaces in final title
```

---

### What Confused Me And What Clicked

what confused me at first was the symbols — i thought @ was related to status and ! was related to completed_at. that was wrong.

once i saw the actual examples in the code comments it clicked immediately:
- @ = tag
- ! = priority
- # = due date

the other thing that confused me was what happens when no symbols are typed. i thought it would return nothing but actually the default values handle that — priority becomes MEDIUM automatically, due_date stays None, tags stay empty.

---

### What I Still Don't Understand

- i understand what `re.findall` is doing generally but i don't understand the actual pattern inside it like `r'\s!([1-4]|urgent|high|medium|low)\b'` — what do all those characters mean?
- i get that the first priority wins when two are typed but i don't understand HOW the code knows to only take the first one — what does `[0]` actually do technically?
- i understand the algorithm extracts the date word like "tomorrow" but i don't fully understand how it converts that word into an actual calendar date — like what is `timedelta(days=1)` doing exactly?
- what happens if someone types a symbol in an unexpected way like `!!high` or `@@shopping` — does it still work or does it break?
Prompt 1
I'm trying to understand how task creation 
works in our Python codebase.

This feature seems to handle creating tasks 
in different files and formats — taking what 
the user types and turning it into a saved task.

Here are the key files involved:
1. cli.py — the front door, where user 
   types the command
2. task_manager.py — the brain, coordinates 
   everything
3. models.py — defines what a Task looks like
4. storage.py — handles saving and loading tasks

Here's the key code from task_manager.py:

def create_task(self, title, description="", 
               priority_value=2,
               due_date_str=None, tags=None):
    priority = TaskPriority(priority_value)
    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(
                due_date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format.")
            return None
    task = Task(title, description, 
                priority, due_date, tags)
    task_id = self.storage.add_task(task)
    return task_id

I'm particularly confused about how 
storage.py gets its information — since 
cli.py is the one where the user creates 
the task, how does the data travel all 
the way to storage.py?

Could you:
1. Explain what this code does simply
2. Walk me through execution when 
   user types:
   python cli.py create "Buy milk" 
   --priority 3 --due "2026-06-01"
3. Clarify how these files interact
4. Identify any external dependencies
5. Explain any complex code blocks
6. Provide a mental model I can use

Now The AI Response To Prompt 1
1. What This Code Does Simply
This code is like a form processor:

takes what the user typed
validates it (checks date format)
builds a proper Task object
hands it to storage to save


2. Answering Your Specific Confusion

"how does storage.py get its info
since cli.py creates everything?"

Here's exactly how the data travels:
STEP 1 — User types in terminal:
python cli.py create "Buy milk" 
--priority 3 --due "2026-06-01"

STEP 2 — cli.py receives it:
title    = "Buy milk"
priority = 3
due      = "2026-06-01"

cli.py calls:
task_manager.create_task(
    "Buy milk", "", 3, "2026-06-01"
)
→ passes the values TO task_manager

STEP 3 — task_manager.py processes it:
converts "3" → TaskPriority.HIGH
converts "2026-06-01" → datetime object
checks date format → valid ✅
builds Task object:
  title    = "Buy milk"
  priority = HIGH
  due_date = 2026-06-01
  status   = TODO (default)

task_manager calls:
self.storage.add_task(task)
→ passes the Task object TO storage

STEP 4 — storage.py receives Task object:
adds it to self.tasks dictionary
calls self.save()
converts Task → JSON
writes to tasks.json file
permanently saved ✅

STEP 5 — confirmation travels back up:
storage returns task_id to task_manager
task_manager returns task_id to cli.py
cli.py prints:
"Created task with ID: abc123"
So storage.py doesn't go GET the info — the info gets passed DOWN to it like a relay race:
cli.py 
  → passes to task_manager.py
        → passes to storage.py
              → saves to tasks.json

3. How The Files Interact
cli.py
  imports TaskManager from task_manager.py
  calls task_manager.create_task()

task_manager.py
  imports Task, TaskPriority from models.py
  imports TaskStorage from storage.py
  builds Task using models.py blueprint
  saves using storage.py

storage.py
  imports Task from models.py
  writes to tasks.json

models.py
  imported by everyone
  doesn't import from any project file
  it's the foundation everything builds on

4. Mental Model
Think of it like a relay race:
cli.py          = starter, fires the gun,
                  passes the baton

task_manager.py = middle runner, 
                  processes and passes on

storage.py      = final runner, 
                  crosses the finish line
                  (saves to disk)

models.py       = the rulebook everyone 
                  reads before running





# **Exercise: Error Diagnosis Challenge**

**1. Off by One Error (Python)**

**Error Diagnosis Challenge
IndexError: list index out of range**

**Error Description In My Own Words**

okay so basically Python tried to access a position in a list that doesn't exist. like imagine a shopping list with 3 items on it — positions 0, 1, 2. if someone asks for position 5 there's nothing there. when YOU ask for something that doesn't exist you just say "nothing there" and move on. but Python doesn't do that — it crashes and throws this error:

`IndexError: list index out of range`

it's Python's way of saying:

> "you asked me for a position that
doesn't exist in this list
so i don't know what to do"
> 

one important thing i learned — Python counts from 0 not 1. so a list with 5 items has valid positions 0, 1, 2, 3, 4. trying to access position 5 crashes even though the list HAS 5 items.

---

**Reading The Stack Trace**

the stack trace is like a trail of breadcrumbs showing where Python was when it crashed:

`line 25: main()
→ this just starts everything

line 17: print_inventory_report(items)
→ this passes the list to the function

line 10: for i in range(len(items)):
         print(items[i]['name'])
→ THIS is where the crash actually happens ⚠️`

the most important thing i learned about stack traces — always read from the BOTTOM up. the bottom line is closest to where the actual crash happened.

---

**Root Cause**

the crash happened at line 10:

python

`for i in range(len(items)):
    print(items[i]['name'])`

the variable `i` became a number that was too big for the list. three things could cause this:

`Cause 1 — list is empty:
items = []
nothing to access at all
i tries to access position 0
but there's nothing there

Cause 2 — list got shorter while looping:
started with 5 items
something deleted one mid-loop
now i=4 but only 4 items exist
position 4 doesn't exist anymore

Cause 3 — off by one:
Python counts from 0 not 1
list of 5 items → valid positions 0,1,2,3,4
position 5 = CRASH
easy mistake to make`

---

**My Suggested Fix**

**before — unsafe:**

python

`for i in range(len(items)):
    print(items[i]['name'])`

**after — safe:**

python

`for item in items:
    print(item['name'])`

by using `for item in items` directly Python handles all the counting itself. you don't need `i` at all. Python never tries to access a position that doesn't exist because it's not using positions — it's just going through each item one by one.

also add a safety check before the loop:

python

`if not items:
    print("No items found")
else:
    for item in items:
        print(item['name'])`

this catches the empty list case before it even tries to loop.

---

**Step By Step Debugging Approach**

if i saw this error in real code here's how i'd investigate:

`STEP 1 — print the list length
print(f"Number of items: {len(items)}")
→ tells me how many items actually exist

STEP 2 — check if list is empty
if not items:
    print("List is empty!")
→ catches the most common cause

STEP 3 — print what position caused crash
add inside the loop:
print(f"Trying position: {i}")
→ shows exactly which number caused crash

STEP 4 — switch to safer loop style
for item in items:
    print(item['name'])
→ lets Python handle counting
→ never goes out of range`

---

**What I Learned To Prevent This In Future**

- Python counts from 0 not 1 — a list with 5 items has positions 0 to 4, NOT 1 to 5
- always use `for item in items` instead of `for i in range(len(items))` when you just need to loop through a list
- always check if a list is empty before trying to access items in it
- read stack traces from the BOTTOM UP — the bottom line is always closest to the actual problem
- the error message itself is a clue — `IndexError` always means a position problem in a list

### What I Still Don't Understand

- i understand the fix but i don't fully understand WHEN you would actually NEED to use `range(len(items))` — like is there ever a good reason to use it?
- i get that the stack trace shows the trail but i don't fully understand how to read it when there are 10 or 20 lines instead of just 3
- i understand this specific error but i wonder what other common Python errors look like — are they all read the same way?
- i fixed the loop but i still don't fully understand what `items[i]['name']` means — specifically the `['name']` part at the end

# **Root Cause Analysis**

### IndexError: list index out of range

### What The Error Means In My Own Words

okay so basically Python tried to access a position in a list that doesn't exist and crashed. it's like a shopping list with 3 items — positions 0, 1, 2. if you ask for position 3 there's nothing there. when a human asks for something that doesn't exist they just say "nothing there" and move on. Python doesn't do that — it crashes and throws:

`IndexError: list index out of range`

one important thing — Python counts from 0 not 1. so a list with 3 items has valid positions 0, 1, 2. trying to access position 3 crashes even though there ARE 3 items.

---

### Understanding The Stack Trace

i was confused about this at first — i thought the numbers 25, 17, 10 were item numbers in the list. they're NOT. they are LINE NUMBERS in the code file. like page numbers in a book.

`line 25 → this is where main() is written
            in the code file
line 17 → this is where 
            print_inventory_report(items) 
            is written
line 10 → this is where the actual 
            crash happens

the stack trace is just showing which 
lines Python visited before crashing
read it from BOTTOM UP to find 
where the problem actually is`

---

### Chain Of Events Leading To Crash

`STEP 1: Python starts at line 25
        runs main()

STEP 2: main() reaches line 17
        calls print_inventory_report(items)
        passes the list along

STEP 3: function starts at line 10
        calculates len(items)
        let's say 3 items exist
        range(3) = 0, 1, 2

STEP 4: loop runs:
        i = 0 → items[0] works ✅
        i = 1 → items[1] works ✅
        i = 2 → items[2] works ✅
        i = 3 → items[3] CRASH ❌
        position 3 doesn't exist
        Python stops completely`

---

### Root Cause

the problem is this specific pattern:

python

`for i in range(len(items)):
    print(items[i]['name'])`

this is called an anti-pattern in Python — it works sometimes but causes problems. the variable `i` becomes a number too big for the list and Python crashes trying to access a position that doesn't exist.

three things that could cause this:

`Cause 1 — list is empty:
items = []
nothing to access at all

Cause 2 — list got shorter mid-loop:
started with 5 items
something removed one during the loop
i goes too far

Cause 3 — Python counts from 0:
list of 3 items = positions 0, 1, 2
trying position 3 = CRASH
easy mistake to make`

---

### My Suggested Fix

python

`# BEFORE — unsafe:
for i in range(len(items)):
    print(f"Item: {items[i]['name']} 
          Quantity: {items[i]['quantity']}")

# AFTER — safe:
for item in items:
    print(f"Item: {item['name']} 
          Quantity: {item['quantity']}")`

also add an empty list check:

python

`def print_inventory_report(items):
    if not items:
        print("No items in inventory")
        return
    for item in items:
        print(f"Item: {item['name']} 
              Quantity: {item['quantity']}")`

by using `for item in items` directly Python handles all the counting itself. you don't need `i` at all and it never goes out of range.

---

### What I Learned

- line numbers in a stack trace are locations in the CODE FILE not item numbers in a list — i got confused about this at first
- Python counts from 0 not 1 — a list with 5 items has valid positions 0 to 4 not 1 to 5
- always use `for item in items` instead of `for i in range(len(items))` — it's safer and cleaner
- always check if a list is empty before looping through it
- read stack traces from BOTTOM UP — the bottom line is always closest to the actual crash
- the code itself wasn't necessarily wrong — it just needed better formatting and a safer loop pattern

---

### What I Still Don't Understand

- i understand the fix but i still don't know WHEN you would actually need to use `range(len(items))` — is there ever a good reason to use it?
- i get that `items[i]` gets a position but i don't fully understand what `['name']` does at the end — like why do you need those square brackets again after already using square brackets?
- i understand this specific error but i wonder what other common Python errors look like and whether you read them the same way
- i now know line numbers are code locations but how do i find line 10 quickly in a real file with hundreds of lines?
