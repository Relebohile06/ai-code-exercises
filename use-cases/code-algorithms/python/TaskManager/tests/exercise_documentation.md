Exercise Part 1: Understanding Project Structure

### Misconceptions I Had

okay so at first i literally just saw a bunch of random python files and had no idea how they connected. i thought all the files ran together every single time you run the app — like one big thing. turns out that's wrong. some files like task_list_merge.py only get used when you actually need to merge lists. not every file runs every time.

i also thought models.py was like... selecting which task is important? like clicking on something. but no — it's more like a template or blueprint that says "this is what a task looks like" before anything even happens.

oh and i called the testing framework "flash"  it's actually unittest. completely different thing. flask is a web thing. unittest is for testing python code.

i also didn't know the difference between built-in imports and custom imports. i thought ALL imports were files you had to create yourself. but stuff like argparse and datetime come FREE with python — you don't build them, they're just there.


### Entry Points

so there's two ways into this project:

- **for a normal user:** you type `python cli.py create "your task"` in the terminal. that's where everything starts
- **for a developer:** you run `python -m unittest discover tests` and python goes and finds all the test files automatically and checks if everything is working


### Architectural Pattern

the files follow a layered pattern — meaning each file has ONE job and they don't do each other's work. they talk to each other using imports. like cli.py calls task_manager.py, task_manager.py calls models.py and storage.py and so on.

the way i think about it now is like a restaurant:

- you (the user) talk to the waiter (cli.py)
- the waiter tells the head chef (task_manager.py) what you want
- the head chef uses recipes (models.py) to know what a task looks like
- then the filing cabinet (storage.py) saves everything
- and the specialist helpers (parser, priority, merge) only come in when specifically needed

you can't skip any file that's needed for your specific command — if one is missing the whole thing breaks


### Key Components and Their Responsibilities

- **cli.py** — the front door. reads what you type in the terminal and passes it along. doesn't do the actual work itself
- **task_manager.py** — the brain. coordinates everything. creating, updating, deleting tasks all goes through here
- **models.py** — the blueprint. defines what a task actually IS — what fields it has, what priority levels exist, what statuses are allowed
- **storage.py** — the filing cabinet. saves tasks to tasks.json and loads them back when you open the app again
- **task_parser.py** — the translator. turns plain text like "Buy milk @shopping !high #tomorrow" into an actual task with proper fields
- **task_priority.py** — the ranker. gives each task a score based on priority, due date and status — then sorts them most important first
- **task_list_merge.py** — the syncer. combines two separate task lists without losing data or creating duplicates. only runs when you actually need to merge


### What I Now Understand About Imports

so imports are basically files talking to each other. but there's two types:

**built-in imports** — these come with python when you install it. you don't create them, they're just there waiting. things like argparse and datetime. free tools in the python toolbox.

**custom imports** — these are files YOUR project created. like when task_manager.py says `from models import Task` it's literally going to find models.py in your project folder and grabbing what it needs from there.

the whole project is connected through imports. that's how separate files work as one system. they don't magically know about each other — they have to specifically import what they need. if you delete one file that another file imports from, the whole thing crashes.

### What I Still Don't Understand

- how does `task_list_merge.py` actually know which version of a task is newer? like what happens if both were updated at the exact same time?
- i still don't fully get how `unittest` finds the test files automatically — like what's it actually looking for?
- when `storage.py` saves to `tasks.json` — what happens if the app crashes halfway through saving? does it lose everything?
- i get that imports connect the files but i don't fully understand yet how python actually goes and finds those files — like what if the file is in a different folder?
- i understand argparse reads commands but i don't fully get how it knows the difference between `-priority` and `-due` when you type them

- 
