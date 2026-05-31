# Exercise 1.1 — Behavior Analysis

## Testing the `calculate_task_score` Function

---

### What This Function Actually Does

okay so basically this function looks at a task and gives it a score. the higher the score the more important the task is. that score is then used to sort tasks so the most urgent ones show up at the top of your list.

it doesn't just look at one thing though — it looks at like 5 different things and adds or removes points based on each one.

---

### The Factors That Affect The Score

i had to read through the whole function carefully to find all of these:

**1. Priority Level — the base score**
this is the starting point. everything else gets added on top of this.

```
LOW    = 1 × 10 = 10 points
MEDIUM = 2 × 10 = 20 points
HIGH   = 4 × 10 = 40 points
URGENT = 6 × 10 = 60 points
```

**2. Due Date — adds urgency points**

```
overdue        → +35
due today      → +20
due in 2 days  → +15
due this week  → +10
no due date    → +0 (nothing added, doesn't crash)
```

**3. Task Status — removes points if finished**

```
DONE   → -50
REVIEW → -15
```

**4. Special Tags — adds points for important tags**

```
"blocker", "critical", "urgent" → +8
regular tags like "shopping"    → +0
empty tags []                   → +0 (doesn't crash)
```

**5. Recently Updated — small boost**

```
updated today → +5
older         → +0
```

---

### My 5 Test Cases

i worked these out manually before writing any code. the idea was to test ONE thing at a time so if something breaks you know exactly where.

---

**Test 1 — Base priority score (URGENT)**

> URGENT task, no due date, no tags, status TODO
> 

```
URGENT base = 60
no due date = +0
status TODO = +0
no tags     = +0

expected score = 60
```

why test this first — because if the base priority scoring is broken everything else is meaningless. start simple.

---

**Test 2 — DONE status penalty**

> MEDIUM task, no due date, status DONE
> 

```
MEDIUM base = 20
no due date = +0
DONE        = -50

expected score = 20 - 50 = -30
```

this confirms that finished tasks sink to the bottom of the list. negative score = task gets ignored.

---

**Test 3 — DONE + overdue combined**

> MEDIUM task, overdue, status DONE
> 

```
MEDIUM base = 20
overdue     = +35
DONE        = -50

expected score = 20 + 35 - 50 = 5
```

this is an edge case — what happens when a task is both overdue AND finished? it should still sink low because it's done. score of 5 confirms that.

---

**Test 4 — Empty tags (edge case)**

> MEDIUM task, no tags at all
> 

```
MEDIUM base  = 20
no tags []   = +0

expected score = 20
```

i wanted to confirm that passing an empty tags list doesn't crash the function. it doesn't — the any() just returns False and moves on.

---

**Test 5 — Special tag boost**

> MEDIUM task, tag = "blocker"
> 

```
MEDIUM base    = 20
blocker tag    = +8

expected score = 28
```

confirms that special tags actually do something vs regular tags which do nothing.

---

### What I Learned Doing This

the biggest thing i learned was to test ONE factor at a time. my first instinct was to test everything together like URGENT + overdue + blocker tag = 108. but if that test fails you have no idea which part broke.

also i learned that reading code before writing tests is actually useful. i found all 5 factors just by scanning for `score +=` and `score -=` lines. that pattern shows you exactly what changes the output.

---

### What I Still Don't Understand

- what happens if two tasks have the exact same score — which one comes first in the sorted list?
- how often does the score get recalculated — every time you open the app or only when something changes?
- who decides what the actual numbers should be like why is overdue +35 and not +40 — is that just a business decision someone made?

# Exercise 1.2 — Test Planning

## Testing `calculate_task_score`, `sort_tasks_by_importance`, `get_top_priority_tasks`

---

### What Each Function Does In Plain English

before writing any tests i needed to understand what each function actually does.

**`calculate_task_score`**
looks at one task and gives it a score based on 5 factors — priority, due date, status, tags, and how recently it was updated. higher score = more important task.

**`sort_tasks_by_importance`**
takes a list of tasks, scores all of them using calculate_task_score, then sorts them highest score first. reverse=True is what makes it go highest to lowest.

**`get_top_priority_tasks`**
does the same as sort_tasks_by_importance but then cuts the list to only return the top N tasks. default is 5 if you don't specify a number. `[:5]` grabs positions 0,1,2,3,4.

---

### The Dependency Chain — Why Test Order Matters

the three functions depend on each other like a chain:

```
get_top_priority_tasks
        ↓ calls
sort_tasks_by_importance
        ↓ calls
calculate_task_score
```

if calculate_task_score has a bug the scores are wrong. if the scores are wrong sort_tasks_by_importance sorts in the wrong order. if the order is wrong get_top_priority_tasks returns the wrong tasks at the top.

one bug at the bottom breaks everything above it.

so the testing order has to be:

```
1. calculate_task_score      ← test this first, its the foundation
2. sort_tasks_by_importance  ← test this second
3. get_top_priority_tasks    ← test this last
```

