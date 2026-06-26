import json


class Task:
    def __init__(self, name, description, priority):
        self.id = None
        self.name = name
        self.description = description
        self.priority = priority
    
    def __str__(self):
        return f"{self.id} | {self.name} | {self.description} | {self.priority}"


class Todolist:
    def __init__(self):
        self.tasks = []
        self.next_id = 1
    
    def add_task(self, task):
        for tsk in self.tasks:
            if tsk.name == task.name:
                return f"Task {task.name} already existed!"
        
        task.id = self.next_id
        self.next_id += 1
        self.tasks.append(task)
        self.save_to_json()
        
        return "Task added successfully!"
    
    def remove_task(self, task_id):
        for tsk in self.tasks:
            if tsk.id == task_id:
                self.tasks.remove(tsk)
                self.save_to_json()
                return "Task deleted!"
        
        return "Task not found!"
    
    def search_by_id(self, task_id):
        for tsk in self.tasks:
            if tsk.id == task_id:
                return tsk
        
        return None
    
    def search_by_name(self, name):
        for tsk in self.tasks:
            if tsk.name.lower() == name.lower():
                return tsk
        
        return None
    
    def show_tasks(self):
        priority_order = {
            "high": 3,
            "medium": 2, 
            "low": 1
        }
        
        sorted_tasks = sorted(
            self.tasks,
            key=lambda task: priority_order[task.priority],
            reverse=True
        )
        
        print(f"\n{'ID':<5}{'NAME':<15}{'DESCRIPTION':<25}{'PRIORITY':<10}")
        print("-" * 60)
        
        for task in sorted_tasks:
            print(f"{task.id:<5}{task.name:<15}{task.description:<25}{task.priority:<10}\n")
    
    def save_to_json(self):
        result = []
        
        for task in self.tasks:
            dic = {
                'ID': task.id,
                'NAME': task.name,
                'DESCRIPTION': task.description,
                'PRIORITY': task.priority
            }
            result.append(dic)
        
        with open('ToDoList.json', 'w') as file:
            json.dump(result, file, indent=4)
    

    def load_json(self):
        self.tasks = []
        
        try:
            with open('ToDoList.json', 'r') as file:
                data = json.load(file)
                
                for row in data:
                    task = Task(
                        row['NAME'],
                        row['DESCRIPTION'],
                        row['PRIORITY']
                    )
                    task.id = int(row['ID'])
                    self.tasks.append(task)
                
                if self.tasks:
                    self.next_id = max(task.id for task in self.tasks) + 1
                else:
                    self.next_id = 1
        
        except FileNotFoundError:
            print("No saved tasks found. Starting with an empty list.")
            self.tasks = []
            self.next_id = 1

def show_menu():
    print("1. Add Task")
    print("2. Delete Task")
    print("3. Show All Tasks")
    print("4. Search Task")
    print("0. Exit")

todolist = Todolist()
todolist.load_json()

print("Welcome to this ToDoList app:")
while True: 
    show_menu()
    choice = input("Choose: ")
    if choice == '1':
        name = input("Enter the name of the task: ")
        description = input("Enter the description: ")
        priority = input("Enter the priority of the task. It should be in this format -> ['high', 'medium', 'low']: ").lower()
        task = Task(name, description, priority)
        print(todolist.add_task(task))
    
    elif choice == '2':
        task_id = int(input("Enter task ID: "))
        print(todolist.remove_task(task_id))
    
    elif choice == '3':
        todolist.show_tasks()
    
    elif choice == '4':
        action = input("How do you want the search the task? [ID/Name]: ").lower()
        if action == 'id':
            task_id = int(input("Enter the task id: "))
            result = todolist.search_by_id(task_id)
            if result:
                print(result)
            else:
                print("Task not found!")
        elif action == 'name':
            name = input("Enter the name of the task: ")
            result = todolist.search_by_name(name)
            if result:
                print(result)
            else:
                print("Task not found!")
        else:
            print("Wrong input!")
    
    elif choice == '0':
        print("Thank you for using our todolist app.")
        break
