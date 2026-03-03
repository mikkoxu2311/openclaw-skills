SQLite at `~/.openclaw/workspace/skills/daily-journal/cache/journal.db`:

```sql
-- Daily conversation entries
CREATE TABLE entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    phase TEXT,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Captured items (insights, ideas, seeds, fleeting)
CREATE TABLE captures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    type TEXT NOT NULL,
    content TEXT,
    tags TEXT,
    context TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Day interrupt check-ins
CREATE TABLE day_interrupts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    time_slot TEXT,
    doing TEXT,
    reflection TEXT,
    insight TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Morning setup
CREATE TABLE morning_setup (
    date TEXT PRIMARY KEY,
    energy_score INTEGER,
    focus_task TEXT,
    template TEXT,
    context TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Conversational retrospectives and reflections
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    type TEXT NOT NULL,
    topic TEXT,
    summary TEXT,
    raw_content TEXT,
    tags TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```