---

### Test Types

i learned there are two types of tests here:

**unit test** — tests ONE function in isolation
example: pass one task to calculate_task_score and check the number it returns. nothing else involved.

**integration test** — tests multiple functions working together
example: pass a list of tasks to get_top_priority_tasks and check that the right tasks come back in the right order. this one secretly runs all 3 functions together.

---

### Full Test Checklist

organized by priority — most important tests first.

---

### PRIORITY 1 — Unit Tests for `calculate_task_score`

*test this first before anything else*

| # | Test | Expected |
| --- | --- | --- |
| 1 | LOW priority, no due date, no tags, TODO | 10 |
| 2 | MEDIUM priority, no due date, no tags, TODO | 20 |
| 3 | HIGH priority, no due date, no tags, TODO | 40 |
| 4 | URGENT priority, no due date, no tags, TODO | 60 |
| 5 | MEDIUM, no due date, status DONE | -30 |
| 6 | MEDIUM, overdue, status DONE | 5 |
| 7 | MEDIUM, no tags at all (empty list) | 20 |
| 8 | MEDIUM, tag = "blocker" | 28 |

---

### PRIORITY 2 — Unit Tests for `sort_tasks_by_importance`

*test this after calculate_task_score passes*

| # | Test | Expected |
| --- | --- | --- |
| 9 | 3 tasks: LOW, URGENT, MEDIUM → check order | URGENT first, MEDIUM second, LOW last |
| 10 | empty list [] passed in | returns [] no crash |
| 11 | only one task passed in | returns that one task in a list |

---

### PRIORITY 3 — Integration Tests for `get_top_priority_tasks`

*test this last — it depends on both functions above*

| # | Test | Expected |
| --- | --- | --- |
| 12 | 10 tasks, limit=3 | returns exactly 3 tasks |
| 13 | 3 tasks, limit=10 (asking for more than exists) | returns just 3, no crash |
| 14 | no limit specified → get_top_priority_tasks(tasks) | returns 5 by default |
| 15 | confirm returned tasks are in correct order | highest score task is at position 0 |

---

### Edge Cases I Found

these are the weird situations that could break things:

**empty list** — passing [] to sort or get_top doesn't crash. python just returns [] back. confirmed safe.

**limit bigger than list** — asking for 10 tasks when only 3 exist. python's [:10] just returns what's available. no crash. confirmed safe.

**DONE + overdue combined** — task is finished but also late. DONE penalty (-50) still wins. score stays low. confirmed working.

**empty tags** — passing a task with no tags doesn't crash the tag section. any() just returns False on an empty list. confirmed safe.

---

### Test Dependencies

```
Tests 1-8 have no dependencies
        ↓
Tests 9-11 depend on tests 1-8 passing first
        ↓
Tests 12-15 depend on tests 1-11 passing first
```

don't run integration tests if unit tests are failing. fix the foundation first.

---

### What I Still Don't Understand

- i understand unit vs integration tests but i don't know yet how to actually write them in Python syntax — like what does a real unittest function look like for sort_tasks_by_importance
- i know the dependency chain but i don't know if pytest or unittest has a way to automatically skip integration tests if unit tests fail
- what happens when two tasks have the exact same score — which one comes first and is that something we should test

# Exercise 2.1 — Writing Your First Test

## Testing `calculate_task_score` with unittest

---

### What This Exercise Was About

the goal was to write a basic test for calculate_task_score and then improve it step by step. i didn't just get the answer — i had to figure out what was wrong with each version and fix it myself.

---

### My First Attempt

this was my very first test. the logic was right but it had a bug i didn't see yet:

```python
import unittest
from models import Task, TaskPriority
from task_priority import calculate_task_score

class TestCalculateTaskScore(unittest.TestCase):
    def test_urgent_priority(self):
        task = Task(priority=TaskPriority.URGENT)
        score = calculate_task_score(task)
        self.assertEqual(score, 60)

if __name__ == '__main__':
    unittest.main()
```

---

### What Was Wrong With It

**Bug 1 — missing title**

Task requires a title as the first argument. i forgot it.

```python
task = Task(priority=TaskPriority.URGENT)      # crashes
task = Task("Test Task", priority=TaskPriority.URGENT)  # fixed
```

**Bug 2 — hidden recency boost**

when you create a Task, updated_at gets set to right now automatically. that means the recency boost (+5) kicks in without me realising it.

so my expected score of 60 was actually wrong — the real score would be 65.

```
URGENT base   = 60
updated today = +5
actual score  = 65  ← not 60
```

the fix was to manually set updated_at to 2 days ago so the boost doesn't trigger:

```python
task.updated_at = datetime.now() - timedelta(days=2)
```

this has to go AFTER creating the task but BEFORE calling calculate_task_score. you can't season food after you've already eaten it.

---

### What I Learned About Test Structure

a test has 3 parts every time:

```
1. create the task         ← set up your data
2. call the function       ← run the code
3. check the result        ← confirm the output
```

