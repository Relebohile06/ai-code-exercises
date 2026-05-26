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
