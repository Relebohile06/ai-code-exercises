AI Response To Your Prompt
1. What This Component Actually Does
The task creation system does one simple job:

Takes information a user types in the terminal, turns it into a proper Task object, and saves it permanently to a file so it's still there next time you open the app.

Status updates do one simple job:

Find an existing task by its ID, change one field (the status), and save it again.


2. Execution Flow — Step By Step
When you type:
python cli.py create "Buy milk" --priority 3 --due "2026-06-01"
Here's exactly what happens:
STEP 1 — cli.py wakes up
reads your command and extracts:
  title    = "Buy milk"
  priority = 3
  due date = "2026-06-01"
        ↓
STEP 2 — cli.py calls task_manager.py
says: "create a task with these values"
        ↓
STEP 3 — task_manager.py builds the Task
goes to models.py and says:
"give me the Task blueprint"
creates a new Task object with:
  title    = "Buy milk"
  priority = HIGH (because 3 = HIGH)
  due_date = 2026-06-01
  status   = TODO (default)
  id       = auto generated UUID
        ↓
STEP 4 — task_manager.py calls storage.py
says: "save this task"
        ↓
STEP 5 — storage.py saves it
takes the Task object
converts it to JSON format
writes it to tasks.json file
        ↓
STEP 6 — cli.py tells the user
prints: "Created task with ID: abc123"

3. How The Files Interact
cli.py
  → imports TaskManager from task_manager.py
  → calls task_manager.create_task()

task_manager.py
  → imports Task, TaskPriority from models.py
  → imports TaskStorage from storage.py
  → builds the Task using models.py blueprint
  → saves it using storage.py

storage.py
  → imports Task from models.py
  → writes to tasks.json

models.py
  → imported by EVERYONE
  → doesn't import from any project file
  → it's the foundation

4. To Answer Your Specific Confusion

"the info coming from storage.py — where does it come from?"

Great question. Here's the answer:
storage.py gets its information from TWO places:
When SAVING:
task_manager.py creates a Task object
        ↓
passes it TO storage.py
        ↓
storage.py converts it to JSON
        ↓
writes it to tasks.json file
When LOADING:
app starts up
        ↓
storage.py automatically reads tasks.json
        ↓
converts JSON back into Task objects
        ↓
stores them in memory
        ↓
ready for task_manager.py to use
So storage.py is like a translator working in BOTH directions:

Task objects → JSON (saving)
JSON → Task objects (loading)


5. Complex Code Block Explained
This is the trickiest part in storage.py:
pythonclass TaskEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Task):
            task_dict = obj.__dict__.copy()
            task_dict['priority'] = obj.priority.value
            task_dict['status'] = obj.status.value
In plain English:

Python can't save a Task object directly to JSON
So TaskEncoder converts it first
It turns TaskPriority.HIGH into just the number 3
It turns TaskStatus.DONE into just the string "done"
Now JSON can understand it


6. Mental Model
Think of the whole system like a restaurant order:
You (user)
→ tell the waiter your order (cli.py)

Waiter (cli.py)
→ writes it on an order slip (task_manager.py)

Kitchen (task_manager.py)
→ uses the recipe (models.py) to prepare it
→ puts the finished dish in the fridge (storage.py)

Fridge (storage.py)
→ keeps everything safe
→ written in a format anyone can read (JSON)
→ still there tomorrow when you come back

7. Your 3 Code Challenges To Test Understanding
Challenge 1:
Add a new field to the Task that records how many times the task status has been updated. You should NOT change models.py yet — just understand where you WOULD need to add it and why.
Challenge 2:
Make the system print a warning message when a task is created without a due date. Find where in the flow that check would need to happen.
Challenge 3:
Make it impossible to set a task's status back to TODO once it has been marked as DONE. Find which file contains the rule that would prevent this and explain why that file is the right place for it.