```python
def test_urgent_priority(self):
    task = Task("Test Task", priority=TaskPriority.URGENT)  # 1
    score = calculate_task_score(task)                       # 2
    self.assertEqual(score, 60)                             # 3
```

---

### Why Separate Test Functions Matter

i tested all 4 priorities but put them in separate functions instead of one big function.

reason — if LOW fails inside one big function, you never find out if HIGH works. separate functions = separate results. you know exactly which priority broke.

```python
def test_urgent_priority(self):  # tests only URGENT
def test_high_priority(self):    # tests only HIGH
def test_medium_priority(self):  # tests only MEDIUM
def test_low_priority(self):     # tests only LOW
```

---

### What setUp Does

i kept repeating the same two lines in every test:

```python
task = Task("Test Task")
task.updated_at = datetime.now() - timedelta(days=2)
```

setUp is a special method that runs automatically before every single test. so instead of repeating those lines 4 times i write them once in setUp and every test gets a fresh task automatically.

```python
def setUp(self):
    self.task = Task("Test Task")
    self.task.updated_at = datetime.now() - timedelta(days=2)
```

then inside each test i just change the priority on the existing task:

```python
def test_urgent_priority(self):
    self.task.priority = TaskPriority.URGENT  # just change priority
    score = calculate_task_score(self.task)
    self.assertEqual(score, 60)
```

---

### Final Working Version

```python
import unittest
from datetime import datetime, timedelta
from models import Task, TaskPriority
from task_priority import calculate_task_score

class TestCalculateTaskScore(unittest.TestCase):
        
    def test_no_due_date_priority(self):
        self.task.priority = TaskPriority.no_due_date
        score = calculate_task_score(self.task)
        self.assertEqual(score, 20)
        
    def test_urgent_priority(self):
        self.task.priority = TaskPriority.URGENT
        score = calculate_task_score(self.task)
        self.assertEqual(score, 60)

    def test_high_priority(self):
        self.task.priority = TaskPriority.HIGH
        score = calculate_task_score(self.task)
        self.assertEqual(score, 40)

    def test_medium_priority(self):
        self.task.priority = TaskPriority.MEDIUM
        score = calculate_task_score(self.task)
        self.assertEqual(score, 20)

    def test_low_priority(self):
        self.task.priority = TaskPriority.LOW
        score = calculate_task_score(self.task)
        self.assertEqual(score, 10)

if __name__ == "__main__":
    unittest.main()
```

---

### Expected Scores Summary

| Priority | Expected Score |
| --- | --- |
| LOW | 10 |
| MEDIUM | 20 |
| HIGH | 40 |
| URGENT | 60 |

these are base scores only — no due date, no special tags, no recency boost, status TODO.

---

### Mistakes I Made Along The Way

- forgot the title argument in Task() — Python crashed before the test even ran
- didn't realise updated_at gets set automatically on task creation — caused a hidden +5 points
- kept using self.create_task() which doesn't exist — should be self.task.priority =
- gave all 4 test functions the same name — Python only ran the last one
- had a missing space in the import line `from task_priority importcalculate_task_score`

---

### What I Still Don't Understand

- i understand setUp runs before every test but i don't know if there's a tearDown that runs after — is that a thing?
- i know assertEqual checks if two values match but what other assertion methods exist — like how do you check if something is None or if a list is empty
- i understand the test passes or fails but i don't know yet what the output looks like when you actually run it in the terminal

# Exercise 2.2 — Learning From Examples

## Testing Due Date Calculations in `calculate_task_score`

---

### What This Exercise Was About

this exercise was about testing the due date part of calculate_task_score. it sounds simple but due dates are actually trickier to test than priority because they depend on what TODAY is — and today keeps changing.

---

### The Problem With Fixed Dates

my first instinct was to write something like:

```python
task.due_date = datetime(2026, 6, 1)
```

but this breaks over time. today that date might be "due this week" and score +10. but in july 2026 that same date is overdue and scores +35. the test fails even though the code didn't change.

the fix is to always set due dates relative to today using datetime.now():

```python
task.due_date = datetime.now() + timedelta(days=2)  # always 2 days from now
task.due_date = datetime.now() - timedelta(days=1)  # always 1 day ago
```

this way the test works correctly no matter when you run it.

---

### The timedelta Pattern

```python
datetime.now() - timedelta(days=1)  # goes BACK in time (past)
datetime.now() + timedelta(days=2)  # goes FORWARD in time (future)
```

minus = past
plus = future

---

### What The Due Date Section Actually Does

```python
if task.due_date:                    # if no due date → skip everything
    days_until_due = (task.due_date - datetime.now()).days
    if days_until_due < 0:           # overdue    → +35
        score += 35
    elif days_until_due == 0:        # due today  → +20
        score += 20
    elif days_until_due <= 2:        # 2 days     → +15
        score += 15
    elif days_until_due <= 7:        # this week  → +10
        score += 10
```

