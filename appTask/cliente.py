import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def _make_request(method, endpoint, **kwargs):
    try:
        response = requests.request(method, f"{BASE_URL}{endpoint}", **kwargs)
        response.raise_for_status()
        if response.status_code == 204:
            return True
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}", file=sys.stderr)
        return None
    except ValueError:
        print("Error: Invalid JSON response from server.", file=sys.stderr)
        return None

def _get_task_id():
    while True:
        try:
            return int(input("Enter the task ID: "))
        except ValueError:
            print("Error: Please enter a valid integer.")

def create_task():
    title = input("Enter the task title: ")
    description = input("Enter the task description: ")
    if not title:
        print("Error: Title cannot be empty.")
        return None
    task = {"title": title, "description": description}
    return _make_request("post", "/tasks/", json=task)

def list_tasks():
    return _make_request("get", "/tasks/")

def get_task():
    task_id = _get_task_id()
    return _make_request("get", f"/tasks/{task_id}")

def update_task():
    task_id = _get_task_id()
    updated_task = {}
    title = input("Enter the new title (leave blank to keep current): ")
    if title:
        updated_task["title"] = title
    description = input("Enter the new description (leave blank to keep current): ")
    if description:
        updated_task["description"] = description
    completed_str = input("Completed? (y/n, leave blank to keep current): ").lower()
    if completed_str == "y":
        updated_task["completed"] = True
    elif completed_str == "n":
        updated_task["completed"] = False
    if not updated_task:
        print("No data provided for update.")
        return None
    return _make_make_request("put", f"/tasks/{task_id}", json=updated_task)

def delete_task():
    task_id = _get_task_id()
    return _make_request("delete", f"/tasks/{task_id}")

def main_menu():
    while True:
        print("\n" + "="*20)
        print("   Task Menu")
        print("="*20)
        print("1. Create Task")
        print("2. List Tasks")
        print("3. Get Task by ID")
        print("4. Update Task")
        print("5. Delete Task")
        print("6. Exit")
        print("="*20)
        choice = input("Select an option: ")

        if choice == "1":
            result = create_task()
            if result:
                print("Task created successfully:", result)
        elif choice == "2":
            tasks = list_tasks()
            if tasks is not None:
                if tasks:
                    print("Task List:")
                    for task in tasks:
                        status = "[X]" if task.get('completed') else "[ ]"
                        print(f"  {status} [{task.get('id')}] {task.get('title')}: {task.get('description')}")
                else:
                    print("No tasks in the list.")
        elif choice == "3":
            result = get_task()
            if result:
                print("Task details:", result)
        elif choice == "4. ":
            result = update_task()
            if result:
                print("Task updated successfully:", result)
        elif choice == "5":
            result = delete_task()
            if result:
                print("Task deleted successfully:", result)
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main_menu()