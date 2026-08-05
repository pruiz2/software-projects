'''
Name: task_manager.py
Author: Pablo Ruiz
Purpose: The following program allows the user to create, manage, and complete tasks.
'''

# Global state shared across all functions.
# tasks_dict mirrors what's in tasks.txt, keyed by task number, for fast in-memory lookups.
# task_number tracks the NEXT number to assign to a newly created task.
tasks_dict = {}
task_number = 1


def create_task():
    # Opened in "a" (append) mode because create_task only ever adds ONE new line
    # to the end of the file — it never needs to touch or rewrite existing lines.
    with open("tasks.txt", "a") as tasks:
        global tasks_dict
        global task_number

        task = input("Enter your task: \n")
        tasks_dict[task_number] = task

        # Write the new task to the file in "N. task text" format.
        tasks.write(f"{task_number}. {tasks_dict[task_number]}\n")

        # Advance the counter so the *next* task gets a fresh, unused number.
        task_number += 1


def mark_complete(line_number):
    global tasks_dict

    # First pass: read the ENTIRE file into memory as a list of lines.
    # We need the full picture before deciding what to change.
    with open("tasks.txt", "r") as read_tasks:
        lines = read_tasks.readlines()

    # Second pass: reopen in "w" (write) mode, which clears the file,
    # then rewrite every line back out — modifying only the one that matches.
    # ("w" is required here, unlike create_task, because we're replacing
    # the file's full contents, not just adding to the end.)
    with open("tasks.txt", "w") as tasks:
        # Tracks whether we ever found a line matching the requested task number.
        # Starts False; only flips to True inside the matching branch below.
        match = False

        for line in lines:
            # Split "3. clean my room" into ["3", " clean my room"] on the FIRST period.
            # We use the split-based number extraction (not line[0]) so this works
            # correctly for both single-digit and multi-digit task numbers (e.g. "10").
            parts = line.strip("\n").split(".")
            parts_number = int(parts[0])

            if parts_number == line_number:
                match = True
                # Tag this specific line as complete, and write it back.
                tasks.write(line.strip("\n") + "[COMPLETE]" + "\n")
                # Keep the in-memory dict in sync with what's now in the file.
                tasks_dict[parts_number] = line.strip("\n") + "[COMPLETE]" + "\n"
            else:
                # Not the target line — write it back completely unchanged.
                # This is critical: without this, every non-matching task
                # would be silently lost when the file gets rewritten.
                tasks.write(line.strip("\n") + "\n")

        # Only AFTER checking every line can we know for certain whether
        # the requested task number ever existed. Checking this outside
        # the loop (not per-line) avoids false "not found" messages.
        if not match:
            print("Task not found")


def view_tasks():
    # Simple read-only pass: open, print every line, done.
    with open("tasks.txt", "r") as tasks:
        for line in tasks:
            line = line.strip("\n")
            print(line)


def delete_tasks(line_number):
    global tasks_dict

    # Same two-pass pattern as mark_complete: read everything first,
    # then rewrite the file from scratch based on what should remain.
    with open("tasks.txt", "r") as read_tasks:
        lines = read_tasks.readlines()

    with open("tasks.txt", "w") as tasks:
        match = False

        for line in lines:
            parts = line.strip("\n").split(".")
            parts_number = int(parts[0])

            if parts_number != line_number:
                # Not the task being deleted — keep it by writing it back.
                tasks.write(line.strip("\n") + "\n")
            else:
                # This IS the task being deleted — simply don't write it.
                # Skipping the write is what "deletes" it from the file;
                # everything else gets carried over as normal.
                # .pop(key, None) removes the key from tasks_dict without
                # crashing if it somehow isn't there (None is the safe fallback).
                tasks_dict.pop(parts_number, None)
                match = True

        if not match:
            print("Task Not Found")


def build_dict():
    # Runs once, at program startup, to rebuild tasks_dict and task_number
    # from whatever is currently saved in tasks.txt — since the program
    # has no memory between runs except what's written to the file.
    with open("tasks.txt", "r") as f:
        lines = f.readlines()

        for line in lines:
            global tasks_dict
            global task_number

            line = line.strip("\n").split(".")
            task_number = int(line[0])
            tasks_dict[task_number] = line[1]

        # After scanning every line, figure out what the NEXT task number
        # should be. We deliberately use max() over ALL dict keys (not just
        # the last line read) because deletions can leave gaps or leave the
        # highest-numbered task anywhere in the file — max() finds the true
        # ceiling regardless of order or missing numbers.
        if len(tasks_dict) == 0:
            # No tasks exist yet (fresh/empty file) — start numbering at 1.
            task_number = 1
        else:
            # Highest existing task number, plus one, avoids ever reusing
            # a number that's already in use.
            task_number = max(tasks_dict.keys()) + 1


def main():
    # Populate tasks_dict and task_number from the file before the menu loop starts.
    build_dict()

    while True:
        print("=============================")
        print(" WELCOME TO THE TASK MANAGER ")
        print("=============================")
        print("PLEASE MAKE A SELECTION:")
        print("TYPE 1, 2, 3, or 4")
        print("[1] Create New Task")
        print("[2] View Tasks")
        print("[3] Mark Task Complete")
        print("[4] Delete Tasks")
        print("[5] Exit\n")

        user_input = int(input())

        if user_input == 1:
            new_task = create_task()
            view_tasks()  # Show the updated list immediately after adding.

        elif user_input == 2:
            display_tasks = view_tasks()

        elif user_input == 3:
            line_to_mark = int(input("Which task to mark complete?\n"))
            mark_task = mark_complete(line_to_mark)
            view_tasks()  # Confirm the change by showing the updated list.

        elif user_input == 4:
            line_to_delete = int(input("Which task to delete?\n"))
            delete_tasks(line_to_delete)
            view_tasks()  # Confirm the deletion by showing the updated list.

        elif user_input == 5:
            print("GOODBYE")
            break


main()