if due_date is None — python sees `if None:` which is always False so the whole block gets skipped. no crash. just returns base score only.

---

### My 5 Test Cases With Expected Scores

all tests use MEDIUM priority (base score 20) with no tags and updated_at set 2 days ago so nothing else interferes.

| Test | Due Date | Calculation | Expected Score |
| --- | --- | --- | --- |
| no due date | None | 20 + 0 | 20 |
| overdue | 1 day ago | 20 + 35 | 55 |
| due today | today | 20 + 20 | 40 |
| due in 2 days | +2 days | 20 + 15 | 35 |
| due next week | +7 days | 20 + 10 | 30 |

---

### Final Working Test File

```python
import unittest
from datetime import datetime, timedelta
from models import Task, TaskPriority
from task_priority import calculate_task_score

class TestDueDateScore(unittest.TestCase):

    def setUp(self):
        self.task = Task("Test Task")
        self.task.priority = TaskPriority.MEDIUM
        self.task.updated_at = datetime.now() - timedelta(days=2)

    def test_no_due_date(self):
        self.task.due_date = None
        score = calculate_task_score(self.task)
        self.assertEqual(score, 20)

    def test_overdue(self):
        self.task.due_date = datetime.now() - timedelta(days=1)
        score = calculate_task_score(self.task)
        self.assertEqual(score, 55)

    def test_due_today(self):
        self.task.due_date = datetime.now()
        score = calculate_task_score(self.task)
        self.assertEqual(score, 40)

    def test_due_in_two_days(self):
        self.task.due_date = datetime.now() + timedelta(days=2)
        score = calculate_task_score(self.task)
        self.assertEqual(score, 35)

    def test_due_next_week(self):
        self.task.due_date = datetime.now() + timedelta(days=7)
        score = calculate_task_score(self.task)
        self.assertEqual(score, 30)

if __name__ == "__main__":
    unittest.main()
```

---

### Why setUp Matters Here

setUp runs before every single test automatically. it creates a fresh task each time with:

- MEDIUM priority
- no due date (None by default)
- updated_at set 2 days ago so recency boost doesn't interfere

then each test only changes ONE thing — the due date. everything else stays controlled. that way if a test fails you know exactly what caused it.

---

### Key Things I Learned

**tests that use fixed dates break over time**
always use datetime.now() + timedelta() so due dates stay relative to today forever.

**None due date doesn't crash**`if task.due_date:` with None just evaluates to False and skips the whole section safely.

**isolate what you're testing**
all 5 tests use MEDIUM priority and the same updated_at so the only thing changing is the due date. one variable at a time.

**minus goes back, plus goes forward**

```python
datetime.now() - timedelta(days=1)  # yesterday
datetime.now() + timedelta(days=7)  # next week
```

---

### Mistakes I Made Along The Way

- wrote the timedelta in comments but forgot to actually set self.task.due_date in the code
- forgot `score =` before calculate_task_score so the result got thrown away
- mixed up the expected scores — got confused between due today (+20) and due in 2 days (+15)
- tried to use TaskPriority.no_due_date which doesn't exist — None is just the default value already

---

### What I Still Don't Understand

- i understand timedelta(days=) but can you use timedelta for hours too — like what if a task is due in 3 hours
- i know `if task.due_date:` handles None safely but what if someone passes in a string like "tomorrow" instead of a datetime object — would that crash
- i understand the 5 due date scenarios but what happens if a task is due exactly at midnight today — does it count as today or tomorrow

# Exercise 3.1 — TDD for a New Feature

## Adding assigned_to boost of +12 to `calculate_task_score`

---

### What TDD Actually Means

TDD = Test Driven Development

the normal way most beginners code:

```
write code first → then write tests
```

the TDD way:

```
write a FAILING test first → then write code to make it pass
```

it feels backwards at first but it forces you to think about what you want BEFORE you build it.

---

### The New Feature

> tasks assigned to the current user should get a score boost of +12
> 

---

### Step 1 — What Needs To Exist First

before writing any test i checked models.py to see if Task already had an `assigned_to` field.

it didn't. the **init** only had:

- id, title, description, priority, status
- created_at, updated_at, due_date, completed_at, tags

so two things needed to be added:

1. `assigned_to` field to Task in models.py
2. boost logic in calculate_task_score in task_priority.py

in TDD you write the test FIRST even though the code doesn't exist yet. the test fails immediately. that's the point — it tells you exactly what to build.

---

### Step 2 — Write The Failing Test First

```python
def test_assigned_to_current_user_boost(self):
    self.task = Task("Test Task")
    self.task.priority = TaskPriority.MEDIUM
    self.task.assigned_to = "current_user"
    self.task.updated_at = datetime.now() - timedelta(days=2)
    score = calculate_task_score(self.task)
    self.assertEqual(score, 32)
```

expected score:

```
MEDIUM base          = 20
assigned to me boost = +12
total                = 32
```

this test fails immediately because:

