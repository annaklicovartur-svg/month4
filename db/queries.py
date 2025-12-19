# C-R-U-D 
# C - Create, R - Read, U - Update, D - Delete

CREATE_TASKS = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        completed INTEGER DEFAULT 0
    )
"""

INSERT_TASKS = 'INSERT INTO tasks (task) VALUES (?)'

SELECT_TASKS = "SELECT id, task, completed FROM tasks"

SELECT_TASKS_UNCOMPLETED = "SELECT id, task, completed FROM tasks WHERE completed = 0"
SELECT_TASKS_COMPLETED = "SELECT id, task, completed FROM tasks WHERE completed = 1"

UPDATE_TASKS = "UPDATE tasks SET task = ? WHERE id = ?"

DELETE_TASKS = 'DELETE FROM tasks WHERE id = ?'
