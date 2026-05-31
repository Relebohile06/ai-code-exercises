# Using AI to Refactor and Enhance Code

# Table of Contents

1. [Understanding What to Change with AI](https://ai.wethinkco.de/ai-software/ai-use-cases/usecases-refactor/#_understanding_code_refactoring_with_ai)
2. [Breaking Down Complex Functions](https://ai.wethinkco.de/ai-software/ai-use-cases/usecases-refactor/#_2_breaking_down_complex_functions)
3. [Improving Code Readability](https://ai.wethinkco.de/ai-software/ai-use-cases/usecases-refactor/#_3_improving_code_readability)
4. [Implementing Design Patterns](https://ai.wethinkco.de/ai-software/ai-use-cases/usecases-refactor/#_4_implementing_design_patterns)

---

---

# 1. Understanding What to Change with AI
## Python Function Refactoring: process_orders()

---

## What This Exercise Was About

The goal was to take a Python function that works but is hard to maintain
and use three different AI prompting strategies to improve it.

The function: `process_orders(orders, inventory, customer_data)`

The problem: One function doing too many jobs at once — over 60 lines,
11 separate responsibilities all living in one place.

---

## Before We Used AI — What I Found First

Before using any prompt, I read the code and identified the jobs myself
by reading the `#` comments the original developer left:

1. Check if item is in inventory
2. Check if enough quantity is available
3. Check if customer exists
4. Calculate price
5. Apply discount if customer is premium
6. Update inventory
7. Calculate shipping based on customer location
8. Add tax
9. Calculate final price
10. Update total revenue
11. Create result

**11 separate jobs inside one function.**

I also grouped them into logical sections:

| Group | Jobs |
|---|---|
| Validating the order | 1, 2, 3 |
| Calculating the total | 4, 5, 8, 9 |
| Update inventory | 6 |
| Calculate shipping | 7 |
| Build the result | 11 |
| Track revenue | 10 |

---

## Prompt 1 — Code Readability Improvement

### What This Prompt Focused On
How the code looks — naming, style, magic numbers, formatting.

### Key Issues the AI Identified

**Magic numbers — hard-coded values with no explanation:**
```python
# Before — confusing
price *= 0.9
tax = price * 0.08
shipping = 5.99
```

```python
# After — clear meaning
PREMIUM_DISCOUNT = 0.10
TAX_RATE = 0.08
DOMESTIC_SHIPPING = 5.99
INTERNATIONAL_SHIPPING = 15.99
```

**Misleading variable names:**

| Before | After | Why |
|---|---|---|
| `price` | `subtotal` | It's not the final amount yet |
| `final_price` | `order_total` | Clearer what it represents |
| `results` | `processed_orders` | More descriptive |
| `result` | `processed_order` | Consistent naming |
| `error_orders` | `failed_orders` | More intuitive |

**Repeated dictionary lookups making code noisy:**
```python
# Before — repeated every time
inventory[item_id]['quantity']
inventory[item_id]['price']
customer_data[customer_id]['premium']
customer_data[customer_id]['location']
```

```python
# After — store once, use cleanly
item = inventory[item_id]
customer = customer_data[customer_id]

item['quantity']
item['price']
customer['premium']
customer['location']
```

### What I Learned
`subtotal` is better than `price` because it tells the reader the amount
is not final — like a till slip showing subtotal before VAT and shipping
are added. The name should match what the variable actually contains
at that point in the code.

---

## Prompt 2 — Function Refactoring

### What This Prompt Focused On
How the code is organised — breaking one large function into smaller,
focused functions with single responsibilities.

### Responsibilities Identified

| Responsibility | Suggested Function |
|---|---|
| Validate order data | `validate_order()` |
| Calculate pricing and tax | `calculate_order_total()` |
| Calculate shipping costs | `calculate_shipping()` |
| Update stock levels | `update_inventory()` |
| Build response object | `create_order_result()` |
| Track total revenue | Stays in main function |

### Improved Flow After Refactoring

```
process_orders()
       ↓
validate_order()
       ↓
calculate_order_total()
       ↓
calculate_shipping()
       ↓
update_inventory()
       ↓
create_order_result()
       ↓
update total_revenue
```

### What the Main Function Looks Like After

```python
for order in orders:

    error = validate_order(order, inventory, customer_data)
    if error:
        failed_orders.append(error)
        continue

    item = inventory[order['item_id']]
    customer = customer_data[order['customer_id']]

    subtotal, tax = calculate_order_total(item, order['quantity'], customer)
    shipping = calculate_shipping(customer, subtotal)
    order_total = subtotal + shipping + tax

    update_inventory(item, order['quantity'])
    total_revenue += order_total

    processed_orders.append(
        create_order_result(order, subtotal, shipping, tax, order_total)
    )
```

### What I Learned
The key question for any function is: "Does this function do ONE thing
or many things?" That single question catches most refactoring problems.

---

## Prompt 3 — Code Duplication Detection

### What This Prompt Focused On
What the code repeats — identical patterns that could be consolidated.

### Repeated Patterns Found

**Pattern 1 — Error creation repeated 3 times:**
```python
error_orders.append({'order_id': order['order_id'], 'error': 'Item not in inventory'})
error_orders.append({'order_id': order['order_id'], 'error': 'Insufficient quantity'})
error_orders.append({'order_id': order['order_id'], 'error': 'Customer not found'})
```

Consolidated into:
```python
def create_error(order_id, message):
    return {'order_id': order_id, 'error': message}

error_orders.append(create_error(order['order_id'], "Customer not found"))
```

**Pattern 2 — Repeated dictionary lookups**
**Pattern 3 — Validation checks all follow the same structure**

### What I Learned
When you see the same structure repeated with only small differences,
that is a signal to extract a helper function. The repeated part
becomes the function body. The small differences become the parameters.

---

## Key Takeaways

**What each prompt caught:**

| Prompt | Focus | What it found |
|---|---|---|
| Prompt 1 | How the code looks | Bad names, magic numbers, noisy lookups |
| Prompt 2 | How the code is organised | Too many responsibilities in one function |
| Prompt 3 | What the code repeats | Duplicated error creation and validation patterns |

**What I will look for first in any unfamiliar function:**
The function's responsibility — does it do ONE thing or many things?

## Before and After Summary

| Problem | Before | After |
|---|---|---|
| Function length | 60+ lines, 11 jobs | Main loop ~20 lines |
| Variable names | `price`, `result`, `error_orders` | `subtotal`, `processed_order`, `failed_orders` |
| Magic numbers | `0.9`, `5.99`, `0.08` | Named constants |
| Error creation | Repeated 3 times | One `create_error()` function |
| Responsibilities | All in one function | Split across 5 helper functions |
| Readability | Requires careful reading | Reads like plain English |

---

---

# 2. Breaking Down Complex Functions
## generate_sales_report() — Python Refactoring Documentation

---

## What This Exercise Was About

The goal was to take a real-world Python function that works but is
dangerously hard to maintain, and use three AI prompting strategies
to systematically decompose it into a clean, modular system.

The function: `generate_sales_report()`

The problem: 150+ lines, 22 separate responsibilities, deeply nested
conditionals, and logic that mutates data mid-function.

---

## Before Using AI — What I Found First

By reading the `#` comments the developer left, I identified 22 jobs
inside one function. **22 jobs. One function.** Twice as bad as
`process_orders()`.

### My Groupings (before any AI prompt)

| Group | Jobs | Suggested Function |
|---|---|---|
| Validation | 1, 5 | `validate_inputs()` |
| Date & Filter handling | 2, 3, 4 | `filter_sales_data()` |
| Calculations & Metrics | 7, 9, 17 | `calculate_metrics()` |
| Grouping data | 8, 11, 15, 21 | `group_sales_data()` |
| Forecast & Trends | 14, 16, 18 | `generate_forecast()` |
| Charts | 19, 20 | `generate_charts()` |
| Detailed report building | 12, 13 | `build_detailed_report()` |
| Output generation | 6, 10, 22 | `generate_output()` |

My groupings matched the AI's response exactly on Prompt 1.

---

## Prompt 1 — System Mapping (Architecture View)

### What This Prompt Specialises In
Prompt 1 is the zoomed-out brain.
It answers: "What exists in this mess?"

### Key Insight
> "A main function should be a traffic controller, not a city.
> It directs traffic — it doesn't build the roads, buildings,
> and cars all at once."

---

## Prompt 2 — Targeted Extraction (Deep Dive View)

### What This Prompt Specialises In
Prompt 2 is the surgical tool.
It answers: "How should this one piece actually work?"

### What Was Extracted — Forecast Logic

~60 lines of complex forecast logic reduced to:
```python
if report_type == 'forecast':
    report_data['forecast'] = generate_forecast_data(sales_data)
```

One line replaced sixty lines of embedded logic.

---

## Prompt 3 — Complexity Reduction (Refactoring Strategy View)

### What This Prompt Specialises In
Prompt 3 is the decision logic dismantler.
It answers: "How do I stop this from getting worse every time I add a feature?"

### The Shotgun Surgery Problem
Adding `'csv'` as a new format required changes in 3 separate places:
1. The validation list
2. The elif block
3. A new helper function

### The Solution — Pipeline Pattern

```
raw data → validate → filter → transform → aggregate → output
```

Old way: "One function decides everything all the time"
Pipeline way: "Many small functions each do one thing in order"

Less decision maze. More assembly line.

---

## How the Three Prompts Work Together

| Layer | Prompt | Question it answers |
|---|---|---|
| 1 — Map | Prompt 1 | What exists in this mess? |
| 2 — Extract | Prompt 2 | How should this one piece work? |
| 3 — Stabilise | Prompt 3 | How do I stop this getting worse? |

**map → extract → stabilise**

## Before and After Summary

| Problem | Before | After |
|---|---|---|
| Function length | 150+ lines | Main function ~15 lines |
| Responsibilities | 22 in one function | 8 focused helper functions |
| Forecast logic | 60 lines embedded | `generate_forecast_data()` |
| Output conditionals | Fragile elif chain | Pipeline with named handlers |
| Adding new format | 3 places to change | 1 place to change |
| Testability | Test everything together | Test each function alone |

---

---

# 3. Improving Code Readability
## Python — Missing Documentation: calculate_compound_interest()

---

## What This Exercise Was About

The goal was to take a working Python function with poor readability
and use AI prompting strategies to improve naming, add documentation,
and verify the refactoring preserved behaviour through unit tests.

The function: `calculate()`
The problem: Cryptic function name, ambiguous parameter names, no
documentation, and no explanation of the financial logic.

---

## Understanding the Code First

R1000 in. R1051.16 after one year. R51.16 added by the bank.
That's interest being earned on top of interest — **compound interest.**

---

## Prompt 1 — Variable and Function Naming Enhancement

**Before:**
```python
def calculate(principal, rate, time, additional=0, frequency=12):
    result = principal
```

**After:**
```python
def calculate_compound_interest(
    principal_amount,
    annual_interest_rate,
    time_years,
    additional_amount=0,
    compounding_frequency_per_year=12
):
    accumulated_amount = principal_amount
```

### Bonus — Extracted Boolean Conditions

**Before:**
```python
if period % frequency == 0 and period < total_periods:
    result += additional
```

**After:**
```python
is_year_end = period_index % compounding_frequency_per_year == 0
is_not_final_period = period_index < total_periods

if is_year_end and is_not_final_period:
    accumulated_amount += additional_amount
```

---

## Prompt 2 — Comment and Documentation Addition

The docstring explained:
- Purpose of the function
- What each parameter means including units
- What each return value represents
- Assumptions made by the calculation
- Limitations (no taxes, fees, or inflation)
- Business rules (contributions added at year boundaries only)

**Prompt 1 answered:** "What are these variables and functions called?"
**Prompt 2 answered:** "Why does this code exist and what rules is it implementing?"

### Important Lesson — AI Doesn't Remember Previous Prompts
When Prompt 2 was applied, the AI documented the old version with old
parameter names. The two improvements had to be manually merged.

> AI gives you pieces. You assemble the final version.

---

## Final Refactored Function

```python
def calculate_compound_interest(
    principal_amount,
    annual_interest_rate,
    time_years,
    additional_amount=0,
    compounding_frequency_per_year=12
):
    """
    Calculate compound interest with periodic compounding and optional yearly contributions.

    Args:
        principal_amount (float): Initial investment amount.
        annual_interest_rate (float): Annual interest rate as a percentage (e.g. 5 for 5%).
        time_years (int or float): Duration of investment in years.
        additional_amount (float, optional): Fixed contribution added at end of each year.
                                             Defaults to 0.
        compounding_frequency_per_year (int, optional): Number of compounding periods per year.
                                                         Defaults to 12.

    Returns:
        dict: Summary containing final_amount, interest_earned, total_contributions.

    Assumptions:
        - Interest rate remains constant over the entire investment period.
        - Additional contributions are added only at the end of each completed year.

    Limitations:
        - Does not account for taxes, inflation, fees, or withdrawals.
    """
    accumulated_amount = principal_amount
    interest_rate_per_period = annual_interest_rate / 100 / compounding_frequency_per_year
    total_periods = time_years * compounding_frequency_per_year

    for period_index in range(1, total_periods + 1):
        periodic_interest = accumulated_amount * interest_rate_per_period
        accumulated_amount += periodic_interest

        is_year_end = period_index % compounding_frequency_per_year == 0
        is_not_final_period = period_index < total_periods

        if is_year_end and is_not_final_period:
            accumulated_amount += additional_amount

    return {
        "final_amount": round(accumulated_amount, 2),
        "interest_earned": round(
            accumulated_amount
            - principal_amount
            - (additional_amount * (time_years - 1)),
            2
        ),
        "total_contributions": principal_amount + (additional_amount * (time_years - 1))
    }
```

---

## Test Results

```
....
----------------------------------------------------------------------
Ran 4 tests in 0.026s

OK
```

All 4 tests passed. Refactoring preserved behaviour completely.

### Real Debugging Moment
`ls` revealed `calculator.py` had 0 bytes — the file existed but was
empty. The function had been pasted into the chat instead of the file.

Lesson: Always verify file contents, not just file existence.

---

## Key Takeaways

**What naming fixes vs what documentation fixes:**

| Prompt 1 — Naming | Prompt 2 — Documentation |
|---|---|
| What things are called | Why things exist |
| Self-documenting code | Context and intent |
| Immediate clarity | Business rules and assumptions |
| Visible at call site | Visible inside the function |

**Biggest impact improvement:**
The function signature is your public face. Every reader sees it first —
before reading a single comment or line of implementation.

## Before and After Summary

| Element | Before | After |
|---|---|---|
| Function name | `calculate()` | `calculate_compound_interest()` |
| Rate param | `rate` | `annual_interest_rate` |
| Time param | `time` | `time_years` |
| Loop variable | `result` | `accumulated_amount` |
| Condition | complex one-liner | `if is_year_end and is_not_final_period` |
| Documentation | None | Full docstring |
| Tests passing | 4/4 | 4/4 |

---

---

# 4. Implementing Design Patterns
## Factory Pattern — Database Connection Manager (Python)

---

## What This Exercise Was About

The goal was to identify a design pattern opportunity in existing code,
implement it with AI guidance, and document the benefits gained.

The code: `DatabaseConnection` — a single class managing all database
types through a giant conditional chain.

The pattern applied: **Factory Pattern**

---

## Understanding the Code First

Two problems identified before using any prompt:

**Problem 1 — Too Many Parameters (11)**
Different databases use different subsets. Redis doesn't need `charset`.
MySQL doesn't need `pool_size`. Every type carries params it doesn't need.

**Problem 2 — Giant Conditional Chain**
```python
if self.db_type == 'mysql':    ...
elif self.db_type == 'postgresql': ...
elif self.db_type == 'mongodb':  ...
elif self.db_type == 'redis':    ...
```
Same pattern seen in `process_orders()` and `generate_sales_report()`.

---

## Prompt 1 — Pattern Opportunity Identification

### What the AI Found

| Problem | Name | Severity |
|---|---|---|
| 11 constructor parameters | Long Parameter List | 🚩 |
| Giant elif in connect() | Giant Conditional | 🚩 |
| Class does too many jobs | Mixed Responsibilities | 🚩 |
| Every new db edits old code | Open/Closed Violation | 🚩 |

### Patterns Recommended

| Pattern | Impact | Effort | Purpose |
|---|---|---|---|
| Factory | 10/10 | 4/10 | Fix creation and conditional |
| Strategy | 8/10 | 6/10 | Fix database-specific behaviour |
| Builder | 7/10 | 7/10 | Fix constructor explosion |

**Factory Pattern chosen — highest return on investment.**

### The Open/Closed Principle
> "Open for extension, closed for modification."

Adding Oracle after refactoring = create `OracleConnection` class only.
Existing code completely untouched.

---

## Prompt 2 — Pattern Implementation

### Refactored Structure

```
BaseDatabaseConnection (ABC)
        ↑
        ├── MySQLConnection      (charset, use_ssl, timeout)
        ├── PostgreSQLConnection (use_ssl)
        ├── MongoDBConnection    (retry_attempts, pool_size, use_ssl)
        └── RedisConnection      (minimal config only)

DatabaseConnectionFactory
    └── create_connection(db_type, **config)
```

### What the AI Added — Base Class

```python
from abc import ABC, abstractmethod

class BaseDatabaseConnection(ABC):
    @abstractmethod
    def connect(self):
        pass
```

Without it — factory hopes the object has `connect()`.
With it — factory guarantees every connection type works the same way.

Like a power socket standard — every plug fits because they all follow
the same interface.

### The Factory Class

```python
class DatabaseConnectionFactory:
    @staticmethod
    def create_connection(db_type, **config):
        if db_type == "mysql":
            return MySQLConnection(**config)
        if db_type == "postgresql":
            return PostgreSQLConnection(**config)
        if db_type == "mongodb":
            return MongoDBConnection(**config)
        if db_type == "redis":
            return RedisConnection(**config)

        raise ValueError(f"Unsupported database type: {db_type}")
```

---

## Key Takeaways

**Factory vs Strategy Pattern:**

| Pattern | Question it answers | Its job |
|---|---|---|
| Factory | Which object should I create? | Creation |
| Strategy | Which algorithm should I execute? | Behaviour |

Factory decides what gets built.
Strategy decides how something behaves.
They are often used together.

**What happens when Oracle support is requested:**

Before — edit `connect()`, risk breaking existing databases.
After — add `OracleConnection` class only. Zero modifications to existing code.

## Before and After Summary

| Element | Before | After |
|---|---|---|
| Classes | 1 giant class | 1 base + 4 specific + 1 factory |
| Parameters | 11 on one constructor | Only relevant params per class |
| Adding new database | Edit existing connect() | Add new class only |
| Guarantee on connect() | None | Enforced by ABC |
| Caller knowledge needed | db_type + all 11 params | db_type + relevant params only |

---

## Pattern Common Pitfalls Applied

| Pitfall | How it was avoided |
|---|---|
| Over-engineering | Factory chosen because it solves a real existing problem |
| Rigid implementation | Base class used instead of forcing textbook structure |
| Pattern tunnel vision | Strategy and Builder considered before committing to Factory |

---

---

# Overall Reflections Across All Exercises

## The One Question That Catches Everything

> "Does this function do ONE thing or many things?"

This question would have caught every problem across all four exercises
before writing a single line of code.

## Patterns That Keep Appearing

| Pattern | Where it appeared |
|---|---|
| Giant elif chain | process_orders, generate_sales_report, DatabaseConnection |
| Too many responsibilities | Every exercise |
| Shotgun surgery | generate_sales_report output formats |
| Magic numbers | process_orders |
| Missing documentation | calculate() |

## The Real Workflow

```
Understand the code first
        ↓
Identify problems yourself
        ↓
Use AI prompt to confirm and expand
        ↓
Compare AI output to your own thinking
        ↓
Merge improvements manually
        ↓
Run tests to verify nothing broke
        ↓
Document what you learned
```

AI gives you pieces. You assemble the final version.