- Task has no assigned_to field yet
- calculate_task_score doesn't know about the boost yet

that's correct. a failing test is step 1 of TDD. ✅

---

### Step 3 — Write Minimal Code To Make It Pass

**models.py — add assigned_to field:**

```python
def __init__(self, title, description="", priority=TaskPriority.MEDIUM,
             due_date=None, tags=None):
    ...
    self.assigned_to = None  # ← add this line
```

**task_priority.py — add boost logic:**

```python
# Calculate base score from priority
score = priority_weights.get(task.priority, 0) * 10

# Assigned to current user boost
if task.assigned_to == "current_user":
    score += 12

# Critical tags boost
if any(tag in ["blocker", "critical", "urgent"] for tag in task.tags):
    score += 8
```

only the minimal code needed. nothing extra. that's TDD. ✅

---

### Step 4 — Write Next Tests (Edge Cases)

after making the first test pass i wrote two more tests for the opposite situations:

**test — different user gets no boost:**

```python
def test_assigned_to_different_user_no_boost(self):
    self.task.priority = TaskPriority.MEDIUM
    self.task.assigned_to = "other_user"
    self.task.updated_at = datetime.now() - timedelta(days=2)
    score = calculate_task_score(self.task)
    self.assertEqual(score, 20)
```

**test — unassigned task gets no boost:**

```python
def test_unassigned_task_no_boost(self):
    self.task.priority = TaskPriority.MEDIUM
    self.task.assigned_to = None
    self.task.updated_at = datetime.now() - timedelta(days=2)
    score = calculate_task_score(self.task)
    self.assertEqual(score, 20)
```

both expected score = 20 because only "current_user" gets the boost. everyone else gets nothing.

---

### The TDD Cycle I Followed

```
write failing test → assigned_to boost test fails ✅
write minimal code → added field + boost logic
test passes ✅
write next test → different user no boost
write next test → None no boost
no refactoring needed — code is already clean
done ✅
```

---

### What I Learned

- write tests BEFORE writing code — the test tells you what to build
- a failing test is not a mistake — it's step 1
- write MINIMAL code to make the test pass — nothing extra
- always test the opposite case — not just "it works" but also "it correctly does NOT work"

---

---

# Exercise 3.2 — TDD for Bug Fix

## Testing the "days since update" calculation

---

### The Suspected Bug

the exercise suggested the "days since update" calculation might be wrong:

```python
days_since_update = (datetime.now() - task.updated_at).days
if days_since_update < 1:
    score += 5
```

---

### The Most Important Rule In Bug Fixing

> before fixing anything — write a test that PROVES the bug exists
if you can't write a failing test — the bug doesn't exist
> 

a lot of developers waste hours fixing things that aren't actually broken. TDD protects you from that.

---

### The Test I Wrote

```python
def test_task_updated_25_hours_ago_gets_no_recency_boost(self):
    self.task.priority = TaskPriority.MEDIUM
    self.task.updated_at = datetime.now() - timedelta(hours=25)
    score = calculate_task_score(self.task)
    self.assertEqual(score, 20)
```

logic:

```
MEDIUM base   = 20
25 hours ago  → .days returns 1
1 < 1 = False → no boost
expected      = 20
```

---

### What I Discovered

the test PASSED. no bug in Python.

here's why `.days` works correctly in Python:

```python
timedelta(hours=23).days  # returns 0 → boost applies ✅
timedelta(hours=25).days  # returns 1 → no boost ✅
timedelta(hours=48).days  # returns 2 → no boost ✅
```

`.days` only counts complete days. so 23 hours = 0 complete days = boost applies. 25 hours = 1 complete day = no boost. that's actually correct behaviour.

---

### Conclusion

```
suspected bug    → .days calculation wrong
wrote test       → test passed immediately
conclusion       → no bug exists in Python
fix needed       → none
```

this bug would exist in JavaScript or Java but not Python. the test proved it.

---

### What I Learned

- always write a failing test before fixing anything
- if the test passes — the bug doesn't exist — don't touch the code
- the same bug can exist in one language but not another
- TDD saves you from fixing things that aren't broken

---

---

# Exercise 4.1 — Integration Testing

## Testing `calculate_task_score`, `sort_tasks_by_importance`, and `get_top_priority_tasks` together

---

### What Integration Testing Means

unit test = tests ONE function in isolation
integration test = tests MULTIPLE functions working together

all my previous tests called calculate_task_score directly with one task.

an integration test calls get_top_priority_tasks with a LIST of tasks and checks the whole chain works correctly together:

```
get_top_priority_tasks
        ↓ calls
sort_tasks_by_importance
        ↓ calls
calculate_task_score
```

---

### Test 1 — Tasks Sorted In Correct Order

