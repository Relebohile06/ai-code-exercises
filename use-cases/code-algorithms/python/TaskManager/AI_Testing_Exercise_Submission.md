# AI-Assisted Testing Exercise — Final Submission
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
|---|---|
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

#### Priority 1 — Unit Tests for `calculate_task_score`

| # | Test | Expected Score |
|---|---|---|
| 1 | LOW, no due date, no tags, TODO | 10 |
| 2 | MEDIUM, no due date, no tags, TODO | 20 |
| 3 | HIGH, no due date, no tags, TODO | 40 |
| 4 | URGENT, no due date, no tags, TODO | 60 |
| 5 | MEDIUM, no due date, status DONE | -30 |
| 6 | MEDIUM, overdue, status DONE | 5 |
| 7 | MEDIUM, no tags (empty list) | 20 |
| 8 | MEDIUM, tag = "blocker" | 28 |

#### Priority 2 — Due Date Tests

| # | Test | Expected Score |
|---|---|---|
| 9 | MEDIUM, no due date | 20 |
| 10 | MEDIUM, overdue | 55 |
| 11 | MEDIUM, due today | 40 |
| 12 | MEDIUM, due in 2 days | 35 |
| 13 | MEDIUM, due next week | 30 |

#### Priority 3 — TDD Feature Tests

| # | Test | Expected Score |
|---|---|---|
| 14 | MEDIUM, assigned to current user | 32 |
| 15 | MEDIUM, assigned to different user | 20 |
| 16 | MEDIUM, assigned_to = None | 20 |

#### Priority 4 — Integration Tests

| # | Test | Expected Result |
|---|---|---|
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
