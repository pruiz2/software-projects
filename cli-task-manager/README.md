# CLI Task Manager

A command-line task manager built in Python. Create, view, complete, and delete tasks, with everything persisted to a local file so your list survives between runs.

This was my first solo Python project, built without hints or provided code — the goal was to work through the design and debugging myself.

## Features

- **Create a task** — add a new task, automatically assigned the next available number
- **View tasks** — list every task, including completion status
- **Mark a task complete** — tag any task as done by its number, without losing the rest of the list
- **Delete a task** — remove a task by its number
- Handles invalid input gracefully (e.g. trying to complete or delete a task number that doesn't exist)
- Task numbers are preserved across program restarts, even with gaps left by deleted tasks

## How to run

```bash
python task_manager.py
```

You'll be dropped into a menu:

```
[1] Create New Task
[2] View Tasks
[3] Mark Task Complete
[4] Delete Tasks
[5] Exit
```

Tasks are stored in `tasks.txt` in the same directory, created automatically on first run.

## What I learned

The building part was straightforward — the debugging is where I actually learned something. A few bugs worth calling out:

- **Append vs. overwrite modes**: early on, I used `"a"` (append) mode to update existing lines in the file, which just piled a modified copy on top of the original instead of replacing it. Switching to `"w"` (write) for any operation that needed to rewrite the *whole* file's contents — versus `"a"` for operations that only ever add one new line — fixed it, but understanding *why* took some tracing.
- **A silent global variable collision**: I reused the same counter variable for two different purposes in two different functions — one to track "the next task number to assign," the other as a throwaway loop variable while marking a task complete. Since they shared a name, completing a task quietly corrupted the numbering used elsewhere in the program. No crash, no error — just wrong behavior that took deliberate testing to catch.
- **An off-by-one bug that only showed up after restarting the program**: task numbering worked fine within a single session but broke on every fresh restart, because I was deriving the "next number" from the last line in the file rather than the true highest number in use. Fixed by tracking the maximum task number across *all* existing tasks instead.
- **A missing newline character** at the end of the file caused two unrelated tasks to get merged onto a single line. Small, invisible character, real and confusing bug until I inspected the raw string with `repr()`.

## Next steps

Rebuilding this as a REST API with FastAPI, backed by MongoDB, and deployed with Vercel — see the sibling project folder once it's up.