```python
import unittest
from models import Task, TaskPriority
from task_priority import get_top_priority_tasks

class TestIntegration(unittest.TestCase):

    def test_tasks_sorted_by_importance(self):
        # create 3 tasks
        task1 = Task("Low Task")
        task1.priority = TaskPriority.LOW
        task2 = Task("Urgent Task")
        task2.priority = TaskPriority.URGENT
        task3 = Task("Medium Task")
        task3.priority = TaskPriority.MEDIUM

        # put them in a list
        tasks = [task1, task2, task3]

        # call get_top_priority_tasks
        result = get_top_priority_tasks(tasks)

        # check the order — highest score first
        self.assertEqual(result[0].title, "Urgent Task")
        self.assertEqual(result[1].title, "Medium Task")
        self.assertEqual(result[2].title, "Low Task")
```

expected scores:

```
URGENT = 60 → position 0
MEDIUM = 20 → position 1
LOW    = 10 → position 2
```

note — all tasks get +5 recency boost since updated_at defaults to now. but adding +5 to ALL of them doesn't change the order. URGENT still wins.

---

### Test 2 — Limit Returns Correct Number of Tasks

```python
    def test_limit_returns_only_three_tasks(self):
        # create 6 tasks
        task1 = Task("Task 1")
        task1.priority = TaskPriority.LOW
        task2 = Task("Task 2")
        task2.priority = TaskPriority.MEDIUM
        task3 = Task("Task 3")
        task3.priority = TaskPriority.HIGH
        task4 = Task("Task 4")
        task4.priority = TaskPriority.URGENT
        task5 = Task("Task 5")
        task5.priority = TaskPriority.LOW
        task6 = Task("Task 6")
        task6.priority = TaskPriority.HIGH

        # put them in a list
        tasks = [task1, task2, task3, task4, task5, task6]

        # call with limit=3
        result = get_top_priority_tasks(tasks, limit=3)

        # check only 3 come back
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].title, "Task 4")  # URGENT = highest
```

---

### What Integration Tests Confirm

- calculate_task_score scores each task correctly
- sort_tasks_by_importance orders them highest first
- get_top_priority_tasks cuts the list to the right size
- the whole chain works end to end

if any one function has a bug — the integration test catches it even if the unit tests missed it.

---

### Difference Between Unit and Integration Tests

|  | Unit Test | Integration Test |
| --- | --- | --- |
| tests | one function | multiple functions together |
| input | one task | a list of tasks |
| checks | a score number | order and count of results |
| finds | bugs in one function | bugs in how functions connect |

---

### What I Learned

- integration tests need a list of tasks not just one
- the order of tasks in the input doesn't matter — sorting fixes it
- adding the same boost to all tasks doesn't change their relative order
- always check both the content (which task) and the count (how many)

---

### What I Still Don't Understand

- i understand integration tests check multiple functions together but i don't know when you would use a mock in an integration test vs a real object
- i know the recency boost applies to all tasks equally but i wonder if there's a way to disable it in tests without manually setting updated_at every time
- i understand the limit cuts the list but i don't know what happens internally when two tasks have the exact same score — which one gets picked for the top 3

# AI-Assisted Testing Exercise — Final Submission

### WeThinkCode_ — Generative AI for Software Development

### Task Priority Algorithm Testing

---

## Part 1 — Test Plan

### The Functions I Tested

**`calculate_task_score`**
looks at one task and gives it a score based on 5 factors. higher score = more important task. this is the foundation everything else depends on.

**`sort_tasks_by_importance`**
takes a list of tasks, scores all of them, then returns them sorted highest score first.

**`get_top_priority_tasks`**
does the same as sort but cuts the list to only return the top N tasks. default limit is 5.

---

### The Dependency Chain

these three functions depend on each other:

```
get_top_priority_tasks
        ↓ calls
sort_tasks_by_importance
        ↓ calls
calculate_task_score
```

a bug at the bottom breaks everything above it. so testing order matters:

```
1. calculate_task_score      ← test first
2. sort_tasks_by_importance  ← test second
3. get_top_priority_tasks    ← test last
```

---

### Factors That Affect The Score

i read through the whole function and mapped every factor:

| Factor | Effect |
| --- | --- |
| LOW priority | +10 |
| MEDIUM priority | +20 |
| HIGH priority | +40 |
| URGENT priority | +60 |
| Overdue | +35 |
| Due today | +20 |
| Due in 2 days | +15 |
| Due this week | +10 |
| Status DONE | -50 |
| Status REVIEW | -15 |
| Special tags (blocker/critical/urgent) | +8 |
| Updated today | +5 |
| Assigned to current user | +12 |

---

### Full Test Checklist

### Priority 1 — Unit Tests for `calculate_task_score`

| # | Test | Expected Score |
| --- | --- | --- |
| 1 | LOW, no due date, no tags, TODO | 10 |
| 2 | MEDIUM, no due date, no tags, TODO | 20 |
| 3 | HIGH, no due date, no tags, TODO | 40 |
| 4 | URGENT, no due date, no tags, TODO | 60 |
| 5 | MEDIUM, no due date, status DONE | -30 |
| 6 | MEDIUM, overdue, status DONE | 5 |
| 7 | MEDIUM, no tags (empty list) | 20 |
| 8 | MEDIUM, tag = "blocker" | 28 |

### Priority 2 — Due Date Tests

| # | Test | Expected Score |
| --- | --- | --- |
| 9 | MEDIUM, no due date | 20 |
| 10 | MEDIUM, overdue | 55 |
| 11 | MEDIUM, due today | 40 |
| 12 | MEDIUM, due in 2 days | 35 |
| 13 | MEDIUM, due next week | 30 |

### Priority 3 — TDD Feature Tests

| # | Test | Expected Score |
| --- | --- | --- |
| 14 | MEDIUM, assigned to current user | 32 |
| 15 | MEDIUM, assigned to different user | 20 |
| 16 | MEDIUM, assigned_to = None | 20 |

### Priority 4 — Integration Tests

| # | Test | Expected Result |
| --- | --- | --- |
| 17 | 3 tasks sorted by importance | URGENT first, MEDIUM second, LOW last |
| 18 | 6 tasks with limit=3 | exactly 3 tasks returned |

---

### Test Types

**unit test** — tests ONE function in isolation with one task
**integration test** — tests all three functions working together with a list of tasks

---

---

## Part 2 — Unit Tests

### Priority Score Tests

```python
import unittest
from datetime import datetime, timedelta
from models import Task, TaskPriority
from task_priority import calculate_task_score

class TestCalculateTaskScore(unittest.TestCase):

    def setUp(self):
        self.task = Task("Test Task")
        self.task.updated_at = datetime.now() - timedelta(days=2)

    def test_urgent_priority(self):
        self.task.priority = TaskPriority.URGENT
        score = calculate_task_score(self.task)
        self.assertEqual(score, 60)

    def test_high_priority(self):
        self.task.priority = TaskPriority.HIGH
        score = calculate_task_score(self.task)
        self.assertEqual(score, 40)

    def test_medium_priority(self):
        self.task.priority = TaskPriority.MEDIUM
        score = calculate_task_score(self.task)
        self.assertEqual(score, 20)

    def test_low_priority(self):
        self.task.priority = TaskPriority.LOW
        score = calculate_task_score(self.task)
        self.assertEqual(score, 10)

if __name__ == "__main__":
    unittest.main()
```

---

### Due Date Tests

```python
import unittest
from datetime import datetime, timedelta
from models import Task, TaskPriority
from task_priority import calculate_task_score

class TestDueDateScore(unittest.TestCase):

    def setUp(self):
        self.task = Task("Test Task")
        self.task.priority = TaskPriority.MEDIUM
        self.task.updated_at = datetime.now() - timedelta(days=2)

    def test_no_due_date(self):
        self.task.due_date = None
        score = calculate_task_score(self.task)
        self.assertEqual(score, 20)

    def test_overdue(self):
        self.task.due_date = datetime.now() - timedelta(days=1)
        score = calculate_task_score(self.task)
        self.assertEqual(score, 55)

    def test_due_today(self):
        self.task.due_date = datetime.now()
        score = calculate_task_score(self.task)
        self.assertEqual(score, 40)

    def test_due_in_two_days(self):
        self.task.due_date = datetime.now() + timedelta(days=2)
        score = calculate_task_score(self.task)
        self.assertEqual(score, 35)

    def test_due_next_week(self):
        self.task.due_date = datetime.now() + timedelta(days=7)
        score = calculate_task_score(self.task)
        self.assertEqual(score, 30)

if __name__ == "__main__":
    unittest.main()
```

---

### Key Thing I Learned About Due Date Tests

fixed dates break over time:

```python
task.due_date = datetime(2026, 6, 1)  # breaks in July 2026
```

relative dates always work:

```python
task.due_date = datetime.now() + timedelta(days=2)  # always 2 days from now
```

---

---

## Part 3 — TDD Implementation

### The New Feature

> tasks assigned to the current user should get a score boost of +12
> 

---

### Step 1 — Wrote The Failing Test First

```python
def test_assigned_to_current_user_boost(self):
    self.task = Task("Test Task")
    self.task.priority = TaskPriority.MEDIUM
    self.task.assigned_to = "current_user"
    self.task.updated_at = datetime.now() - timedelta(days=2)
    score = calculate_task_score(self.task)
    self.assertEqual(score, 32)
```

expected: MEDIUM(20) + assigned boost(+12) = 32

this test failed immediately because assigned_to didn't exist yet. that's correct — a failing test is step 1 of TDD.

---

### Step 2 — Minimal Code To Make It Pass

**models.py — added assigned_to field:**

```python
self.assigned_to = None
```

**task_priority.py — added boost logic:**

```python
# Assigned to current user boost
if task.assigned_to == "current_user":
    score += 12
```

---

### Step 3 — Edge Case Tests

```python
def test_assigned_to_different_user_no_boost(self):
    self.task.priority = TaskPriority.MEDIUM
    self.task.assigned_to = "other_user"
    self.task.updated_at = datetime.now() - timedelta(days=2)
    score = calculate_task_score(self.task)
    self.assertEqual(score, 20)

def test_unassigned_task_no_boost(self):
    self.task.priority = TaskPriority.MEDIUM
    self.task.assigned_to = None
    self.task.updated_at = datetime.now() - timedelta(days=2)
    score = calculate_task_score(self.task)
    self.assertEqual(score, 20)
```

---

### TDD Bug Fix — Exercise 3.2

suspected bug — `.days` calculation wrong for recency boost.

most important rule in bug fixing:

> write a test that proves the bug exists before touching anything
> 

```python
def test_task_updated_25_hours_ago_gets_no_recency_boost(self):
    self.task.priority = TaskPriority.MEDIUM
    self.task.updated_at = datetime.now() - timedelta(hours=25)
    score = calculate_task_score(self.task)
    self.assertEqual(score, 20)
```

the test passed immediately. no bug in Python.

```python
timedelta(hours=25).days  # returns 1
1 < 1                     # False → no boost ✅
```

conclusion — no fix needed. the test proved the bug doesn't exist in Python.

---

---

## Part 4 — Integration Test

```python
import unittest
from models import Task, TaskPriority
from task_priority import get_top_priority_tasks

class TestIntegration(unittest.TestCase):

    def test_tasks_sorted_by_importance(self):
        task1 = Task("Low Task")
        task1.priority = TaskPriority.LOW
        task2 = Task("Urgent Task")
        task2.priority = TaskPriority.URGENT
        task3 = Task("Medium Task")
        task3.priority = TaskPriority.MEDIUM

        tasks = [task1, task2, task3]
        result = get_top_priority_tasks(tasks)

        self.assertEqual(result[0].title, "Urgent Task")
        self.assertEqual(result[1].title, "Medium Task")
        self.assertEqual(result[2].title, "Low Task")

    def test_limit_returns_only_three_tasks(self):
        task1 = Task("Task 1")
        task1.priority = TaskPriority.LOW
        task2 = Task("Task 2")
        task2.priority = TaskPriority.MEDIUM
        task3 = Task("Task 3")
        task3.priority = TaskPriority.HIGH
        task4 = Task("Task 4")
        task4.priority = TaskPriority.URGENT
        task5 = Task("Task 5")
        task5.priority = TaskPriority.LOW
        task6 = Task("Task 6")
        task6.priority = TaskPriority.HIGH

        tasks = [task1, task2, task3, task4, task5, task6]
        result = get_top_priority_tasks(tasks, limit=3)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].title, "Task 4")

if __name__ == "__main__":
    unittest.main()
```

---

---

## Part 5 — Reflection

### Where I Started

when i started this exercise i had no idea what testing actually was. i thought it was just running your code and seeing if it worked. i called unittest "flash" at some point. i didn't know what setUp did. i didn't know the difference between a unit test and an integration test.

i also thought all you needed to do was test the happy path — like give it a URGENT task and check you get 60. i didn't think about edge cases at all.

---

### What Changed

**i learned to read code before writing tests**

before writing a single test i scanned the whole function for `score +=` and `score -=` patterns. that gave me the complete map of every factor that affects the output. that approach works on any function — find what changes the output, then test each one.

**i learned that time breaks tests**

the biggest surprise was discovering that `updated_at` gets set automatically when you create a Task. i had a test that was silently wrong — it expected 60 but would have actually returned 65. fixed dates break over time too. now i always use `datetime.now() + timedelta()` instead of fixed dates.

**i learned what TDD actually means**

TDD felt backwards at first — write a test before the code exists? but once i did it, it made sense. the failing test tells you exactly what to build. you only build what the test needs. nothing extra. it keeps code clean.

**i learned the most important rule in bug fixing**

> write a test that proves the bug exists before touching anything
> 

for exercise 3.2 i wrote a test expecting the bug to exist — and it passed. no bug. if i had just gone in and "fixed" things without a test i might have actually broken working code.

**i learned the difference between unit and integration tests**

unit tests = one function, one task, check one number
integration tests = multiple functions, list of tasks, check order and count

both matter. unit tests tell you WHERE something broke. integration tests tell you IF something broke end to end.

---

### Mistakes I Made That I Won't Make Again

- forgetting the title argument in Task() — Python crashes before the test runs
- setting updated_at AFTER calling calculate_task_score — too late, score already calculated
- giving all test functions the same name — Python only runs the last one
- writing `self.create_task()` which doesn't exist — should be `self.task.priority =`
- testing with wrong expected values from the actual function — tests should check what the code DOES not what you think it should do

---

### What I Still Want To Learn

- how to read test output in the terminal when tests actually run
- what other assertion methods exist besides assertEqual
- whether there's a way to skip the recency boost in tests without manually setting updated_at every time
- what happens when two tasks have the exact same score — which one comes first
- how to write tests for functions that interact with files or databases
